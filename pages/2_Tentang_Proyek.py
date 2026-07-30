"""
pages/2_Tentang_Proyek.py
Halaman tentang proyek
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff

from utils.ui import load_css

st.set_page_config(
    page_title="Tentang Proyek -- TJ Sentiment Insight",
    page_icon="\u2139\ufe0f",
    layout="wide",
)

load_css()

# Konstanta warna dan konfigurasi visual dashboard
C_PRIMARY = "#0f4c81"
C_ACCENT = "#f0a202"
C_POSITIF = "#15803d"
C_NEGATIF = "#b91c1c"
C_TEXT = "#0f172a"
C_TEXT_BODY = "#475569"
C_TEXT_MUTED = "#94a3b8"
C_BORDER = "#e2e8f0"
FONT_FAMILY = "Plus Jakarta Sans, sans-serif"

PLOTLY_CONFIG = {"displayModeBar": False}


def _apply_layout(fig, height=300, showlegend=False):
    """Layout dasar agar semua chart konsisten dengan tema aplikasi."""
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=C_TEXT_BODY, size=12),
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=C_BORDER)
    fig.update_yaxes(showgrid=True, gridcolor=C_BORDER, zeroline=False)
    return fig


def chart_distribusi_rating():
    """Membuat visualisasi distribusi rating pengguna."""
    x = ["1", "2", "3", "4", "5"]
    y = [229, 72, 62, 36, 1601]
    colors = [C_NEGATIF, C_NEGATIF, C_TEXT_MUTED, C_POSITIF, C_POSITIF]
    fig = go.Figure(go.Bar(
        x=x, y=y, marker_color=colors,
        text=[f"{v:,}".replace(",", ".") for v in y], textposition="outside",
    ))
    fig.update_layout(xaxis_title="Rating", yaxis_title="Jumlah Ulasan")
    return _apply_layout(fig, height=300)


def chart_distribusi_sentimen():
    """Membuat diagram distribusi sentimen."""
    labels = ["Positif", "Negatif"]
    values = [1637, 301]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62, sort=False,
        marker=dict(colors=[C_POSITIF, C_NEGATIF]),
        textinfo="label+percent", textfont=dict(size=12, color="white"),
    ))
    fig.add_annotation(text="<b>1.938</b><br>ulasan berlabel", showarrow=False,
                        font=dict(size=14, color=C_TEXT))
    return _apply_layout(fig, height=300, showlegend=True)


def chart_perbandingan_model():
    """Membuat grafik perbandingan performa model."""
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
    svm = [95.62, 90.99, 92.64, 91.79]
    bert = [98.20, 96.26, 96.89, 96.57]
    fig = go.Figure()
    fig.add_bar(name="SVM", x=metrics, y=svm, marker_color=C_TEXT_MUTED,
                text=[f"{v:.2f}%" for v in svm], textposition="outside")
    fig.add_bar(name="IndoBERT", x=metrics, y=bert, marker_color=C_PRIMARY,
                text=[f"{v:.2f}%" for v in bert], textposition="outside")
    fig.update_layout(barmode="group", yaxis_range=[0, 112],
                       yaxis_title="Skor Macro Average (%)")
    return _apply_layout(fig, height=340, showlegend=True)


def chart_confusion_matrix(z, colorscale):
    """"Menampilkan confusion matrix dalam bentuk heatmap."""
    labels = ["Negatif", "Positif"]
    z_text = [[str(v) for v in row] for row in z]
    fig = ff.create_annotated_heatmap(
        z=z, x=labels, y=labels, annotation_text=z_text,
        colorscale=colorscale, showscale=False,
    )
    fig.update_yaxes(autorange="reversed", title_text="Aktual")
    fig.update_xaxes(title_text="Prediksi", side="bottom")
    return _apply_layout(fig, height=280)


def chart_training_curve():
    """Membuat kurva training dan validation loss IndoBERT."""
    epochs = [1, 2, 3]
    train_loss = [0.378506, 0.125096, 0.068966]
    val_loss = [0.173782, 0.169925, 0.155439]
    fig = go.Figure()
    fig.add_scatter(x=epochs, y=train_loss, name="Training Loss", mode="lines+markers",
                     line=dict(color=C_ACCENT, width=3), marker=dict(size=8))
    fig.add_scatter(x=epochs, y=val_loss, name="Validation Loss", mode="lines+markers",
                     line=dict(color=C_PRIMARY, width=3), marker=dict(size=8))
    fig.update_layout(xaxis_title="Epoch", yaxis_title="Loss",
                       xaxis=dict(tickmode="array", tickvals=[1, 2, 3]))
    return _apply_layout(fig, height=300, showlegend=True)


