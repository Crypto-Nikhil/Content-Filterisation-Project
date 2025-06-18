import streamlit as st
from PIL import Image
import os
import re
import tempfile

# Page setup
st.set_page_config(page_title="AI Moderation System", layout="centered")
st.title("🛡️ AI Content Moderation System")
st.caption("Upload text, images, or media for real-time sensitive content detection.")

# Initialize session for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Language Selector
language = st.selectbox("🌐 Select Language", ["English", "Hindi", "Spanish"])

# Category Selection
st.markdown("### 🧠 Select Categories to Moderate")
selected_categories = {
    "NSFW": st.checkbox("NSFW", value=True),
    "Hate Speech": st.checkbox("Hate Speech", value=True),
    "Violence": st.checkbox("Violence", value=True),
    "Profanity": st.checkbox("Profanity", value=True),
    "Drugs": st.checkbox("Drugs"),
    "Self-Harm": st.checkbox("Self-Harm"),
    "Sensitive Info": st.checkbox("Sensitive Info", value=True)
}

# Moderation logic
def moderate_text(text, categories):
    flags = []
    text_lower = text.lower()
    if categories["Profanity"] and "fuck" in text_lower:
        flags.append("🔴 Profanity Detected")
    if categories["Violence"] and "kill" in text_lower:
        flags.append("🔴 Violence Detected")
    if categories["NSFW"] and "sex" in text_lower:
        flags.append("🔴 NSFW Content Detected")
    if categories["Drugs"] and "cocaine" in text_lower:
        flags.append("🔴 Drug Reference Detected")
    if categories["Self-Harm"] and "suicide" in text_lower:
        flags.append("🔴 Self-Harm Reference Detected")
    if categories["Hate Speech"] and "hate" in text_lower:
        flags.append("🔴 Hate Speech Detected")
    if categories["Sensitive Info"]:
        pii_patterns = [
            r"\b\d{10}\b",  # phone
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\w{2,}",  # email
            r"\b\d{4} \d{4} \d{4}\b",  # Aadhaar-like
            r"\b(?:\d[ -]*?){13,16}\b",  # card number
            r"[A-Z]{5}[0-9]{4}[A-Z]"  # PAN
        ]
        if any(re.search(p, text) for p in pii_patterns):
            flags.append("🔴 Sensitive Info Detected")
    return flags or ["✅ No Issues Detected"]

def moderate_file(uploaded_file, categories):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    results = []

    simulated_checks = {
        "NSFW": ext in [".jpg", ".jpeg", ".png"],
        "Profanity": ext in [".mp3", ".wav"],
        "Violence": ext == ".mp4"
    }

    for category, detected in simulated_checks.items():
        if category not in categories:
            continue
        allowed = categories[category]
        score = round(random.uniform(0.01, 0.99), 2) if detected else round(random.uniform(0.01, 0.3), 2)
        status = "✅ Allowed" if allowed else "❌ Blocked"
        detection = "Detected" if detected else "Not Detected"
        icon = "✅" if not detected else "🚫" if not allowed else "⚠️"
        results.append(f"{icon} **Category:** {category} | **{status}** | **Score:** {score} | **Result:** {detection}")

    return results


# Chat-like input area
with st.chat_message("user"):
    st.markdown("### 💬 Type or upload content")

    # --- Text input first ---
    user_text = st.text_input("Enter your message...", key="chat_input", label_visibility="collapsed")

    # --- File upload just below it ---
    uploaded_file = st.file_uploader("📎 Upload image, audio, or video", type=["jpg", "jpeg", "png", "mp3", "wav", "mp4"])

    # --- Send button ---
    if st.button("📨 Send"):
        if user_text or uploaded_file:
            st.session_state.chat.append(("user", user_text, uploaded_file))


# Display chat history
for sender, text, file in st.session_state.chat:
    with st.chat_message(sender):
        if text:
            st.markdown(f"**You:** {text}")
            results = moderate_text(text, selected_categories)
            for res in results:
                st.markdown(f"- {res}")

        if file:
            ext = os.path.splitext(file.name)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                img = Image.open(file)
                st.image(img, caption="Uploaded Image")
            elif ext in [".mp3", ".wav"]:
                st.audio(file)
            elif ext == ".mp4":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(file.read())
                    st.video(tmp.name)
            results = moderate_file(file, selected_categories)
            for res in results:
                st.markdown(f"- {res}")
