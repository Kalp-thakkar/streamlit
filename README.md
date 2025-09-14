This project is a Streamlit web app that uses Google’s Gemini API to classify movie reviews into Positive, Negative, or Neutral.
It also provides a confidence score, a short explanation, and key evidence phrases.

🚀 Features

Paste a movie review and analyze sentiment instantly.

Returns results in JSON format with:

label → Positive / Negative / Neutral

confidence → Score between 0–1

explanation → Short reasoning

evidence_phrases → Key phrases from review

Simple Streamlit UI for interaction.

Uses Gemini REST API directly with Python’s requests library.
