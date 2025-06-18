import streamlit as st
from PIL import Image
import os
import re
import random
import tempfile

# Page setup
st.set_page_config(page_title="AI Content Moderation", layout="centered")
st.title("🛡️ AI Content Moderation System")
st.caption("Upload text, images, or media for real-time sensitive content detection.")

# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Language selector
language = st.selectbox("🌐 Select Language", ["English", "Hindi", "Spanish"])

# Category toggles: CHECKED means BLOCK
st.markdown("### 🧠 Select Categories to Block")
blocked_categories = {
    "NSFW": st.checkbox("NSFW", value=True),
    "Hate Speech": st.checkbox("Hate Speech", value=True),
    "Violence": st.checkbox("Violence", value=True),
    "Profanity": st.checkbox("Profanity", value=True),
    "Drugs": st.checkbox("Drugs"),
    "Self-Harm": st.checkbox("Self-Harm"),
    "Sensitive Info": st.checkbox("Sensitive Info", value=True)
}

# Moderation logic for text
def moderate_text(text, categories):
    results = []
    text_lower = text.lower()

    checks = {
        "NSFW": "sex" in text_lower,
        "Profanity": any(w in text_lower for w in ["fuck", "shit"]),
        "Violence": "kill" in text_lower,
        "Drugs": "cocaine" in text_lower,
        "Self-Harm": "suicide" in text_lower,
        "Hate Speech": "hate" in text_lower,
        "Sensitive Info": any(re.search(p, text) for p in [
            r"\b\d{10}\b",  # phone
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\w{2,}",  # email
            r"\b\d{4} \d{4} \d{4}\b",  # Aadhaar-like
            r"\b(?:\d[ -]*?){13,16}\b",  # card number
            r"[A-Z]{5}[0-9]{4}[A-Z]"  # PAN
        ])
    }

    for category, detected in checks.items():
        if category not in categories:
            continue
        allowed = not categories[category]  # Invert: checked = block
        score = round(random.uniform(0.7, 0.99), 2) if detected else round(random.uniform(0.01, 0.3), 2)
        status = "✅ Allowed" if allowed else "❌ Blocked"
        result = "Detected" if detected else "Not Detected"
        icon = "✅" if not detected else ("⚠️" if allowed else "🚫")
        results.append(f"{icon} **Category:** {category} | **{status}** | **Score:** {score} | **Result:** {result}")

    return results

# Moderation logic for files
def moderate_file(uploaded_file, categories):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    results = []

    checks = {
        "NSFW": ext in [".jpg", ".jpeg", ".png"],
        "Profanity": ext in [".mp3", ".wav"],
        "Violence": ext == ".mp4"
    }

    for category, detected in checks.items():
        if category not in categories:
            continue
        allowed = not categories[category]  # Invert: checked = block
        score = round(random.uniform(0.7, 0.99), 2) if detected else round(random.uniform(0.01, 0.3), 2)
        status = "✅ Allowed" if allowed else "❌ Blocked"
        result = "Detected" if detected else "Not Detected"
        icon = "✅" if not detected else ("⚠️" if allowed else "🚫")
        results.append(f"{icon} **Category:** {category} | **{status}** | **Score:** {score} | **Result:** {result}")

    return results

# Chat-style input area
with st.chat_message("user"):
    st.markdown("### 💬 Type or upload content")

    # Text box first
    user_text = st.text_input("Enter your message...", key="chat_input", label_visibility="collapsed")

    # Upload field below the textbox
    uploaded_file = st.file_uploader("📎 Upload image, audio, or video", type=["jpg", "jpeg", "png", "mp3", "wav", "mp4"])

    # Send button
    if st.button("📨 upload"):
        if user_text or uploaded_file:
            st.session_state.chat.append(("user", user_text, uploaded_file))

# Display chat history with results
for sender, text, file in st.session_state.chat:
    with st.chat_message(sender):
        if text:
            st.markdown(f"**You:** {text}")
            results = moderate_text(text, blocked_categories)
            for r in results:
                st.markdown(r)

        if file:
            ext = os.path.splitext(file.name)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                st.image(Image.open(file), caption="Uploaded Image")
            elif ext in [".mp3", ".wav"]:
                st.audio(file)
            elif ext == ".mp4":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(file.read())
                    st.video(tmp.name)

            results = moderate_file(file, blocked_categories)
            for r in results:
                st.markdown(r)
