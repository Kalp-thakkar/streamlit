import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not loaded. Check your .env file!")

# Gemini API endpoint
API_URL ="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContentkey=AIzaSyCGTWGQoOaBCs9op6__llUHrrLt0Y0tDds"

# Function to classify review
def classify_review(review: str):
    prompt = f"""
    You are a sentiment classifier for movie reviews.
    Classify the review into Positive, Negative, or Neutral.
    Provide output in valid JSON with keys:
    - label (Positive/Negative/Neutral)
    - confidence (0-1)
    - explanation (1-2 sentences)
    - evidence_phrases (list of key phrases from review)

    Review: "{review}"
    """

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }    
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(API_URL, headers=headers, json=data)
    print(response)

    if response.status_code != 200:
        return {"error": f"API request unable to fetch response due to unavailability of free API: {response.text}"}

    try:
        text_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_response)  # parse JSON returned by model
    except Exception as e:
        return {"error": "Invalid response format", "raw": response.text, "exception": str(e)}


# --- Streamlit UI ---
st.set_page_config(page_title="🎬 Movie Review Sentiment Marker", layout="centered")
st.title("🎬 Movie Review Sentiment Marker (LLM via REST API)")

review = st.text_area("Paste a movie review:", height=150)

if st.button("Analyze"):
    if review.strip():
        with st.spinner("Analyzing..."):
            result = classify_review(review)

        if "error" in result:
            st.error("⚠️ Model returned invalid output")
            st.code(result.get("raw", result["error"]))
        else:
            st.success(f"Label: {result['label']}")
            st.metric("Confidence", f"{result['confidence']:.2f}")
            st.write("**Explanation:**", result["explanation"])
            if result["evidence_phrases"]:
                st.write("**Evidence Phrases:**")
                st.write(", ".join(result["evidence_phrases"]))
    else:
        st.warning("Please enter a review before analyzing.")
