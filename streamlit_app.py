import streamlit as st
import re

# --- Page setup ---
st.set_page_config(page_title="AI Content Filter", layout="centered")

st.title("🔒 AI Content Moderation Filter")
st.markdown("Detect and filter sensitive content across multiple categories, languages, and modalities.")

# --- Language Selector ---
language = st.selectbox("🌍 Select Language", ["English", "Hindi", "Spanish"])

# --- Category Toggles ---
st.markdown("### 🧠 Select Categories to Filter")
selected_categories = {
    "NSFW": st.checkbox("NSFW", value=True),
    "Hate Speech": st.checkbox("Hate Speech", value=True),
    "Violence": st.checkbox("Violence"),
    "Profanity": st.checkbox("Profanity", value=True),
    "Drugs": st.checkbox("Drugs"),
    "Self-Harm": st.checkbox("Self-Harm"),
    "Sensitive Info": st.checkbox("Sensitive Info", value=True)
}

# --- Text Input Section ---
st.markdown("### ✍️ Try It Live")
test_input = st.text_area("Enter sample message for testing", placeholder="Type something that might be flagged...", height=150)

# --- Analyze Button ---
if st.button("🔍 Analyze Text"):

    if not test_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        # ✅ Simulated prediction (replace this with actual model inference)
        mock_predictions = {
            "NSFW": 0.12 if "sex" not in test_input else 0.91,
            "Hate Speech": 0.08 if "hate" not in test_input else 0.95,
            "Violence": 0.10 if "kill" not in test_input else 0.89,
            "Profanity": 0.05 if "fuck" not in test_input else 0.93,
            "Drugs": 0.06 if "cocaine" not in test_input else 0.90,
            "Self-Harm": 0.04 if "suicide" not in test_input else 0.88,
        }

        # Regex-based PII detection (emails, phone numbers, Aadhaar, etc.)
        pii_patterns = [
            r"\b\d{10}\b",                              # Mobile number
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\w{2,}", # Email
            r"\b\d{4} \d{4} \d{4}\b",                    # Aadhaar format
            r"\b(?:\d[ -]*?){13,16}\b",                  # Credit card format
            r"[A-Z]{5}[0-9]{4}[A-Z]"                     # PAN format
        ]
        sensitive_info_detected = any(re.search(pattern, test_input) for pattern in pii_patterns)

        st.markdown("### 🧾 Analysis Result")

        for category, enabled in selected_categories.items():
            if enabled:
                if category == "Sensitive Info":
                    if sensitive_info_detected:
                        st.error("🔴 Sensitive Info: Blocked (Detected PII)")
                    else:
                        st.success("✅ Sensitive Info: Allowed")
                else:
                    score = mock_predictions.get(category, 0.0)
                    if score >= 0.8:
                        st.error(f"🔴 {category}: Blocked (score={score:.2f})")
                    else:
                        st.success(f"✅ {category}: Allowed (score={score:.2f})")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
