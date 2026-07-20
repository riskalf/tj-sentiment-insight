"""
pages/2_Tentang_Proyek.py
Halaman tentang proyek
"""

import streamlit as st

from utils.ui import load_css

st.set_page_config(
    page_title="Tentang Proyek -- TJ Sentiment Insight",
    page_icon="\u2139\ufe0f",
    layout="wide",
)

load_css()

st.html("""
<div style="font-size:22px; font-weight:700; color:var(--tj-text); margin-bottom:4px">
    Tentang Proyek
</div>
<p style="font-size:13px; color:var(--tj-text-body); margin:0 0 8px">
    Metodologi, perbandingan model, dan batasan dari penelitian di balik prototipe ini.
</p>
""")

# Metodologi
CRISP_DM = [
    ("Business Understanding",
     "Merumuskan tujuan penelitian: memahami sentimen dan tema keluhan "
     "pengguna aplikasi TJ: Transjakarta lewat ulasan Google Play Store."),
    ("Data Understanding",
     "Mengumpulkan 2.000 ulasan lewat scraping Google Play Store, "
     "lalu mengamati distribusi rating dan tanggal ulasan."),
    ("Data Preparation",
     "Pelabelan otomatis dari rating, case folding, normalisasi kata "
     "tidak baku, tokenisasi, stopword removal, dan stemming (khusus jalur SVM)."),
    ("Modeling",
     "Melatih dan membandingkan dua model: Support Vector Machine "
     "dengan TF-IDF, dan fine-tuning IndoBERT."),
    ("Evaluation",
     "Membandingkan accuracy, precision, recall, dan F1-score (macro "
     "average) kedua model pada data uji yang sama."),
    ("Deployment",
     "Prototipe ini -- aplikasi Streamlit yang mengimplementasikan "
     "model terbaik (IndoBERT) untuk analisis sentimen interaktif."),
]

langkah_html = "".join(
    f'''<div style="display:flex; gap:14px; margin-bottom:16px">
        <div style="flex-shrink:0; width:28px; height:28px; border-radius:50%;
                    background:var(--tj-primary-light); color:var(--tj-primary);
                    display:flex; align-items:center; justify-content:center;
                    font-size:13px; font-weight:700">{i}</div>
        <div>
            <div style="font-size:14px; font-weight:500; color:var(--tj-text); margin-bottom:2px">
                {nama}
            </div>
            <div style="font-size:13px; color:var(--tj-text-body); line-height:1.6">
                {deskripsi}
            </div>
        </div>
    </div>'''
    for i, (nama, deskripsi) in enumerate(CRISP_DM, start=1)
)

st.html(f"""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:24px 0 16px">
    Metodologi Penelitian (CRISP-DM)
</div>
{langkah_html}
""")

# Perbandingan model
BARIS_METRIK = [
    ("Accuracy", "95,10%", "97,68%"),
    ("Precision (macro)", "90,43%", "94,78%"),
    ("Recall (macro)", "90,98%", "96,59%"),
    ("F1-score (macro)", "90,70%", "95,65%"),
]

baris_html = "".join(
    f'''<tr style="border-bottom:1px solid var(--tj-border)">
        <td style="padding:10px 4px; color:var(--tj-text-body)">{metrik}</td>
        <td style="padding:10px 4px; text-align:right; color:var(--tj-text-body)">{svm}</td>
        <td style="padding:10px 4px; text-align:right; font-weight:700; color:var(--tj-primary)">{bert}</td>
    </tr>'''
    for metrik, svm, bert in BARIS_METRIK
)

st.html(f"""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:32px 0 16px">
    Perbandingan SVM vs IndoBERT
</div>
<div class="tj-card" style="padding:20px">
    <table style="width:100%; border-collapse:collapse; font-size:13px">
        <thead>
            <tr style="border-bottom:2px solid var(--tj-border)">
                <th style="text-align:left; padding:8px 4px; color:var(--tj-text-muted); font-weight:500">Metrik</th>
                <th style="text-align:right; padding:8px 4px; color:var(--tj-text-muted); font-weight:500">SVM</th>
                <th style="text-align:right; padding:8px 4px; color:var(--tj-primary); font-weight:700">IndoBERT</th>
            </tr>
        </thead>
        <tbody>
            {baris_html}
        </tbody>
    </table>
    <p style="font-size:11px; color:var(--tj-text-muted); margin:12px 0 0">
        IndoBERT unggul di semua metrik dan dipilih sebagai model yang dipakai pada prototipe ini.
    </p>
</div>
""")

