"""
utils/model.py

Fungsi untuk memuat model dan prediksi sentimen.
"""

import streamlit as st
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Repository model di Hugging Face
REPO_ID = "riskalf/tj-sentiment-indobert"

# Urutan label harus sesuai dengan model saat training
LABELS = ["negatif", "positif"]

# Panjang maksimum token
MAX_LENGTH = 128


@st.cache_resource(show_spinner="Memuat model IndoBERT dari Hugging Face...")
def load_model():
    """Memuat model dan tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(REPO_ID)
    model = AutoModelForSequenceClassification.from_pretrained(REPO_ID)
    model.eval()  # mode inferensi: matikan dropout, dsb.
    return model, tokenizer


def predict_sentiment(normalized_text: str) -> dict:
    """Prediksi sentimen dari teks yang sudah dinormalisasi."""
    model, tokenizer = load_model()

    inputs = tokenizer(
        normalized_text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1).squeeze().tolist()

    idx_terpilih = int(torch.argmax(logits, dim=-1).item())

    return {
        "label": LABELS[idx_terpilih],
        "confidence": probs[idx_terpilih],
        "probabilities": {LABELS[i]: probs[i] for i in range(len(LABELS))},
    }