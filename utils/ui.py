"""
Komponen UI aplikasi.
"""

from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_PATH = BASE_DIR / "assets" / "style.css"


def _escape(text: str) -> str:
    """Escape karakter HTML."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# HTML

def _html_stat_card(label: str, value: str, sublabel: Optional[str] = None) -> str:
    sub_html = (
        f'<div style="font-size:11px;color:var(--tj-text-muted);margin-top:2px">{_escape(sublabel)}</div>'
        if sublabel else ""
    )
    return (
        f'<div class="tj-stat-card">'
        f'<div class="tj-stat-label">{_escape(label)}</div>'
        f'<div class="tj-stat-value">{_escape(value)}</div>'
        f'{sub_html}'
        f'</div>'
    )


def _html_sentiment_badge(label: str, confidence: float) -> str:
    is_positif = label == "positif"
    kelas = "positif" if is_positif else "negatif"
    ikon = "ti-mood-smile" if is_positif else "ti-mood-sad"
    teks = "Positif" if is_positif else "Negatif"
    persen = round(confidence * 100)
    return (
        '<div style="display:flex;align-items:center;justify-content:space-between;'
        'flex-wrap:wrap;gap:8px;margin-bottom:4px">'
        f'<span class="tj-badge tj-badge-{kelas}"><i class="ti {ikon}"></i>{teks}</span>'
        f'<span style="font-size:12px;color:var(--tj-text-muted)">Keyakinan model {persen}%</span>'
        '</div>'
        '<div class="tj-progress-track">'
        f'<div class="tj-progress-fill {kelas}" style="width:{persen}%"></div>'
        '</div>'
    )


def _html_theme_chip(theme_name: str) -> str:
    return (
        '<div class="tj-label">Tema keluhan terdeteksi</div>'
        f'<span class="tj-chip"><i class="ti ti-bug"></i>{_escape(theme_name)}</span>'
    )


def _html_keyword_chips(keywords: List[str]) -> str:
    if not keywords:
        return ""
    chips = "".join(
        f'<span class="tj-chip"><i class="ti ti-check" style="color:var(--tj-positif)"></i>{_escape(k)}</span>'
        for k in keywords
    )
    return f'<div class="tj-label" style="margin-top:12px">Keyword yang dikenali</div><div>{chips}</div>'


def _html_rating_comparison(rating_label: str, cocok: bool) -> str:
    ikon = "ti-check" if cocok else "ti-alert-triangle"
    warna = "var(--tj-positif)" if cocok else "var(--tj-text-muted)"
    return (
        f'<div style="display:flex;align-items:center;gap:6px;font-size:11px;'
        f'color:var(--tj-text-muted);margin:8px 0 4px">'
        f'<i class="ti {ikon}" style="color:{warna}"></i>{_escape(rating_label)}'
        f'</div>'
    )


def _html_preprocessing_trace(raw: str, normalized: str) -> str:
    return (
        '<div>'
        f'<span class="tj-mono-trace">{_escape(raw)}</span>'
        '<i class="ti ti-arrow-right" style="color:var(--tj-text-muted);vertical-align:middle;margin:0 4px"></i>'
        f'<span class="tj-mono-trace">{_escape(normalized)}</span>'
        '</div>'
    )


# UI

def load_css() -> None:
    import streamlit as st

    css = CSS_PATH.read_text(encoding="utf-8")

    # Tabler Icons
    st.markdown(
        """
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.44.0/tabler-icons.min.css">
""",
        unsafe_allow_html=True,
    )

    # CSS
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def stat_card(label: str, value: str, sublabel: Optional[str] = None) -> None:
    """Menampilkan kartu statistik."""
    import streamlit as st

    st.html(_html_stat_card(label, value, sublabel))


def sentiment_badge(label: str, confidence: float) -> None:
    """Menampilkan badge sentimen."""
    import streamlit as st

    st.html(_html_sentiment_badge(label, confidence))


def theme_chip(theme_name: str) -> None:
    """Menampilkan tema keluhan."""
    import streamlit as st

    if theme_name and theme_name != "Lainnya":
        st.html(_html_theme_chip(theme_name))


def keyword_chips(keywords: List[str]) -> None:
    """Menampilkan keyword yang ditemukan."""
    import streamlit as st

    html = _html_keyword_chips(keywords)
    if html:
        st.html(html)


def rating_comparison(rating_label: str, cocok: bool) -> None:
    """Menampilkan perbandingan rating."""
    import streamlit as st

    st.html(_html_rating_comparison(rating_label, cocok))


def preprocessing_trace(raw: str, normalized: str) -> None:
    """Menampilkan hasil preprocessing."""
    import streamlit as st

    st.html(_html_preprocessing_trace(raw, normalized))