def chart_tema_keluhan():
    """Membuat grafik distribusi tema keluhan."""
    tema = ["Bug & Update Sistem", "Tiket & Pembayaran", "Tracking & Akurasi Bus",
            "Informasi Rute & Navigasi", "Layanan Operasional", "Lainnya"]
    jumlah = [95, 80, 64, 25, 19, 18]
    tema, jumlah = tema[::-1], jumlah[::-1]  # terbesar tampil di atas
    fig = go.Figure(go.Bar(
        x=jumlah, y=tema, orientation="h", marker_color=C_PRIMARY,
        text=jumlah, textposition="outside",
    ))
    fig.update_layout(xaxis_title="Jumlah Ulasan Negatif")
    return _apply_layout(fig, height=320)


st.html("""
<div style="font-size:22px; font-weight:700; color:var(--tj-text); margin-bottom:4px">
    Tentang Proyek
</div>
<p style="font-size:13px; color:var(--tj-text-body); margin:0 0 8px">
    Metodologi, perbandingan model, dan batasan dari penelitian di balik prototipe ini.
</p>
""")

# Dashboard ringkasan hasil penelitian
st.html("""
<div style="font-size:15px; font-weight:700; color:var(--tj-text); margin:20px 0 14px">
    Dashboard Ringkasan Hasil Penelitian
</div>
""")

KPI = [
    ("Ulasan Di-scraping", "2.000"),
    ("Data Terlabeli", "1.938"),
    ("Akurasi Terbaik", "98,20%"),
    ("F1-Score Terbaik", "96,57%"),
    ("Tema Keluhan", "6 Kategori"),
]
kpi_cols = st.columns(len(KPI))
for col, (label, value) in zip(kpi_cols, KPI):
    with col:
        st.html(f"""
        <div class="tj-stat-card">
            <div class="tj-stat-label">{label}</div>
            <div class="tj-stat-value" style="font-size:19px">{value}</div>
        </div>
        """)

st.html('<div style="height:18px"></div>')

col_a, col_b = st.columns(2)
with col_a:
    st.html('<div class="tj-label">Distribusi Rating Ulasan (2.000 Data)</div>')
    st.plotly_chart(chart_distribusi_rating(), use_container_width=True, config=PLOTLY_CONFIG)
with col_b:
    st.html('<div class="tj-label">Distribusi Sentimen (Rating-Based Labeling)</div>')
    st.plotly_chart(chart_distribusi_sentimen(), use_container_width=True, config=PLOTLY_CONFIG)

col_c, col_d = st.columns(2)
with col_c:
    st.html('<div class="tj-label">Confusion Matrix &mdash; SVM (388 Data Uji)</div>')
    st.plotly_chart(chart_confusion_matrix([[53, 7], [10, 318]], "Blues"),
                     use_container_width=True, config=PLOTLY_CONFIG)
with col_d:
    st.html('<div class="tj-label">Confusion Matrix &mdash; IndoBERT (388 Data Uji)</div>')
    st.plotly_chart(chart_confusion_matrix([[57, 3], [4, 324]], "Oranges"),
                     use_container_width=True, config=PLOTLY_CONFIG)

st.html('<div class="tj-label">Kurva Pelatihan IndoBERT (Training vs Validation Loss)</div>')
st.plotly_chart(chart_training_curve(), use_container_width=True, config=PLOTLY_CONFIG)

# Tahapan penelitian CRISP-DM
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

# Perbandingan performa model
BARIS_METRIK = [
    ("Accuracy", "95,62%", "98,20%"),
    ("Precision (macro)", "90,99%", "96,26%"),
    ("Recall (macro)", "92,64%", "96,89%"),
    ("F1-score (macro)", "91,79%", "96,57%"),
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
""")
st.plotly_chart(chart_perbandingan_model(), use_container_width=True, config=PLOTLY_CONFIG)
st.html(f"""
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

# Visualisasi tema keluhan
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
""")
st.plotly_chart(chart_tema_keluhan(), use_container_width=True, config=PLOTLY_CONFIG)
st.html(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px">
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

# Teknologi yang digunakan 
TEKNOLOGI = [
    "Python", 
    "Streamlit", 
    "Plotly",
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
