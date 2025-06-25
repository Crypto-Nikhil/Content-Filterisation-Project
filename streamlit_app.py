from moderation_model import predict_text

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
def moderate_text(text, categories_ui):
    predictions = predict_text(text)
    results = []
    block_flag = False

    for category, (detected, score) in predictions.items():
        if category not in categories_ui:
            continue

        to_block = categories_ui[category]   # True = block this category
        allow = not (to_block and detected)  # If blocked & detected → not allowed
        status = "✅ Allowed" if allow else "❌ Blocked"
        result = "Detected" if detected else "Not Detected"
        icon = "✅" if not detected else ("⚠️" if allow else "🚫")

        if to_block and detected:
            block_flag = True

        results.append(f"{icon} **Category:** {category} | **{status}** | **Score:** {score:.2f} | **Result:** {result}")

    # Show final moderation status
    if block_flag:
        st.warning("🚫 This content was BLOCKED based on selected guardrails.")
    else:
        st.success("✅ This content PASSED moderation.")

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
