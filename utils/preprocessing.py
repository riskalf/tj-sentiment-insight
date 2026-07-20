"""
utils/preprocessing.py
Fungsi preprocessing teks untuk model IndoBERT.

"""

from pathlib import Path

import pandas as pd
import streamlit as st

# Lokasi folder data
BASE_DIR = Path(__file__).resolve().parent.parent
KAMUS_PATH = BASE_DIR / "data" / "kamuskatabaku.xlsx"

# Kamus tambahan
CUSTOM_DICT = {
    # Nama & platform aplikasi
    "apk": "aplikasi", "app": "aplikasi", "apl": "aplikasi",
    # TransJakarta
    "tj": "transjakarta", "tije": "transjakarta", "busway": "bus",
    # Pembayaran & tiket
    "qr": "qrcode", "qris": "qrcode", "topup": "isi saldo", "tjpay": "dompet digital",
    # Error / teknis
    "eror": "error", "erro": "error", "ngelag": "lag", "ngadet": "error",
    "lemot": "lambat", "lelet": "lambat",
    # Negasi informal
    "gak": "tidak", "ga": "tidak", "gk": "tidak", "nggak": "tidak", "ngga": "tidak",
    "ndak": "tidak", "ndk": "tidak", "kagak": "tidak", "kaga": "tidak",
    "gabisa": "tidak bisa", "gatau": "tidak tahu", "gapaham": "tidak paham",
    "gausah": "tidak usah",
    # Abreviasi umum
    "yg": "yang", "jg": "juga", "krn": "karena", "karna": "karena", "kalo": "kalau",
    "klo": "kalau", "udah": "sudah", "udh": "sudah", "sdh": "sudah", "blm": "belum",
    "blum": "belum", "utk": "untuk", "tuk": "untuk", "dgn": "dengan", "dg": "dengan",
    "sm": "sama", "tpi": "tapi", "lg": "lagi", "lgi": "lagi", "bs": "bisa",
    "bsa": "bisa", "msh": "masih", "msih": "masih", "emg": "memang",
    "emang": "memang", "gmn": "bagaimana", "gimana": "bagaimana", "knp": "kenapa",
    "kpn": "kapan", "tlg": "tolong", "tlng": "tolong", "mhn": "mohon",
    "hrs": "harus", "hbs": "habis", "bgt": "banget", "bngt": "banget",
    "sy": "saya", "dlm": "dalam", "dpt": "dapat", "dpat": "dapat",
    # Variasi ejaan umum
    "mantab": "mantap", "mantabs": "mantap", "mantul": "mantap",
    "baguss": "bagus", "bgus": "bagus", "ok": "oke", "okk": "oke",
    "okeh": "oke", "iya": "ya",
    # Terima kasih
    "makasih": "terima kasih", "mksh": "terima kasih", "thx": "terima kasih",
    "tks": "terima kasih", "thanks": "terima kasih",
    # Kata kerja informal
    "nunggu": "tunggu", "nungguin": "tunggu", "ngantri": "antri",
    "bayarin": "bayar", "beliin": "beli",
}


@st.cache_data(show_spinner=False)
def load_kamus_dict() -> dict:
    """Memuat kamus normalisasi."""
    kamus = pd.read_excel(KAMUS_PATH)
    kamus_dict = dict(zip(kamus["tidak_baku"], kamus["kata_baku"]))
    kamus_dict.update(CUSTOM_DICT)
    return kamus_dict


def case_folding(text: str) -> str:
    """Mengubah teks menjadi huruf kecil."""
    return str(text).lower()


def normalize_text(text: str, kamus_dict: dict) -> str:
    """Menormalkan kata berdasarkan kamus."""
    words = text.split()
    return " ".join(kamus_dict.get(w, w) for w in words)


def preprocess_for_bert(raw_text: str) -> dict:
    """Menjalankan preprocessing untuk IndoBERT."""
    kamus_dict = load_kamus_dict()
    folded = case_folding(raw_text)
    normalized = normalize_text(folded, kamus_dict)
    return {
        "raw": raw_text,
        "case_folding": folded,
        "normalisasi": normalized,
    }