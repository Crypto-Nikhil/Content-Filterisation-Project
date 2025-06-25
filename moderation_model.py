import joblib
import pandas as pd

# Load saved model + vectorizer
model = joblib.load("text_moderation_model.pkl")
vectorizer = joblib.load("text_vectorizer.pkl")

# List of moderation categories (from training)
category_labels = model.classes_.tolist()  # Or hardcode if needed

def predict_text(text):
    """Predict moderation categories for a given input string."""
    vec = vectorizer.transform([text])
    preds = model.predict(vec)
    probs = model.predict_proba(vec)

    # Convert to dictionary: {label: (detected, score)}
    result = {}
    for i, label in enumerate(category_labels):
        detected = bool(preds[0][i])
        score = round(probs[0][i], 2)
        result[label] = (detected, score)
    return result
