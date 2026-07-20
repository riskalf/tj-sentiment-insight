"""
Halaman beranda aplikasi.
"""

import streamlit as st

from utils.ui import load_css, stat_card

st.set_page_config(
    page_title="TJ Sentiment Insight",
    page_icon="\U0001F68C",  # bus
    layout="wide",
)

load_css()

# Data ringkasan
STATS = {
    "akurasi": "97,68%",
    "f1_macro": "95,65%",
    "jumlah_ulasan": "1.940",
    "tema_terbanyak": "Bug & Update Sistem",
    "tema_terbanyak_persen": "30,20% ulasan negatif",
}

# Hero
st.html("""
<div style="text-align:center; max-width:640px; margin:8px auto 32px">
    <span style="display:inline-block; font-size:12px; color:var(--tj-primary);
                 background:var(--tj-primary-light); padding:4px 12px;
                 border-radius:20px; margin-bottom:16px">
        Riset skripsi &middot; Sains data
    </span>
    <div style="font-size:30px; font-weight:700; line-height:1.35;
                color:var(--tj-text); margin-bottom:12px">
        Memahami Sentimen dan Keluhan Pengguna Aplikasi TJ: Transjakarta
    </div>
    <p style="font-size:15px; color:var(--tj-text-body); line-height:1.6; margin:0">
        Prototipe ini memakai model IndoBERT hasil penelitian untuk
        mengklasifikasikan sentimen ulasan secara otomatis dan mengenali
        tema keluhan pengguna.
    </p>
</div>
""")

_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("Coba analisis sekarang  \u2192", use_container_width=True, key="hero_cta"):
        st.switch_page("pages/1_Analisis_Sentimen.py")

st.write("")

# Statistik
col1, col2, col3, col4 = st.columns(4)
with col1:
    stat_card("Akurasi model", STATS["akurasi"])
with col2:
    stat_card("F1-score (macro)", STATS["f1_macro"])
with col3:
    stat_card("Ulasan dianalisis", STATS["jumlah_ulasan"])
with col4:
    stat_card("Keluhan terbanyak", STATS["tema_terbanyak"], STATS["tema_terbanyak_persen"])

st.write("")
st.write("")

# Alur penelitian
LANGKAH = [
    ("ti-cloud-download", "Scraping"),
    ("ti-filter", "Preprocessing"),
    ("ti-cpu", "Pelatihan"),
    ("ti-chart-bar", "Evaluasi"),
    ("ti-rocket", "Deployment"),
]

langkah_html = "".join(
    f'''<div style="position:relative; z-index:1; display:flex; flex-direction:column;
                align-items:center; gap:6px; background:var(--tj-bg); padding:0 4px">
        <div style="width:32px; height:32px; border-radius:50%; background:var(--tj-card);
                    border:1px solid #CBD5E1; display:flex; align-items:center; justify-content:center">
            <i class="ti {ikon}" style="font-size:15px; color:var(--tj-primary)"></i>
        </div>
        <span style="font-size:11px; color:var(--tj-text-body); text-align:center">{label}</span>
    </div>'''
    for ikon, label in LANGKAH
)

st.html(f"""
<div style="font-size:12px; color:var(--tj-text-muted); margin-bottom:18px">
    Alur penelitian (CRISP-DM)
</div>
<div style="display:flex; align-items:flex-start; justify-content:space-between; position:relative">
    <div style="position:absolute; top:16px; left:36px; right:36px; height:1px; background:var(--tj-border)"></div>
    {langkah_html}
</div>
""")

# Footer
st.html("""
<div style="text-align:center; padding-top:40px; margin-top:24px;
            border-top:1px solid var(--tj-border); font-size:11px; color:var(--tj-text-muted)">
    Skripsi Sains Data &middot; 2026
</div>
""")