# Kategori tema keluhan
KATEGORI_TEMA = [
    ("ti-bug", "Bug & Update Sistem",
     "Masalah teknis aplikasi: error, force close, atau tidak bisa dibuka setelah pembaruan."),
    ("ti-credit-card", "Tiket & Pembayaran",
     "Kendala transaksi: isi saldo, scan QR, atau saldo terpotong tanpa transaksi berhasil."),
    ("ti-map-pin", "Tracking & Akurasi Bus",
     "Ketidaksesuaian data posisi atau estimasi waktu kedatangan bus secara real-time."),
    ("ti-route", "Informasi Rute & Navigasi",
     "Kejelasan informasi rute, halte, koridor, dan arah tujuan pada aplikasi."),
    ("ti-steering-wheel", "Layanan Operasional",
     "Kualitas layanan di lapangan: sopir, armada, waktu tunggu, dan kebersihan."),
    ("ti-dots", "Lainnya",
     "Keluhan yang tidak cocok dengan kata kunci pada lima kategori di atas."),
]

kategori_html = "".join(
    f'''<div style="background:var(--tj-bg); border:1px solid var(--tj-border);
                border-radius:8px; padding:12px">
        <div style="font-size:13px; font-weight:500; color:var(--tj-text); margin-bottom:4px">
            <i class="ti {ikon}" style="color:var(--tj-primary); margin-right:4px"></i>{nama}
        </div>
        <div style="font-size:12px; color:var(--tj-text-body); line-height:1.5">{deskripsi}</div>
    </div>'''
    for ikon, nama, deskripsi in KATEGORI_TEMA
)

st.html(f"""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:32px 0 16px">
    Kategori Tema Keluhan
</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px">
    {kategori_html}
</div>
<p style="font-size:11px; color:var(--tj-text-muted); margin-top:10px">
    Tema keluhan dideteksi lewat pencocokan kata kunci (rule-based), hanya dijalankan
    untuk ulasan yang diprediksi bersentimen negatif.
</p>
""")

# Batasan penelitian
st.html("""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:32px 0 16px">
    Batasan Penelitian
</div>
<div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:8px; padding:16px">
    <div style="font-size:13px; font-weight:500; color:#92400E; margin-bottom:8px">
        <i class="ti ti-alert-triangle"></i> Perlu diperhatikan
    </div>
    <ul style="margin:0; padding-left:18px; font-size:13px; color:#78350F; line-height:1.8">
        <li>Klasifikasi sentimen hanya biner (positif/negatif); ulasan berbintang 3 (netral)
            tidak digunakan saat melatih model.</li>
        <li>Deteksi tema keluhan berbasis pencocokan kata kunci (rule-based), bukan model
            klasifikasi terlatih tersendiri, dan belum divalidasi terhadap data berlabel manusia.</li>
        <li>Prototipe ini adalah alat bantu riset/demonstrasi -- tidak terhubung dan tidak
            merepresentasikan sistem operasional resmi TJ: Transjakarta.</li>
        <li>Data ulasan diambil dari Google Play Store pada rentang waktu tertentu; sentimen
            pengguna dapat berubah seiring waktu dan pembaruan aplikasi.</li>
    </ul>
</div>
""")

# Keterangan Tambahan 
TEKNOLOGI = [
    "Python", 
    "Streamlit", 
    "Hugging Face Transformers", 
    "IndoBERT",
    "Scikit-learn", 
    "PyTorch",
]
chip_html = "".join(f'<span class="tj-chip">{t}</span>' for t in TEKNOLOGI)

st.html(f"""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:32px 0 16px">
    Teknologi yang Digunakan
</div>
<div>{chip_html}</div>

<div style="text-align:center; padding-top:32px; margin-top:32px;
            border-top:1px solid var(--tj-border); font-size:12px; color:var(--tj-text-muted)">
    <div>RISKA ALIFIA PUTRI &middot; 15210004 &middot; Program Studi Sains Data</div>
    <div style="margin-top:4px">Universitas Nusa Mandiri &middot; 2026</div>
</div>
""")