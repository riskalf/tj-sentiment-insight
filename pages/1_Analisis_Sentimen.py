"""
pages/1_Analisis_Sentimen.py
Halaman analisis sentimen

"""

import streamlit as st

from utils.model import predict_sentiment
from utils.preprocessing import preprocess_for_bert
from utils.theme_classifier import kategori_keluhan
from utils.ui import (
    keyword_chips,
    load_css,
    preprocessing_trace,
    rating_comparison,
    sentiment_badge,
    theme_chip,
)

st.set_page_config(
    page_title="Analisis Sentimen -- TJ Sentiment Insight",
    page_icon="\U0001F50E",
    layout="wide",
)

load_css()

CONTOH_POSITIF = (
    "Aplikasi ini sangat membantu untuk cek jadwal dan rute bus TransJakarta. "
    "Tampilannya juga mudah dipahami dan informasinya akurat."
)
CONTOH_NEGATIF = (
    "Setelah update terakhir aplikasi ini jadi sering error dan susah login. "
    "Tolong segera diperbaiki."
)


def _isi_contoh(teks: str) -> None:
    st.session_state.ulasan_input = teks


def _label_dari_rating(rating_1_5: int):
    if rating_1_5 < 3:
        return "negatif"
    if rating_1_5 > 3:
        return "positif"
    return None


st.html("""
<div style="font-size:22px; font-weight:700; color:var(--tj-text); margin-bottom:4px">
    Analisis Sentimen
</div>
<p style="font-size:13px; color:var(--tj-text-body); margin:0 0 20px">
    Masukkan ulasan pengguna untuk melihat prediksi sentimen dan tema keluhan.
</p>
""")

if "ulasan_input" not in st.session_state:
    st.session_state.ulasan_input = ""

# Input
with st.container(border=True):
    st.caption("Rating (opsional)")
    rating_terpilih = st.feedback("stars", key="rating_input")
    st.caption("Tidak memengaruhi prediksi -- hanya pembanding dengan aturan pelabelan penelitian.")

    ulasan = st.text_area(
        "Ulasan",
        key="ulasan_input",
        height=120,
        placeholder="Tempel atau ketik ulasan aplikasi di sini...",
        label_visibility="collapsed",
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.button(
            "Contoh ulasan positif",
            key="contoh_positif",
            on_click=_isi_contoh,
            args=(CONTOH_POSITIF,),
            use_container_width=True,
        )
    with col_b:
        st.button(
            "Contoh ulasan negatif",
            key="contoh_negatif",
            on_click=_isi_contoh,
            args=(CONTOH_NEGATIF,),
            use_container_width=True,
        )

    analisis_diklik = st.button("Analisis sentimen", key="tombol_analisis")

# Proses Analisis
if analisis_diklik:
    teks = ulasan.strip()
    if not teks:
        st.warning("Silakan masukkan ulasan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis..."):
            hasil_pre = preprocess_for_bert(teks)
            hasil_prediksi = predict_sentiment(hasil_pre["normalisasi"])

            kategori, kw_cocok = None, []
            if hasil_prediksi["label"] == "negatif":
                kategori, kw_cocok = kategori_keluhan(hasil_pre["normalisasi"])

        st.session_state.hasil_analisis = {
            "preprocessing": hasil_pre,
            "prediksi": hasil_prediksi,
            "kategori": kategori,
            "keywords": kw_cocok,
            "rating": rating_terpilih,
        }

# Hasil Analisis
if "hasil_analisis" in st.session_state:
    hasil = st.session_state.hasil_analisis
    prediksi = hasil["prediksi"]

    with st.container(border=True):
        sentiment_badge(prediksi["label"], prediksi["confidence"])

        if hasil["rating"] is not None:
            rating_1_5 = hasil["rating"] + 1 
            label_rating = _label_dari_rating(rating_1_5)
            if label_rating is None:
                rating_comparison(
                    f"Rating Anda ({rating_1_5}/5) netral -- tidak dipakai saat melatih "
                    "model (lihat Ruang Lingkup penelitian), jadi tidak ada pembanding langsung.",
                    cocok=False,
                )
            else:
                cocok = label_rating == prediksi["label"]
                kata_hubung = "sejalan" if cocok else "berbeda"
                rating_comparison(
                    f"Rating Anda ({rating_1_5}/5) {kata_hubung} dengan prediksi model "
                    f"(model mendeteksi sentimen {prediksi['label']}).",
                    cocok=cocok,
                )

        if prediksi["label"] == "positif":
            st.html("""
                <p style="font-size:13px; color:var(--tj-text-body); margin-top:12px">
                    Terima kasih atas ulasan Anda. Komentar ini tidak menunjukkan
                    indikasi keluhan utama.
                </p>
            """)
        else:
            if hasil["kategori"] != "Lainnya":
                theme_chip(hasil["kategori"])

            if hasil["keywords"]:
                keyword_chips(hasil["keywords"])

        with st.expander("Lihat proses preprocessing"):
            preprocessing_trace(
                hasil["preprocessing"]["raw"],
                hasil["preprocessing"]["normalisasi"],
            )