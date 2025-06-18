import streamlit as st
import re
from PIL import Image
import os
import tempfile

st.set_page_config(page_title="AI Moderation Chat", layout="centered")
st.title("🛡️ AI Chat Moderation Interface")

# Session state to store chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# --- Helper to simulate moderation result ---
def moderate_text(text):
    results = []
    if "fuck" in text.lower():
        results.append("🔴 Profanity Detected")
    if "kill" in text.lower():
        results.append("🔴 Violence Detected")
    if re.search(r"\b\d{10}\b", text):
        results.append("🔴 Phone Number Detected")
    if "sex" in text.lower():
        results.append("🔴 NSFW Content Detected")
    return results or ["✅ No Issues Detected"]

# --- Input section (like chat bubble) ---
with st.chat_message("user"):
    st.markdown("### 💬 Type or upload to test")

    # Chat input area
    user_input = st.text_input("Enter your message here", key="chat_input", label_visibility="collapsed", placeholder="Type something...")

    # File upload like attachment
    file = st.file_uploader("📎 Upload Image / Audio / Video", type=["png", "jpg", "jpeg", "mp4", "mp3", "wav"], label_visibility="collapsed")

    # Send button
    if st.button("Send"):
        if user_input or file:
            st.session_state.chat.append(("user", user_input, file))

# --- Display chat history ---
for idx, (sender, msg, uploaded_file) in enumerate(st.session_state.chat):
    with st.chat_message(sender):
        if msg:
            st.markdown(f"**You:** {msg}")
            moderation = moderate_text(msg)
            for issue in moderation:
                st.markdown(f"- {issue}")

        if uploaded_file:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            if file_ext in [".png", ".jpg", ".jpeg"]:
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image")
                st.markdown("- 🔴 NSFW Content Detected (simulated)")
            elif file_ext in [".mp3", ".wav"]:
                st.audio(uploaded_file)
                st.markdown("- 🔴 Profanity Detected (simulated)")
            elif file_ext in [".mp4"]:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.read())
                    st.video(tmp.name)
                    st.markdown("- 🔴 Violence Detected (simulated)")
