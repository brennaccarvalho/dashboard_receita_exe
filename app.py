"""
Analytics Dashboard
Weekly Performance Report
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

from queries import (
    get_alerts_stats,
    get_arr_subscriptions,
    get_audience_profile,
    get_audience_weekly,
    get_cart_recovery,
    get_channel_revenue,
    get_checkout_funnel_quick,
    get_checkout_funnel_traditional,
    get_conversion_by_segment,
    get_email_stats,
    get_gsc_data,
    get_payment_conversion,
    get_product_performance,
    get_registration_by_channel,
    get_registration_funnel,
    get_registration_score_trend,
    get_revenue_weekly,
    get_upsell_vitrine,
)

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard de Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  THEME / BRAND TOKENS
# ═══════════════════════════════════════════════════════════════
THEME_MODE = st.sidebar.radio(
    "Tema",
    ["Escuro", "Claro"],
    index=0,
    help="Use o modo claro para fundo creme; modo escuro para tema noturno.",
)


def get_tokens(mode: str) -> dict:
    if mode == "Claro":
        return {
            "NAVY": "#1F3552",
            "PURPLE": "#4F46E5",
            "PINK": "#D94877",
            "ORANGE": "#C97A1F",
            "BG": "#F6F3EF",
            "CARD": "#FFF9F1",
            "CARD2": "#F1ECE5",
            "TEXT": "#18212B",
            "MUTED": "#6B7280",
            "GREEN": "#1F8A5B",
            "RED_SOFT": "#C65B5B",
            "SIDEBAR_BG": "#20324B",
            "SIDEBAR_TEXT": "#F8FAFC",
            "BORDER": "#DDD6CE",
            "BORDER_SOFT": "#ECE4DC",
            "GRID": "#D8D1C8",
            "TABLE_HEAD": "#F5F1EB",
            "SHADOW": "rgba(15, 23, 42, 0.06)",
        }

    # dark mode (default)
    return {
        "NAVY": "#0F172A",
        "PURPLE": "#7C8CF8",
        "PINK": "#E56B91",
        "ORANGE": "#F2A541",
        "BG": "#0B1220",
        "CARD": "#121B2B",
        "CARD2": "#172233",
        "TEXT": "#E5EDF8",
        "MUTED": "#94A3B8",
        "GREEN": "#2FB37D",
        "RED_SOFT": "#F07C7C",
        "SIDEBAR_BG": "#10192B",
        "SIDEBAR_TEXT": "#F8FAFC",
        "BORDER": "#253247",
        "BORDER_SOFT": "#1C2738",
        "GRID": "#334155",
        "TABLE_HEAD": "#162132",
        "SHADOW": "rgba(0, 0, 0, 0.18)",
    }

_tokens = get_tokens(THEME_MODE)
NAVY = _tokens["NAVY"]
PURPLE = _tokens["PURPLE"]
PINK = _tokens["PINK"]
ORANGE = _tokens["ORANGE"]
BG = _tokens["BG"]
CARD = _tokens["CARD"]
CARD2 = _tokens["CARD2"]
TEXT = _tokens["TEXT"]
MUTED = _tokens["MUTED"]
GREEN = _tokens["GREEN"]
RED_SOFT = _tokens["RED_SOFT"]
SIDEBAR_BG = _tokens["SIDEBAR_BG"]
SIDEBAR_TEXT = _tokens["SIDEBAR_TEXT"]
BORDER = _tokens["BORDER"]
BORDER_SOFT = _tokens["BORDER_SOFT"]
GRID = _tokens["GRID"]
TABLE_HEAD = _tokens["TABLE_HEAD"]
SHADOW = _tokens["SHADOW"]


def rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


TRACK = rgba(TEXT, 0.08)
TRACK_STRONG = rgba(TEXT, 0.12)
PURPLE_SOFT = rgba(PURPLE, 0.14)
PINK_SOFT = rgba(PINK, 0.14)
ORANGE_SOFT = rgba(ORANGE, 0.14)
GREEN_SOFT = rgba(GREEN, 0.14)
SIDEBAR_PANEL = rgba(SIDEBAR_TEXT, 0.06)
SIDEBAR_PANEL_STRONG = rgba(SIDEBAR_TEXT, 0.10)
SIDEBAR_BORDER = rgba(SIDEBAR_TEXT, 0.16)

# ═══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Google Fonts ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Base ───────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [class*="css"], .stApp, .main {{
  font-family: 'Figtree', sans-serif !important;
  color: {TEXT} !important;
  line-height: 1.45;
}}
p, [data-testid="stMarkdownContainer"] p {{
  margin-bottom: 0;
}}

[data-testid="stAppViewContainer"], .stApp {{
  background:
    linear-gradient(180deg, {BG} 0%, {CARD2} 140%) !important;
  background-attachment: fixed;
}}

[data-testid="stHeader"] {{
  background: transparent !important;
}}

h1, h2, h3, h4 {{
  font-family: 'Figtree', sans-serif !important;
  font-weight: 600 !important;
  color: {TEXT} !important;
}}

/* ── Hide Streamlit chrome ──────────────────────── */
#MainMenu, footer, .stDeployButton {{ visibility: hidden; }}
.block-container {{
  padding: 1.25rem 1.5rem 2.5rem 1.5rem !important;
  max-width: 1440px !important;
}}

/* ── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] > div:first-child {{
  background: {SIDEBAR_BG} !important;
  border-right: 1px solid {SIDEBAR_BORDER};
}}
[data-testid="stSidebar"] * {{
  color: {SIDEBAR_TEXT} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
  background: {rgba(SIDEBAR_TEXT, 0.06)} !important;
  border-color: {SIDEBAR_BORDER} !important;
  border-radius: 12px !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stCheckbox label {{
  color: {rgba(SIDEBAR_TEXT, 0.72)} !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] {{
  gap: 0.35rem;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
  background: transparent;
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 0.46rem 0.6rem;
  transition: all 0.15s ease;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
  background: {rgba(SIDEBAR_TEXT, 0.06)};
  border-color: {rgba(SIDEBAR_TEXT, 0.10)};
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
  background: {rgba(PURPLE, 0.22)};
  border-color: {rgba(PURPLE, 0.45)};
  box-shadow: inset 0 0 0 1px {rgba(PURPLE, 0.18)};
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
  color: {SIDEBAR_TEXT} !important;
  font-weight: 600 !important;
}}
[data-testid="stSidebar"] .stCheckbox > label {{
  padding-top: 0.35rem;
}}
.sidebar-panel {{
  background: {rgba(SIDEBAR_TEXT, 0.05)};
  border: 1px solid {SIDEBAR_BORDER};
  border-radius: 16px;
  padding: 14px 15px;
}}
.sidebar-kicker {{
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {rgba(SIDEBAR_TEXT, 0.72)};
  margin-bottom: 10px;
}}
.status-row {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}}
.status-row:last-child {{ margin-bottom: 0; }}
.status-dot {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.status-text {{
  font-size: 12px;
  color: {SIDEBAR_TEXT};
}}

/* ── Context strip ──────────────────────────────── */
.context-strip {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.65rem;
  margin: -0.55rem 0 1.1rem 0;
}}
.context-chip {{
  display: flex;
  align-items: flex-start;
  gap: 0.55rem;
  padding: 0.8rem 0.9rem;
  border-radius: 16px;
  border: 1px solid {BORDER};
  background: {CARD};
  min-height: 72px;
}}
.context-chip.good {{
  border-color: {rgba(GREEN, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {GREEN_SOFT} 130%);
}}
.context-chip.alert {{
  border-color: {rgba(ORANGE, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {ORANGE_SOFT} 130%);
}}
.context-chip.accent {{
  border-color: {rgba(PURPLE, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {PURPLE_SOFT} 130%);
}}
.context-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.context-copy {{
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}}
.context-label {{
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: {MUTED};
}}
.context-value {{
  font-size: 13px;
  color: {TEXT};
  font-weight: 600;
}}

/* ── Tabs ───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
  background: {CARD};
  border-radius: 16px;
  padding: 4px;
  gap: 5px;
  border: 1px solid {BORDER};
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 0.2rem;
}}
.stTabs [data-baseweb="tab"] {{
  font-family: 'Figtree', sans-serif;
  font-size: 12.5px;
  font-weight: 600;
  color: {MUTED};
  border-radius: 12px;
  padding: 9px 16px;
  border: none !important;
  background: transparent !important;
  white-space: nowrap;
  transition: all 0.15s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{
  color: {TEXT};
  background: {rgba(PURPLE, 0.08)} !important;
}}
.stTabs [data-baseweb="tab"]:focus-visible {{
  outline: 2px solid {rgba(PURPLE, 0.35)};
  outline-offset: 1px;
}}
.stTabs [aria-selected="true"] {{
  background: {PURPLE} !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: none;
}}
.stTabs [data-baseweb="tab-panel"] {{
  background: transparent !important;
  padding: 0 !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}

/* ── KPI Card ───────────────────────────────────── */
.kpi-card {{
  background: {CARD};
  border-radius: 16px;
  padding: 16px 18px 14px 18px;
  border: 1px solid {BORDER};
  min-height: 116px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.45rem;
  position: relative;
  overflow: hidden;
  box-shadow: none;
}}
.kpi-card::before {{
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 4px;
  border-radius: 0 0 18px 18px;
}}
.kpi-card::after {{
  display: none;
}}
.kpi-label {{
  font-size: 10px;
  font-weight: 600;
  color: {MUTED};
  text-transform: uppercase;
  letter-spacing: 0.09em;
  font-family: 'Figtree', sans-serif;
  min-height: 2.4em;
}}
.kpi-value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 23px;
  font-weight: 600;
  color: {TEXT};
  line-height: 1.1;
}}
.kpi-delta-pos {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {GREEN};
  margin-top: auto;
}}
.kpi-delta-neg {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {ORANGE};
  margin-top: auto;
}}
.kpi-delta-neu {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {MUTED};
  margin-top: auto;
}}

/* ── Section Title ──────────────────────────────── */
.sec-title {{
  font-family: 'Figtree', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: {TEXT};
  margin: 1.25rem 0 0.65rem 0;
  padding-bottom: 8px;
  border-bottom: 1px solid {BORDER};
}}

/* ── Data Table ─────────────────────────────────── */
.dtable {{
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 12.5px;
  font-family: 'Figtree', sans-serif;
  background: {CARD};
  border: 1px solid {BORDER};
  border-radius: 16px;
  overflow: hidden;
  box-shadow: none;
}}
.dtable th {{
  background: {TABLE_HEAD};
  color: {MUTED};
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid {BORDER};
}}
.dtable td {{
  padding: 9px 14px;
  border-bottom: 1px solid {BORDER_SOFT};
  color: {TEXT};
  vertical-align: middle;
}}
.dtable tr:last-child td {{ border-bottom: none; }}
.dtable tr:hover td {{ background: {rgba(PURPLE, 0.04)}; }}
.mono {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; }}

/* ── Badges ─────────────────────────────────────── */
.bg {{ background:{GREEN_SOFT}; color:{GREEN}; padding:2px 8px; border-radius:999px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bo {{ background:{ORANGE_SOFT}; color:{ORANGE}; padding:2px 8px; border-radius:999px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bp {{ background:{PURPLE_SOFT}; color:{PURPLE}; padding:2px 8px; border-radius:999px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bk {{ background:{PINK_SOFT}; color:{PINK}; padding:2px 8px; border-radius:999px; font-size:11px; font-family:'JetBrains Mono',monospace; }}

/* ── Band Row ───────────────────────────────────── */
.band {{
  background: {CARD};
  border-radius: 14px;
  padding: 12px 14px;
  margin-bottom: 7px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.9rem;
  border: 1px solid {BORDER};
  box-shadow: none;
}}
.band-label {{ font-size: 12.5px; color: {TEXT}; }}
.band-val {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; text-align: right; }}

/* ── Funnel Row ─────────────────────────────────── */
.frow {{
  background: {CARD};
  border-radius: 16px;
  padding: 13px 16px;
  margin-bottom: 7px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.9rem;
  border-left: 3px solid transparent;
  box-shadow: none;
}}
.frow-label {{ font-size: 12.5px; font-weight: 500; color: {TEXT}; }}
.frow-sub   {{ font-size: 10.5px; color: {MUTED}; font-family: 'JetBrains Mono', monospace; margin-top:2px; }}
.frow-n     {{ font-family: 'JetBrains Mono', monospace; font-size: 17px; font-weight: 600; text-align:right; }}
.frow-pct   {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {MUTED}; text-align:right; }}

/* ── Alert / Info ───────────────────────────────── */
.alert-box {{
  background: {ORANGE_SOFT};
  border: 1px solid {rgba(ORANGE, 0.28)};
  border-radius: 14px;
  padding: 11px 15px;
  font-size: 12.5px;
  color: {TEXT};
  margin-bottom: 10px;
  box-shadow: none;
}}
.info-box {{
  background: {PURPLE_SOFT};
  border: 1px solid {rgba(PURPLE, 0.28)};
  border-radius: 14px;
  padding: 11px 15px;
  font-size: 12.5px;
  color: {TEXT};
  margin-bottom: 10px;
  box-shadow: none;
}}
.takeaway-note {{
  margin: 0 0 0.8rem 0;
  padding: 0.72rem 0.9rem;
  border-radius: 14px;
  border: 1px solid {BORDER};
  background: {CARD};
  color: {TEXT};
  font-size: 12.5px;
  line-height: 1.45;
}}
.takeaway-note strong {{
  color: {TEXT};
}}
.takeaway-note.good {{
  border-color: {rgba(GREEN, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {GREEN_SOFT} 130%);
}}
.takeaway-note.alert {{
  border-color: {rgba(ORANGE, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {ORANGE_SOFT} 130%);
}}
.takeaway-note.accent {{
  border-color: {rgba(PURPLE, 0.32)};
  background: linear-gradient(135deg, {rgba(CARD, 0.94)} 0%, {PURPLE_SOFT} 130%);
}}

/* ── Bar mini ───────────────────────────────────── */
.mini-bar-wrap {{
  flex: 1; margin: 0 14px;
  height: 5px;
  background: {TRACK};
  border-radius: 3px;
  overflow: hidden;
}}
.mini-bar-fill {{ height: 100%; border-radius: 3px; }}

/* ── Selectbox / inputs ─────────────────────────── */
[data-baseweb="select"] > div {{
  background: {CARD2} !important;
  border-color: {BORDER} !important;
  border-radius: 12px !important;
  box-shadow: none !important;
}}
.stSelectbox [data-baseweb="select"] > div:hover {{
  border-color: {rgba(PURPLE, 0.35)} !important;
}}
[data-baseweb="select"] > div:focus-within {{
  border-color: {PURPLE} !important;
  box-shadow: 0 0 0 1px {rgba(PURPLE, 0.20)} !important;
}}
.stSelectbox label, .stRadio label {{
  font-size: 11px !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: {MUTED} !important;
}}
.stRadio [data-testid="stMarkdownContainer"] p {{
  font-size: 13px !important;
  color: {TEXT} !important;
}}
div[role="radiogroup"] label {{
  font-size: 13px !important;
}}

/* ── Layout alignment ───────────────────────────── */
[data-testid="stHorizontalBlock"] {{
  align-items: stretch;
}}
[data-testid="column"] {{
  display: flex;
  flex-direction: column;
}}
[data-testid="column"] > div {{
  width: 100%;
}}

/* ── Divider ────────────────────────────────────── */
hr {{ border-color: {BORDER} !important; }}

/* ── Scrollbar ──────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {TRACK_STRONG}; border-radius: 3px; }}

/* ── Header / hero ──────────────────────────────── */
.hero-card {{
  position: relative;
  overflow: hidden;
  margin-bottom: 1rem;
  padding: 1.25rem 1.4rem;
  border-radius: 18px;
  border: 1px solid {BORDER};
  background: {CARD};
  box-shadow: none;
}}
.hero-card::after {{
  display: none;
}}
.hero-kicker {{
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: {MUTED};
  margin-bottom: 8px;
}}
.hero-title {{
  font-family: 'Figtree', sans-serif;
  font-size: 30px;
  line-height: 1.08;
  color: {TEXT};
  letter-spacing: -0.02em;
}}
.hero-meta {{
  margin-top: 10px;
  font-size: 13px;
  color: {MUTED};
}}
.hero-meta .mono {{
  font-size: 13px;
}}

/* ── Plotly surfaces ────────────────────────────── */
div[data-testid="stPlotlyChart"] {{
  background: {CARD};
  border: 1px solid {BORDER};
  border-radius: 16px;
  padding: 0.35rem 0.45rem 0.2rem 0.45rem;
  box-shadow: none;
}}
div[data-testid="stPlotlyChart"] > div {{
  border-radius: 12px;
}}

/* ── Responsive ─────────────────────────────────── */
@media (max-width: 980px) {{
  .block-container {{
    padding: 1rem 1rem 2rem 1rem !important;
  }}
  .hero-title {{
    font-size: 31px;
  }}
  .context-chip {{
    min-width: 150px;
  }}
  .stTabs [data-baseweb="tab-list"] {{
    gap: 0.4rem;
  }}
  .stTabs [data-baseweb="tab"] {{
    padding: 0.75rem 0.95rem;
  }}
}}

@media (max-width: 640px) {{
  .hero-card {{
    padding: 1.15rem 1rem;
    border-radius: 20px;
  }}
  .hero-title {{
    font-size: 24px;
  }}
  .hero-meta {{
    font-size: 12px;
    line-height: 1.5;
  }}
  .context-strip {{
    gap: 0.5rem;
  }}
  .context-chip {{
    min-width: 100%;
  }}
  .kpi-card {{
    min-height: 110px;
  }}
  .sec-title {{
    font-size: 17px;
  }}
}}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def fmt_brl(v: float) -> str:
    s = f"{abs(v):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + "R$ " + s


def fmt_date_pt_br(value: datetime) -> str:
    months = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ]
    return f"{value.day:02d} de {months[value.month - 1]} de {value.year}"


def fmt_month_short_pt(value: datetime) -> str:
    months = [
        "jan", "fev", "mar", "abr", "mai", "jun",
        "jul", "ago", "set", "out", "nov", "dez",
    ]
    return f"{months[value.month - 1]}/{str(value.year)[2:]}"


def fmt_k(v: float) -> str:
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.1f}k"
    return str(int(v))


def spacer(height: int = 14) -> None:
    st.markdown(f'<div style="height:{height}px;"></div>', unsafe_allow_html=True)


def kpi(label: str, value: str, delta: float | None = None,
        good_if_positive: bool = True, accent: str = PINK) -> str:
    if delta is not None:
        is_good = (delta >= 0 and good_if_positive) or (delta < 0 and not good_if_positive)
        cls  = "kpi-delta-pos" if is_good else "kpi-delta-neg"
        sign = "▲" if delta >= 0 else "▼"
        dt   = f'<div class="{cls}">{sign} {abs(delta):.1f}% vs sem. ant.</div>'
    else:
        dt = f'<div class="kpi-delta-neu">—</div>'
    return f"""
    <div class="kpi-card" style="border-bottom:3px solid {accent};">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {dt}
    </div>"""

def section(title: str) -> None:
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)


def takeaway(text: str, tone: str = "accent") -> None:
    st.markdown(f'<div class="takeaway-note {tone}">{text}</div>', unsafe_allow_html=True)


def context_chip(label: str, value: str, tone: str = "neutral", dot_color: str | None = None) -> str:
    dot_color = dot_color or MUTED
    return f"""
    <div class="context-chip {tone}">
      <div class="context-dot" style="background:{dot_color};"></div>
      <div class="context-copy">
        <div class="context-label">{label}</div>
        <div class="context-value">{value}</div>
      </div>
    </div>
    """


def merge_nested_dict(base: dict, overrides: dict) -> dict:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def plotly_theme() -> dict:
    axis_defaults = dict(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=BORDER,
        tickfont=dict(size=11, color=MUTED),
        title=dict(font=dict(size=11, color=MUTED)),
        automargin=True,
    )
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Figtree, sans-serif", color=TEXT, size=12),
        margin=dict(l=10, r=10, t=34, b=10),
        xaxis={**axis_defaults, "gridcolor": "rgba(0,0,0,0)"},
        yaxis=axis_defaults,
        legend=dict(
            font=dict(size=10, color=MUTED),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor=CARD2,
            font=dict(family="Figtree", size=12, color=TEXT),
            bordercolor=BORDER,
        ),
    )


def plotly_layout(**overrides) -> dict:
    return merge_nested_dict(plotly_theme(), overrides)


cfg = {"displayModeBar": False, "responsive": True}


# ═══════════════════════════════════════════════════════════════
#  DATA LAYER
# ═══════════════════════════════════════════════════════════════
TODAY = datetime(2026, 3, 17)
N = 8
CURRENT_WEEK_START = TODAY - timedelta(days=TODAY.weekday())
WEEK_START_DATES = [CURRENT_WEEK_START - timedelta(weeks=N - 1 - i) for i in range(N)]
WEEKS = [d.strftime("%d/%m") for d in WEEK_START_DATES]
WEEK_SELECTION_TO_START = {
    d.strftime("%d/%m"): d.strftime("%Y-%m-%d")
    for d in WEEK_START_DATES
}
CW = WEEKS[-1]   # current week label

CHS = ["Orgânico", "E-mail", "Direto", "Redes Sociais", "Pago", "Alertas"]
CHS_PAL = [PURPLE, PINK, ORANGE, NAVY, GREEN, MUTED]

CURR_MONTH = datetime(TODAY.year, TODAY.month, 1)
HIST_MONTH_DATES = pd.date_range(end=CURR_MONTH, periods=6, freq="MS")
FC_MONTH_DATES = pd.date_range(start=CURR_MONTH + pd.offsets.MonthBegin(1), periods=6, freq="MS")
MONTHS_HIST = [fmt_month_short_pt(d.to_pydatetime()) for d in HIST_MONTH_DATES]
MONTHS_FORECAST = [fmt_month_short_pt(d.to_pydatetime()) for d in FC_MONTH_DATES]
REV_MONTH_HIST = [332000, 341000, 356000, 349000, 378000, 392000]
REV_FORECAST_BASE = [401000, 411000, 423000, 434000, 447000, 460000]
REV_FORECAST_LOW = [391000, 398000, 408000, 417000, 427000, 438000]
REV_FORECAST_HIGH = [409000, 423000, 437000, 450000, 467000, 482000]
REV_TARGET = [405000, 414000, 426000, 438000, 452000, 468000]
REV_DRIVER_RETAIN = [252000, 258000, 265000, 272000, 279000, 286000]
REV_DRIVER_NEW = [111000, 114000, 118000, 121000, 125000, 129000]
REV_DRIVER_UPSELL = [38000, 39000, 40000, 41000, 43000, 45000]

REG_QUALITY = [
    ("Básico (20 pts)", 820, MUTED),
    ("Intermediário (21–55)", 1140, ORANGE),
    ("Avançado (56–90)", 1010, PURPLE),
    ("Completo (91–100)", 270, PINK),
]

AUDIENCE_MONETIZATION_SEGMENTS = {
    "Segmento": ["Novos usuários", "Recorrentes", "Reativados", "Assinantes"],
    "Sessões": [28400, 52200, 13400, 23000],
    "Conv. (%)": [1.2, 2.8, 4.1, 5.9],
    "Receita": [8400, 42600, 18200, 25000],
}


def safe_pct_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / previous * 100


def coerce_week_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "week_start" not in df.columns:
        return df
    out = df.copy()
    out["week_start"] = pd.to_datetime(out["week_start"])
    return out.sort_values("week_start").reset_index(drop=True)


def empty_state() -> None:
    st.info("Sem dados para este período")


def build_mock_query_data(selected_week_start: str) -> dict:
    rng = np.random.default_rng(42)
    week_range = pd.date_range(end=pd.to_datetime(selected_week_start), periods=8, freq="W-MON")
    channel_weeks = week_range[-5:]

    rev = [88400.0, 76200.0, 92100.0, 84600.0, 79800.0, 96300.0, 88700.0, 94200.0]
    rev_yoy = [r * rng.uniform(0.72, 0.86) for r in rev]
    trx = [int(r / rng.uniform(88, 116)) for r in rev]
    rev_pt = [r * rng.uniform(0.62, 0.72) for r in rev]
    rev_ass = [r - p for r, p in zip(rev, rev_pt)]
    revenue_weekly = pd.DataFrame({
        "week_start": week_range,
        "receita_total": rev,
        "transacoes": trx,
        "ticket_medio": [r / t for r, t in zip(rev, trx)],
        "receita_pontual": rev_pt,
        "receita_assinatura": rev_ass,
        "receita_total_yoy": rev_yoy,
    })

    arr_subscriptions = pd.DataFrame({
        "week_start": week_range,
        "arr_total": [472500, 478400, 481800, 486200, 489500, 495100, 490100, 498600],
        "nova_arr_semana": [3200, 4100, 5800, 3600, 4400, 6200, 3800, 4900],
        "taxa_renovacao_semana": [0.78, 0.82, 0.86, 0.81, 0.79, 0.84, 0.88, 0.836],
        "taxa_renovacao_12m": [0.814] * 8,
        "assinaturas_vencendo_30_dias": [118] * 8,
        "assinaturas_vencendo_60_dias": [204] * 8,
        "assinaturas_vencendo_90_dias": [337] * 8,
    })

    product_performance = pd.DataFrame([
        {"produto": "Produto A", "preco_produto": 89.99, "carrinhos_iniciados": 312, "carrinhos_concluidos": 198, "receita_estimada": 198 * 89.99},
        {"produto": "Produto B", "preco_produto": 39.95, "carrinhos_iniciados": 487, "carrinhos_concluidos": 362, "receita_estimada": 362 * 39.95},
        {"produto": "Produto C", "preco_produto": 330.00, "carrinhos_iniciados": 88, "carrinhos_concluidos": 41, "receita_estimada": 41 * 330.00},
        {"produto": "Produto D", "preco_produto": 69.29, "carrinhos_iniciados": 224, "carrinhos_concluidos": 142, "receita_estimada": 142 * 69.29},
        {"produto": "Produto E", "preco_produto": 69.87, "carrinhos_iniciados": 195, "carrinhos_concluidos": 114, "receita_estimada": 114 * 69.87},
        {"produto": "Produto F", "preco_produto": 39.95, "carrinhos_iniciados": 318, "carrinhos_concluidos": 253, "receita_estimada": 253 * 39.95},
        {"produto": "Produto G", "preco_produto": 59.93, "carrinhos_iniciados": 147, "carrinhos_concluidos": 88, "receita_estimada": 88 * 59.93},
        {"produto": "Produto H", "preco_produto": 69.29, "carrinhos_iniciados": 178, "carrinhos_concluidos": 109, "receita_estimada": 109 * 69.29},
    ])

    channel_base_revenue = [33200, 19400, 13800, 10100, 8600, 9100]
    channel_base_sessions = [44800, 11200, 17600, 9400, 5800, 5200]
    channel_factors = [0.86, 0.91, 0.96, 0.93, 1.00]
    channel_rows = []
    for week_date, factor in zip(channel_weeks, channel_factors):
        for channel, revenue, sessions in zip(CHS, channel_base_revenue, channel_base_sessions):
            week_factor = factor if week_date == channel_weeks[-1] else factor * rng.uniform(0.94, 1.07)
            channel_rows.append({
                "week_start": week_date,
                "canal": channel,
                "receita": round(revenue * week_factor, 2),
                "sessoes": int(round(sessions * week_factor)),
            })
    channel_revenue = pd.DataFrame(channel_rows)

    gsc_data = pd.DataFrame({
        "week_start": week_range,
        "impressoes": [1240000, 1180000, 1310000, 1290000, 1220000, 1380000, 1340000, 1410000],
        "cliques": [28400, 25100, 31200, 29800, 27600, 33100, 30800, 34200],
        "ctr": [0.0229, 0.0213, 0.0238, 0.0231, 0.0226, 0.0240, 0.0230, 0.0243],
        "posicao_media": [18.4, 18.9, 17.8, 17.6, 18.1, 17.2, 17.4, 16.9],
    })

    audience_weekly = pd.DataFrame({
        "week_start": week_range,
        "sessoes": [82400, 71200, 89600, 84100, 76800, 93400, 87400, 94000],
        "visitantes_unicos": [54100, 49200, 56300, 54800, 52100, 59800, 57200, 61200],
        "taxa_engajamento": [0.488, 0.476, 0.512, 0.503, 0.497, 0.521, 0.518, 0.524],
        "paginas_por_sessao": [3.3, 3.1, 3.5, 3.4, 3.2, 3.6, 3.5, 3.7],
        "sessoes_yoy": [65100, 53900, 69400, 66800, 60900, 77800, 72500, 78400],
    })

    audience_profile = pd.DataFrame([
        {"dimensao": "dim1", "segmento": "nao_cadastrados", "sessoes": 49200},
        {"dimensao": "dim1", "segmento": "cadastrados_nao_logados", "sessoes": 27400},
        {"dimensao": "dim1", "segmento": "cadastrados_logados", "sessoes": 17400},
        {"dimensao": "dim2", "segmento": "nunca_compraram", "sessoes": 44200},
        {"dimensao": "dim2", "segmento": "ja_compraram", "sessoes": 26800},
        {"dimensao": "dim2", "segmento": "assinantes_ativos", "sessoes": 23000},
        {"dimensao": "dim3", "segmento": "novos", "sessoes": 28400},
        {"dimensao": "dim3", "segmento": "recorrentes", "sessoes": 52200},
        {"dimensao": "dim3", "segmento": "reativados", "sessoes": 13400},
    ])

    registration_funnel = pd.DataFrame([
        {"etapa": "Visitantes não-logados", "contagem": 94000},
        {"etapa": "Encontraram barreira de cadastro", "contagem": 18700},
        {"etapa": "Acessaram página de login / cadastro", "contagem": 11400},
        {"etapa": "Iniciaram formulário", "contagem": 8900},
        {"etapa": "Cadastros efetivados", "contagem": 3240},
    ])

    registration_by_channel = pd.DataFrame([
        {"canal": "Orgânico", "cadastros": 1210, "score_medio": 64.2, "conversao_para_venda": 14.8},
        {"canal": "E-mail", "cadastros": 680, "score_medio": 71.8, "conversao_para_venda": 17.2},
        {"canal": "Direto", "cadastros": 540, "score_medio": 58.9, "conversao_para_venda": 13.6},
        {"canal": "Redes Sociais", "cadastros": 480, "score_medio": 52.3, "conversao_para_venda": 11.8},
        {"canal": "Pago", "cadastros": 220, "score_medio": 67.1, "conversao_para_venda": 15.9},
        {"canal": "Alertas", "cadastros": 110, "score_medio": 55.4, "conversao_para_venda": 12.4},
    ])

    registration_score_trend = pd.DataFrame({
        "week_start": week_range,
        "score_medio": [58.2, 59.8, 61.0, 59.4, 60.1, 61.8, 59.3, 62.4],
    })

    email_stats = pd.DataFrame([{
        "emails_enviados": 48200,
        "sessoes_geradas": 11200,
        "ctr": 0.0484,
        "receita_atribuida": 19400,
    }])

    alerts_stats = pd.DataFrame([{
        "alertas_enviados": 62400,
        "sessoes_geradas": 5200,
        "ctr": 0.0833,
        "receita_atribuida": 9100,
    }])

    checkout_funnel_traditional = pd.DataFrame([
        {"etapa": "Início (produto ao carrinho)", "carrinhos": 4820, "conversao_pct": None, "abandono_pct": None},
        {"etapa": "Escolha do meio de pagamento", "carrinhos": 3960, "conversao_pct": 82.2, "abandono_pct": 17.8},
        {"etapa": "Vitrine de upsell", "carrinhos": 3780, "conversao_pct": 95.5, "abandono_pct": 4.5},
        {"etapa": "Início do processamento", "carrinhos": 3540, "conversao_pct": 93.7, "abandono_pct": 6.3},
        {"etapa": "Carrinho concluído", "carrinhos": 3018, "conversao_pct": 85.3, "abandono_pct": 14.7},
    ])

    checkout_funnel_quick = pd.DataFrame([
        {"etapa": "Início (clique compra rápida)", "carrinhos": 2140, "conversao_pct": None, "abandono_pct": None},
        {"etapa": "Confirmação de login", "carrinhos": 1820, "conversao_pct": 85.0, "abandono_pct": 15.0},
        {"etapa": "Início do processamento", "carrinhos": 1710, "conversao_pct": 93.9, "abandono_pct": 6.1},
        {"etapa": "Concluída com sucesso", "carrinhos": 1490, "conversao_pct": 87.1, "abandono_pct": None},
        {"etapa": "Falha no processamento", "carrinhos": 220, "conversao_pct": 12.9, "abandono_pct": None},
        {"etapa": "Migração p/ carrinho trad.", "carrinhos": 96, "conversao_pct": 43.6, "abandono_pct": None},
    ])

    cart_recovery = pd.DataFrame([{
        "elegiveis": 1802,
        "mensagens_enviadas": 1540,
        "recuperados": 312,
        "taxa_recuperacao": 312 / 1802,
        "receita_recuperada": 312 * 84.6,
    }])

    payment_conversion = pd.DataFrame([
        {"meio_pagamento": "Cartão de Crédito", "concluidos_pct": 0.892, "abandono_pct": 0.108},
        {"meio_pagamento": "Pix", "concluidos_pct": 0.934, "abandono_pct": 0.066},
        {"meio_pagamento": "Boleto", "concluidos_pct": 0.761, "abandono_pct": 0.239},
        {"meio_pagamento": "Cartão de Débito", "concluidos_pct": 0.848, "abandono_pct": 0.152},
    ])

    upsell_vitrine = pd.DataFrame([{
        "taxa_adicao": 0.314,
        "impacto_ticket_medio": 18.60,
        "carrinhos_com_upsell": 948,
        "receita_incremental": 17633,
    }])

    conversion_by_segment = pd.DataFrame([
        {"segmentacao": "perfil_comercial", "segmento": "Novos compradores", "conversao_pct": 38.4},
        {"segmentacao": "perfil_comercial", "segmento": "Compradores recorrentes", "conversao_pct": 52.1},
        {"segmentacao": "perfil_comercial", "segmento": "Assinantes ativos", "conversao_pct": 61.8},
        {"segmentacao": "perfil_engajamento", "segmento": "Usuários novos no site", "conversao_pct": 28.2},
        {"segmentacao": "perfil_engajamento", "segmento": "Usuários recorrentes", "conversao_pct": 49.7},
        {"segmentacao": "perfil_engajamento", "segmento": "Usuários reativados", "conversao_pct": 64.3},
        {"segmentacao": "safra_cadastro", "segmento": "Cadastro 2026", "conversao_pct": 38.1},
        {"segmentacao": "safra_cadastro", "segmento": "Cadastro 2025", "conversao_pct": 44.8},
        {"segmentacao": "safra_cadastro", "segmento": "Cadastro 2024", "conversao_pct": 51.3},
        {"segmentacao": "safra_cadastro", "segmento": "Cadastro ≤ 2023", "conversao_pct": 58.9},
    ])

    return {
        "revenue_weekly": revenue_weekly,
        "arr_subscriptions": arr_subscriptions,
        "product_performance": product_performance,
        "channel_revenue": channel_revenue,
        "gsc_data": gsc_data,
        "email_stats": email_stats,
        "alerts_stats": alerts_stats,
        "audience_weekly": audience_weekly,
        "audience_profile": audience_profile,
        "registration_funnel": registration_funnel,
        "registration_by_channel": registration_by_channel,
        "registration_score_trend": registration_score_trend,
        "checkout_funnel_traditional": checkout_funnel_traditional,
        "checkout_funnel_quick": checkout_funnel_quick,
        "cart_recovery": cart_recovery,
        "payment_conversion": payment_conversion,
        "upsell_vitrine": upsell_vitrine,
        "conversion_by_segment": conversion_by_segment,
    }


def load_query_data(use_mock: bool, selected_week_start: str) -> dict:
    if use_mock:
        return build_mock_query_data(selected_week_start)

    return {
        "revenue_weekly": coerce_week_df(get_revenue_weekly(selected_week_start)),
        "arr_subscriptions": coerce_week_df(get_arr_subscriptions(selected_week_start)),
        "product_performance": get_product_performance(selected_week_start),
        "channel_revenue": coerce_week_df(get_channel_revenue(selected_week_start)),
        "gsc_data": coerce_week_df(get_gsc_data(selected_week_start)),
        "email_stats": get_email_stats(selected_week_start),
        "alerts_stats": get_alerts_stats(selected_week_start),
        "audience_weekly": coerce_week_df(get_audience_weekly(selected_week_start)),
        "audience_profile": get_audience_profile(selected_week_start),
        "registration_funnel": get_registration_funnel(selected_week_start),
        "registration_by_channel": get_registration_by_channel(selected_week_start),
        "registration_score_trend": coerce_week_df(get_registration_score_trend(selected_week_start)),
        "checkout_funnel_traditional": get_checkout_funnel_traditional(selected_week_start),
        "checkout_funnel_quick": get_checkout_funnel_quick(selected_week_start),
        "cart_recovery": get_cart_recovery(selected_week_start),
        "payment_conversion": get_payment_conversion(selected_week_start),
        "upsell_vitrine": get_upsell_vitrine(selected_week_start),
        "conversion_by_segment": get_conversion_by_segment(selected_week_start),
    }

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0 10px 0;">
      <h1 style="color:{SIDEBAR_TEXT}; margin:0; letter-spacing:0.02em;">Receita 360</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;color:{rgba(SIDEBAR_TEXT, 0.72)};text-transform:uppercase;"
                f"letter-spacing:.08em;margin-bottom:6px;'>Semana de referência</div>",
                unsafe_allow_html=True)
    week_sel = st.selectbox(
        "Semana de referência",
        WEEKS,
        index=len(WEEKS) - 1,
        label_visibility="collapsed",
    )

    use_mock = st.toggle(
        "Modo mock (sem Redshift)",
        value=True,
        help="Desative para buscar dados do Redshift usando `.streamlit/secrets.toml`.",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;color:{rgba(SIDEBAR_TEXT, 0.72)};text-transform:uppercase;"
                f"letter-spacing:.08em;margin-bottom:6px;'>Comparação</div>",
                unsafe_allow_html=True)
    compare = st.radio(
        "Comparação",
        ["4 semanas anteriores", "Ano anterior (YoY)", "Ambos"],
        index=2,
        label_visibility="collapsed",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Status bullets
    st.markdown(f"""
    <div class="sidebar-panel">
      <div class="sidebar-kicker">Status da semana</div>
      <div class="status-row">
        <div class="status-dot" style="background:{GREEN};"></div>
        <div class="status-text">Receita <b>+6,2%</b> vs meta</div>
      </div>
      <div class="status-row">
        <div class="status-dot" style="background:{ORANGE};"></div>
        <div class="status-text">Renovações abaixo da média</div>
      </div>
      <div class="status-row">
        <div class="status-dot" style="background:{PURPLE};"></div>
        <div class="status-text">Score de cadastros crescendo</div>
      </div>
      <div class="status-row">
        <div class="status-dot" style="background:{PINK};"></div>
        <div class="status-text">Compra rápida com menos falhas</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10.5px;color:{rgba(SIDEBAR_TEXT, 0.72)};text-align:center;'>"
                f"Atualizado em {TODAY.strftime('%d/%m/%Y')}</div>",
                unsafe_allow_html=True)


USE_MOCK_DATA = use_mock
selected_week_start = WEEK_SELECTION_TO_START[week_sel]
query_data = load_query_data(USE_MOCK_DATA, selected_week_start)

revenue_weekly_df = coerce_week_df(query_data["revenue_weekly"])
arr_subscriptions_df = coerce_week_df(query_data["arr_subscriptions"])
product_performance_df = query_data["product_performance"].copy()
channel_revenue_df = coerce_week_df(query_data["channel_revenue"])
gsc_data_df = coerce_week_df(query_data["gsc_data"])
email_stats_df = query_data["email_stats"].copy()
alerts_stats_df = query_data["alerts_stats"].copy()
audience_weekly_df = coerce_week_df(query_data["audience_weekly"])
audience_profile_df = query_data["audience_profile"].copy()
registration_funnel_df = query_data["registration_funnel"].copy()
registration_by_channel_df = query_data["registration_by_channel"].copy()
registration_score_trend_df = coerce_week_df(query_data["registration_score_trend"])
checkout_funnel_traditional_df = query_data["checkout_funnel_traditional"].copy()
checkout_funnel_quick_df = query_data["checkout_funnel_quick"].copy()
cart_recovery_df = query_data["cart_recovery"].copy()
payment_conversion_df = query_data["payment_conversion"].copy()
upsell_vitrine_df = query_data["upsell_vitrine"].copy()
conversion_by_segment_df = query_data["conversion_by_segment"].copy()


def numeric_list(df: pd.DataFrame, column: str) -> list[float]:
    if df.empty or column not in df.columns:
        return []
    return pd.to_numeric(df[column], errors="coerce").fillna(0).tolist()


def week_labels(df: pd.DataFrame) -> list[str]:
    if df.empty or "week_start" not in df.columns:
        return WEEKS
    return pd.to_datetime(df["week_start"]).dt.strftime("%d/%m").tolist()


def normalize_ratio(value: float | None) -> float | None:
    if value is None or pd.isna(value):
        return None
    value = float(value)
    return value / 100 if value > 1 else value


revenue_labels = week_labels(revenue_weekly_df)
rev = numeric_list(revenue_weekly_df, "receita_total")
rev_yoy = numeric_list(revenue_weekly_df, "receita_total_yoy")
trx = numeric_list(revenue_weekly_df, "transacoes")
ticket = numeric_list(revenue_weekly_df, "ticket_medio")
rev_pt = numeric_list(revenue_weekly_df, "receita_pontual")
rev_ass = numeric_list(revenue_weekly_df, "receita_assinatura")
REV_CW = rev[-1] if rev else None
REV_PW = rev[-2] if len(rev) > 1 else None
TRX_CW = trx[-1] if trx else None
TRX_PW = trx[-2] if len(trx) > 1 else None
TK_CW = ticket[-1] if ticket else None
TK_PW = ticket[-2] if len(ticket) > 1 else None

renew_labels = week_labels(arr_subscriptions_df)
arr_total = numeric_list(arr_subscriptions_df, "arr_total")
new_arr = numeric_list(arr_subscriptions_df, "nova_arr_semana")
renew_trend = [normalize_ratio(v) or 0 for v in numeric_list(arr_subscriptions_df, "taxa_renovacao_semana")]
ARR = arr_total[-1] if arr_total else None
ARR_PW = arr_total[-2] if len(arr_total) > 1 else None
RENEW_WEEK = renew_trend[-1] if renew_trend else None
RENEW_12M = (
    normalize_ratio(pd.to_numeric(arr_subscriptions_df["taxa_renovacao_12m"], errors="coerce").fillna(0).iloc[-1])
    if not arr_subscriptions_df.empty and "taxa_renovacao_12m" in arr_subscriptions_df.columns
    else None
)
SUBS_VENCE = {
    "30d": int(pd.to_numeric(arr_subscriptions_df["assinaturas_vencendo_30_dias"], errors="coerce").fillna(0).iloc[-1])
    if not arr_subscriptions_df.empty and "assinaturas_vencendo_30_dias" in arr_subscriptions_df.columns else 0,
    "60d": int(pd.to_numeric(arr_subscriptions_df["assinaturas_vencendo_60_dias"], errors="coerce").fillna(0).iloc[-1])
    if not arr_subscriptions_df.empty and "assinaturas_vencendo_60_dias" in arr_subscriptions_df.columns else 0,
    "90d": int(pd.to_numeric(arr_subscriptions_df["assinaturas_vencendo_90_dias"], errors="coerce").fillna(0).iloc[-1])
    if not arr_subscriptions_df.empty and "assinaturas_vencendo_90_dias" in arr_subscriptions_df.columns else 0,
}

if not product_performance_df.empty:
    df_prods = product_performance_df.rename(columns={
        "produto": "name",
        "preco_produto": "price",
        "carrinhos_iniciados": "ini",
        "carrinhos_concluidos": "conc",
        "receita_estimada": "receita",
    }).copy()
    for col in ["price", "ini", "conc", "receita"]:
        df_prods[col] = pd.to_numeric(df_prods[col], errors="coerce").fillna(0)
    df_prods["conv"] = np.where(df_prods["ini"] > 0, df_prods["conc"] / df_prods["ini"], 0)
    df_prods = df_prods.sort_values("receita", ascending=False).reset_index(drop=True)
    PRODS = df_prods.to_dict("records")
else:
    df_prods = pd.DataFrame(columns=["name", "price", "ini", "conc", "receita", "conv"])
    PRODS = []

if not channel_revenue_df.empty:
    channel_revenue_df["receita"] = pd.to_numeric(channel_revenue_df["receita"], errors="coerce").fillna(0)
    channel_revenue_df["sessoes"] = pd.to_numeric(channel_revenue_df["sessoes"], errors="coerce").fillna(0)
    channel_latest_week = channel_revenue_df["week_start"].max()
    latest_channels = channel_revenue_df[channel_revenue_df["week_start"] == channel_latest_week].set_index("canal")
    channel_weeks_sorted = sorted(channel_revenue_df["week_start"].unique())
    prev_channels = pd.DataFrame(columns=channel_revenue_df.columns)
    if len(channel_weeks_sorted) > 1:
        prev_week = channel_weeks_sorted[-2]
        prev_channels = channel_revenue_df[channel_revenue_df["week_start"] == prev_week].set_index("canal")
    latest_channels = latest_channels.reindex(CHS, fill_value=0)
    prev_channels = prev_channels.reindex(CHS, fill_value=0)
    ch_rev = latest_channels["receita"].tolist()
    ch_sess = latest_channels["sessoes"].tolist()
    ch_conv = [((r / s) * 100) if s else 0 for r, s in zip(ch_rev, ch_sess)]
    ch_deltas = [
        safe_pct_change(curr, prev)
        for curr, prev in zip(ch_rev, prev_channels.get("receita", pd.Series(index=CHS, dtype=float)).tolist())
    ]
else:
    ch_rev = []
    ch_sess = []
    ch_conv = []
    ch_deltas = []

audience_labels = week_labels(audience_weekly_df)
sess_wk = numeric_list(audience_weekly_df, "sessoes")
sess_yoy = numeric_list(audience_weekly_df, "sessoes_yoy")
uv_wk = numeric_list(audience_weekly_df, "visitantes_unicos")
eng_wk = [normalize_ratio(v) or 0 for v in numeric_list(audience_weekly_df, "taxa_engajamento")]
ppg_wk = numeric_list(audience_weekly_df, "paginas_por_sessao")
SESS_CW = sess_wk[-1] if sess_wk else None
SESS_PW = sess_wk[-2] if len(sess_wk) > 1 else None
UV_CW = uv_wk[-1] if uv_wk else None
ENG_RATE = eng_wk[-1] if eng_wk else None
PPG = ppg_wk[-1] if ppg_wk else None

gsc_labels = week_labels(gsc_data_df)
gsc_imp = numeric_list(gsc_data_df, "impressoes")
gsc_clk = numeric_list(gsc_data_df, "cliques")
gsc_pos = numeric_list(gsc_data_df, "posicao_media")
gsc_ctr = [((c / i) * 100) if i else 0 for c, i in zip(gsc_clk, gsc_imp)]

REG_FUNNEL = []
if not registration_funnel_df.empty:
    registration_funnel_df["contagem"] = pd.to_numeric(registration_funnel_df["contagem"], errors="coerce").fillna(0)
    counts = registration_funnel_df["contagem"].tolist()
    steps = registration_funnel_df["etapa"].tolist()
    for idx, (label, val) in enumerate(zip(steps, counts)):
        prev_val = counts[idx - 1] if idx > 0 else None
        conv = (val / prev_val * 100) if prev_val else None
        REG_FUNNEL.append((label, int(val), conv))

registration_by_channel_df["cadastros"] = pd.to_numeric(
    registration_by_channel_df.get("cadastros", pd.Series(dtype=float)),
    errors="coerce",
).fillna(0)
if "canal" not in registration_by_channel_df.columns:
    registration_by_channel_df["canal"] = pd.Series(dtype=object)
registration_by_channel_df["score_medio"] = pd.to_numeric(
    registration_by_channel_df.get("score_medio", pd.Series(dtype=float)),
    errors="coerce",
).fillna(0)
registration_by_channel_df["conversao_para_venda"] = pd.to_numeric(
    registration_by_channel_df.get("conversao_para_venda", pd.Series(dtype=float)),
    errors="coerce",
).fillna(0)
REG_CH = list(registration_by_channel_df[["canal", "cadastros", "score_medio", "conversao_para_venda"]].itertuples(index=False, name=None))
REG_SCORE = (
    float(np.average(registration_by_channel_df["score_medio"], weights=registration_by_channel_df["cadastros"]))
    if not registration_by_channel_df.empty and registration_by_channel_df["cadastros"].sum() > 0 else None
)
REG_SCORE_TREND = numeric_list(registration_score_trend_df, "score_medio")
score_trend = REG_SCORE_TREND

CART_TRAD = []
if not checkout_funnel_traditional_df.empty:
    checkout_funnel_traditional_df["carrinhos"] = pd.to_numeric(checkout_funnel_traditional_df["carrinhos"], errors="coerce").fillna(0)
    checkout_funnel_traditional_df["conversao_pct"] = pd.to_numeric(checkout_funnel_traditional_df["conversao_pct"], errors="coerce")
    checkout_funnel_traditional_df["abandono_pct"] = pd.to_numeric(checkout_funnel_traditional_df["abandono_pct"], errors="coerce")
    CART_TRAD = [
        (
            row.etapa,
            int(row.carrinhos),
            float(row.conversao_pct) if pd.notna(row.conversao_pct) else None,
            float(row.abandono_pct) if pd.notna(row.abandono_pct) else None,
        )
        for row in checkout_funnel_traditional_df.itertuples(index=False)
    ]

CART_QUICK = []
if not checkout_funnel_quick_df.empty:
    checkout_funnel_quick_df["carrinhos"] = pd.to_numeric(checkout_funnel_quick_df["carrinhos"], errors="coerce").fillna(0)
    checkout_funnel_quick_df["conversao_pct"] = pd.to_numeric(checkout_funnel_quick_df["conversao_pct"], errors="coerce")
    checkout_funnel_quick_df["abandono_pct"] = pd.to_numeric(checkout_funnel_quick_df["abandono_pct"], errors="coerce")
    CART_QUICK = [
        (
            row.etapa,
            int(row.carrinhos),
            float(row.conversao_pct) if pd.notna(row.conversao_pct) else None,
            float(row.abandono_pct) if pd.notna(row.abandono_pct) else None,
        )
        for row in checkout_funnel_quick_df.itertuples(index=False)
    ]

CART_CONV_TRAD = (CART_TRAD[-1][1] / CART_TRAD[0][1]) if len(CART_TRAD) >= 2 and CART_TRAD[0][1] else None
CART_CONV_QUICK = (CART_QUICK[3][1] / CART_QUICK[0][1]) if len(CART_QUICK) >= 4 and CART_QUICK[0][1] else None

PAYMENTS = []
if not payment_conversion_df.empty:
    payment_conversion_df["concluidos_pct"] = pd.to_numeric(payment_conversion_df["concluidos_pct"], errors="coerce").fillna(0)
    payment_conversion_df["abandono_pct"] = pd.to_numeric(payment_conversion_df["abandono_pct"], errors="coerce").fillna(0)
    PAYMENTS = [
        (
            row.meio_pagamento,
            0,
            normalize_ratio(row.concluidos_pct) or 0,
            normalize_ratio(row.abandono_pct) or 0,
        )
        for row in payment_conversion_df.itertuples(index=False)
    ]

ABAND_ELIG = MSGS_SENT = RECOVERED = 0
REC_RATE = REC_REV = None
if not cart_recovery_df.empty:
    recovery_row = cart_recovery_df.iloc[0]
    ABAND_ELIG = int(pd.to_numeric(recovery_row.get("elegiveis"), errors="coerce") or 0)
    MSGS_SENT = int(pd.to_numeric(recovery_row.get("mensagens_enviadas"), errors="coerce") or 0)
    RECOVERED = int(pd.to_numeric(recovery_row.get("recuperados"), errors="coerce") or 0)
    REC_RATE = normalize_ratio(pd.to_numeric(recovery_row.get("taxa_recuperacao"), errors="coerce"))
    REC_REV = float(pd.to_numeric(recovery_row.get("receita_recuperada"), errors="coerce") or 0)

UPSELL_ROW = upsell_vitrine_df.iloc[0] if not upsell_vitrine_df.empty else pd.Series(dtype=object)

EMAIL_ROW = email_stats_df.iloc[0] if not email_stats_df.empty else pd.Series(dtype=object)
ALERTS_ROW = alerts_stats_df.iloc[0] if not alerts_stats_df.empty else pd.Series(dtype=object)


# ═══════════════════════════════════════════════════════════════
#  PAGE HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-card">
  <div class="hero-kicker">Painel executivo</div>
  <div class="hero-title">
    Dashboard semanal de receita e conversão
  </div>
  <div class="hero-meta">
    Semana de referência:
    <span class="mono" style="color:{TEXT};">{week_sel}</span>
    &nbsp;·&nbsp;
    Gerado em {fmt_date_pt_br(TODAY)}
  </div>
</div>
""", unsafe_allow_html=True)

hero_chips = [
    context_chip(
        "Modo de dados",
        "Mock para navegação completa" if USE_MOCK_DATA else "Conectado",
        tone="alert" if USE_MOCK_DATA else "good",
        dot_color=ORANGE if USE_MOCK_DATA else GREEN,
    ),
]
st.markdown(f'<div class="context-strip">{"".join(hero_chips)}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💰  Receita",
    "📡  Canais",
    "👥  Audiência",
    "📝  Cadastros",
    "🛒  Checkout",
    "🔮  Forecast",
])


# ───────────────────────────────────────────────────────────────
#  TAB 1 — RECEITA
# ───────────────────────────────────────────────────────────────
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    drev = safe_pct_change(REV_CW, REV_PW)
    dtrx = safe_pct_change(TRX_CW, TRX_PW)
    dtk = safe_pct_change(TK_CW, TK_PW)
    darr = safe_pct_change(ARR, ARR_PW)
    with c1: st.markdown(kpi("Receita Total", fmt_brl(REV_CW) if REV_CW is not None else "—", drev, accent=PINK), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Transações", f"{int(TRX_CW):,}" if TRX_CW is not None else "—", dtrx, accent=PURPLE), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Ticket Médio", fmt_brl(TK_CW) if TK_CW is not None else "—", dtk, accent=ORANGE), unsafe_allow_html=True)
    with c4: st.markdown(kpi("ARR Total", fmt_brl(ARR) if ARR is not None else "—", darr, accent=PURPLE), unsafe_allow_html=True)

    spacer()

    # Revenue trend + Mix
    ca, cb = st.columns([3, 1])

    with ca:
        section(f"Receita sobe para {fmt_brl(REV_CW)} na semana" if REV_CW is not None else "Receita semanal")
        if revenue_weekly_df.empty:
            empty_state()
        else:
            takeaway(
                f"<strong>Takeaway:</strong> a receita avançou <strong>{drev:.1f}% vs semana anterior</strong> "
                f"e segue acima do comparativo YoY, com 2026 visualmente enfatizado.",
                "good" if (drev or 0) >= 0 else "alert",
            )
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=revenue_labels, y=rev_yoy, name="2025",
                marker_color=TRACK_STRONG,
                hovertemplate="%{y:,.0f}<extra>2025</extra>",
            ))
            fig.add_trace(go.Scatter(
                x=revenue_labels, y=rev, name="2026",
                mode="lines+markers",
                line=dict(color=PINK, width=2.5),
                marker=dict(size=7, color=PINK, line=dict(color=CARD, width=1.5)),
                fill="tonexty", fillcolor=PINK_SOFT,
                hovertemplate="R$ %{y:,.0f}<extra>2026</extra>",
            ))
            fig.update_layout(**plotly_layout(height=265, barmode="overlay"))
            fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
            st.plotly_chart(fig, width="stretch", config=cfg)

    with cb:
        section("Mix da receita")
        if revenue_weekly_df.empty or REV_CW in (None, 0):
            empty_state()
        else:
            mix_labels = ["Pontual", "Assinatura"]
            mix_values = [rev_pt[-1], rev_ass[-1]]
            mix_share = [value / REV_CW * 100 for value in mix_values]
            section(f"{mix_labels[int(np.argmax(mix_values))]} domina o mix da receita")
            takeaway(
                f"<strong>Takeaway:</strong> {mix_labels[0]} responde por <strong>{mix_share[0]:.0f}% da receita</strong>, "
                f"enquanto {mix_labels[1].lower()} representa <strong>{mix_share[1]:.0f}%</strong>.",
                "accent",
            )
            fig_mix = go.Figure(go.Bar(
                x=mix_share,
                y=mix_labels,
                orientation="h",
                marker_color=[PINK, PURPLE],
                text=[f"{share:.0f}% · {fmt_brl(value)}" for share, value in zip(mix_share, mix_values)],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=10, color=TEXT),
                hovertemplate="%{y}: %{x:.1f}%<br>Receita: %{customdata}<extra></extra>",
                customdata=[fmt_brl(value) for value in mix_values],
            ))
            fig_mix.update_layout(**plotly_layout(height=265, showlegend=False, margin=dict(l=10, r=10, t=20, b=10)))
            fig_mix.update_xaxes(ticksuffix="%", showgrid=False, visible=False, range=[0, max(mix_share) * 1.35])
            fig_mix.update_yaxes(showgrid=False)
            st.plotly_chart(fig_mix, width="stretch", config=cfg)

    # Product table + Subscriptions
    col_p, col_s = st.columns([2, 1])

    with col_p:
        section("Performance por produto — semana atual")
        if df_prods.empty:
            empty_state()
        else:
            rows = ""
            for _, r in df_prods.iterrows():
                cv = r["conv"] * 100
                if cv >= 70:
                    badge = f'<span class="bg">{cv:.1f}%</span>'
                elif cv < 55:
                    badge = f'<span class="bo">{cv:.1f}%</span>'
                else:
                    badge = f'<span class="bp">{cv:.1f}%</span>'
                rows += (f"<tr><td>{r['name']}</td>"
                         f"<td class='mono'>{fmt_brl(r['price'])}</td>"
                         f"<td class='mono'>{int(r['ini']):,}</td>"
                         f"<td class='mono'>{int(r['conc']):,}</td>"
                         f"<td>{badge}</td>"
                         f"<td class='mono'><b>{fmt_brl(r['receita'])}</b></td></tr>")
            st.markdown(f"""
            <table class="dtable">
              <thead><tr>
                <th>Produto</th><th>Preço</th><th>Iniciados</th>
                <th>Concluídos</th><th>Conversão</th><th>Receita Est.</th>
              </tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)

    with col_s:
        section("Assinaturas")
        if arr_subscriptions_df.empty:
            empty_state()
        else:
            subs_items = [
                ("Nova ARR (média 4 sem.)", fmt_brl(sum(new_arr[-4:]) / min(len(new_arr), 4)), TEXT),
                ("Taxa de renovação (sem.)", f"{(RENEW_WEEK or 0) * 100:.1f}%",
                 GREEN if (RENEW_WEEK or 0) >= 0.82 else ORANGE),
                ("Taxa renovação acum. 12m", f"{(RENEW_12M or 0) * 100:.1f}%", TEXT),
                ("Venc. próx. 30 dias", str(SUBS_VENCE["30d"]), ORANGE),
                ("Venc. próx. 60 dias", str(SUBS_VENCE["60d"]), ORANGE),
                ("Venc. próx. 90 dias", str(SUBS_VENCE["90d"]), MUTED),
            ]
            for lbl, val, color in subs_items:
                st.markdown(f"""<div class="band">
                  <div class="band-label">{lbl}</div>
                  <div class="band-val" style="color:{color};">{val}</div>
                </div>""", unsafe_allow_html=True)

            fig_ren = go.Figure(go.Scatter(
                x=renew_labels, y=[r * 100 for r in renew_trend],
                mode="lines+markers",
                line=dict(color=PURPLE, width=2),
                marker=dict(size=5, color=PURPLE),
                fill="tozeroy", fillcolor=PURPLE_SOFT,
                hovertemplate="%{y:.1f}%<extra></extra>",
            ))
            fig_ren.add_hline(y=(RENEW_12M or 0) * 100, line_dash="dot", line_color=MUTED,
                              annotation_text="média 12m",
                              annotation_font_color=MUTED, annotation_font_size=10)
            fig_ren.update_layout(**plotly_layout(height=165, showlegend=False))
            fig_ren.update_yaxes(ticksuffix="%", range=[65, 100])
            st.plotly_chart(fig_ren, width="stretch", config=cfg)

    section("Recompra — perfil do comprador na semana")
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(kpi("Novos compradores",       "38,4%", -2.1, accent=ORANGE), unsafe_allow_html=True)
    with r2: st.markdown(kpi("Compradores recorrentes", "61,6%",  2.1, accent=GREEN),  unsafe_allow_html=True)
    with r3: st.markdown(kpi("Retorno (últimas 4 sem.)", "74,2%",  0.8, accent=PURPLE),unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
#  TAB 2 — CANAIS
# ───────────────────────────────────────────────────────────────
with tab2:
    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1: st.markdown(kpi("Receita — Orgânico", fmt_brl(ch_rev[0]) if len(ch_rev) > 0 else "—", ch_deltas[0] if len(ch_deltas) > 0 else None, accent=PURPLE), unsafe_allow_html=True)
    with kc2: st.markdown(kpi("Receita — E-mail", fmt_brl(ch_rev[1]) if len(ch_rev) > 1 else "—", ch_deltas[1] if len(ch_deltas) > 1 else None, accent=PINK), unsafe_allow_html=True)
    with kc3: st.markdown(kpi("Receita — Direto", fmt_brl(ch_rev[2]) if len(ch_rev) > 2 else "—", ch_deltas[2] if len(ch_deltas) > 2 else None, accent=ORANGE), unsafe_allow_html=True)
    with kc4: st.markdown(kpi("Receita — Alertas", fmt_brl(ch_rev[5]) if len(ch_rev) > 5 else "—", ch_deltas[5] if len(ch_deltas) > 5 else None, accent=PURPLE), unsafe_allow_html=True)

    spacer()

    cb1, cb2 = st.columns([2, 1])
    with cb1:
        section("Quais canais mais trazem receita")
        if channel_revenue_df.empty:
            empty_state()
        else:
            top_channel = CHS[int(np.argmax(ch_rev))]
            section(f"Quais canais mais trazem receita: {top_channel} lidera a semana")
            takeaway(
                f"<strong>Takeaway:</strong> {top_channel} concentra a maior receita da semana, "
                f"enquanto o gráfico mantém os demais canais como comparação secundária.",
                "accent",
            )
            fig_chr = go.Figure(go.Bar(
                x=CHS, y=ch_rev,
                marker_color=CHS_PAL,
                text=[fmt_brl(r) for r in ch_rev],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=10, color=TEXT),
                hovertemplate="%{x}: R$ %{y:,.0f}<extra></extra>",
            ))
            fig_chr.update_layout(**plotly_layout(
                height=270,
                bargap=0.35,
                yaxis=dict(visible=False),
            ))
            st.plotly_chart(fig_chr, width="stretch", config=cfg)

    with cb2:
        section("Eficiência por canal (R$/sessão)")
        if channel_revenue_df.empty:
            empty_state()
        else:
            takeaway(
                "<strong>Takeaway:</strong> este indicador mostra monetização por sessão, então ajuda a separar "
                "volume de tráfego de qualidade econômica do canal.",
                "accent",
            )
            fig_ccv = go.Figure(go.Bar(
                x=ch_conv, y=CHS,
                orientation="h",
                marker=dict(
                    color=ch_conv,
                    colorscale=[[0, PURPLE], [0.5, PINK], [1, ORANGE]],
                    showscale=False,
                ),
                text=[f"{c:.2f}%" for c in ch_conv],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=10, color=TEXT),
                hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
            ))
            fig_ccv.update_layout(**plotly_layout(
                height=270,
                xaxis=dict(visible=False),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            ))
            st.plotly_chart(fig_ccv, width="stretch", config=cfg)

    section("Onde vale aprofundar por canal")
    if channel_revenue_df.empty:
        empty_state()
    else:
        rows = ""
        for ch, rev_v, sess, conv, delta_v in zip(CHS, ch_rev, ch_sess, ch_conv, ch_deltas):
            if delta_v is None:
                badge = '<span class="bp">—</span>'
            else:
                badge = (f'<span class="bg">▲ {delta_v:.1f}%</span>' if delta_v > 0
                         else f'<span class="bo">▼ {abs(delta_v):.1f}%</span>')
            rows += (f"<tr><td><b>{ch}</b></td>"
                     f"<td class='mono'>{fmt_brl(rev_v)}</td>"
                     f"<td class='mono'>{fmt_k(sess)}</td>"
                     f"<td class='mono'>{conv:.2f}%</td>"
                     f"<td>{badge}</td></tr>")
        st.markdown(f"""
        <table class="dtable">
          <thead><tr>
            <th>Canal</th><th>Receita</th><th>Sessões</th>
            <th>Eficiência (R$/Sessão)</th><th>vs Sem. Ant.</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    spacer()
    section("O que os canais próprios entregam")
    takeaway(
        "<strong>Takeaway:</strong> os canais próprios aparecem separados porque ajudam a ler retenção e reativação, "
        "não apenas aquisição bruta.",
        "good",
    )

    ce1, ce2 = st.columns(2)
    with ce1:
        section("E-mail marketing")
        if email_stats_df.empty:
            empty_state()
        else:
            email_items = [
                ("Emails enviados", f"{int(pd.to_numeric(EMAIL_ROW.get('emails_enviados'), errors='coerce') or 0):,}".replace(",", ".")),
                ("Sessões geradas", f"{int(pd.to_numeric(EMAIL_ROW.get('sessoes_geradas'), errors='coerce') or 0):,}".replace(",", ".")),
                ("CTR médio", f"{(normalize_ratio(pd.to_numeric(EMAIL_ROW.get('ctr'), errors='coerce')) or 0) * 100:.2f}%".replace(".", ",")),
                ("Receita atribuída", fmt_brl(float(pd.to_numeric(EMAIL_ROW.get('receita_atribuida'), errors='coerce') or 0))),
            ]
            for lbl, val in email_items:
                st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                            f'<div class="band-val">{val}</div></div>', unsafe_allow_html=True)

    with ce2:
        section("Alertas de trânsitos")
        if alerts_stats_df.empty:
            empty_state()
        else:
            alerts_items = [
                ("Alertas enviados", f"{int(pd.to_numeric(ALERTS_ROW.get('alertas_enviados'), errors='coerce') or 0):,}".replace(",", ".")),
                ("Sessões geradas", f"{int(pd.to_numeric(ALERTS_ROW.get('sessoes_geradas'), errors='coerce') or 0):,}".replace(",", ".")),
                ("CTR médio", f"{(normalize_ratio(pd.to_numeric(ALERTS_ROW.get('ctr'), errors='coerce')) or 0) * 100:.2f}%".replace(".", ",")),
                ("Receita atribuída", fmt_brl(float(pd.to_numeric(ALERTS_ROW.get('receita_atribuida'), errors='coerce') or 0))),
            ]
            for lbl, val in alerts_items:
                st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                            f'<div class="band-val">{val}</div></div>', unsafe_allow_html=True)

    spacer()
    section("Descoberta orgânica — como está o topo do funil")
    cg1, cg2 = st.columns(2)
    with cg1:
        if gsc_data_df.empty:
            empty_state()
        else:
            takeaway(
                f"<strong>Takeaway:</strong> impressões chegaram a <strong>{fmt_k(gsc_imp[-1])}</strong> e cliques a "
                f"<strong>{fmt_k(gsc_clk[-1])}</strong>, reforçando a tendência de ganho orgânico.",
                "good",
            )
            fig_gsc = go.Figure()
            fig_gsc.add_trace(go.Scatter(
                x=gsc_labels, y=gsc_imp, name="Impressões",
                mode="lines+markers",
                line=dict(color=PURPLE, width=2),
                marker=dict(size=5),
                yaxis="y",
            ))
            fig_gsc.add_trace(go.Scatter(
                x=gsc_labels, y=gsc_clk, name="Cliques",
                mode="lines+markers",
                line=dict(color=PINK, width=2),
                marker=dict(size=5),
                yaxis="y2",
            ))
            layout2 = plotly_layout(
                height=230,
                yaxis=dict(title=dict(text="Impressões", font=dict(size=11, color=MUTED)), tickformat=",.0f"),
                yaxis2=dict(
                    title=dict(text="Cliques", font=dict(size=11, color=MUTED)),
                    overlaying="y",
                    side="right",
                    gridcolor="rgba(0,0,0,0)",
                    tickformat=",.0f",
                    linecolor=BORDER,
                    tickfont=dict(size=11, color=MUTED),
                ),
            )
            fig_gsc.update_layout(**layout2)
            st.plotly_chart(fig_gsc, width="stretch", config=cfg)

    with cg2:
        if gsc_data_df.empty:
            empty_state()
        else:
            fig_pos = go.Figure(go.Scatter(
                x=gsc_labels, y=gsc_pos,
                mode="lines+markers",
                line=dict(color=ORANGE, width=2.5),
                marker=dict(size=6, color=ORANGE),
                fill="tozeroy", fillcolor=ORANGE_SOFT,
                hovertemplate="Posição %{y:.1f}<extra></extra>",
            ))
            fig_pos.update_layout(**plotly_layout(
                height=230,
                showlegend=False,
                title=dict(
                    text="Posição média — quanto menor, melhor",
                    font=dict(size=11, color=MUTED),
                ),
            ))
            fig_pos.update_yaxes(autorange="reversed", title="Posição média")
            st.plotly_chart(fig_pos, width="stretch", config=cfg)


# ───────────────────────────────────────────────────────────────
#  TAB 3 — AUDIÊNCIA
# ───────────────────────────────────────────────────────────────
with tab3:
    ka1, ka2, ka3, ka4 = st.columns(4)
    dsess = safe_pct_change(SESS_CW, SESS_PW)
    uv_delta = safe_pct_change(UV_CW, uv_wk[-2] if len(uv_wk) > 1 else None)
    eng_delta = safe_pct_change(ENG_RATE, eng_wk[-2] if len(eng_wk) > 1 else None)
    ppg_delta = safe_pct_change(PPG, ppg_wk[-2] if len(ppg_wk) > 1 else None)
    with ka1: st.markdown(kpi("Sessões", fmt_k(SESS_CW) if SESS_CW is not None else "—", dsess, accent=PURPLE), unsafe_allow_html=True)
    with ka2: st.markdown(kpi("Unique Visitors", fmt_k(UV_CW) if UV_CW is not None else "—", uv_delta, accent=PINK), unsafe_allow_html=True)
    with ka3: st.markdown(kpi("Taxa de Engajamento", f"{(ENG_RATE or 0) * 100:.1f}%" if ENG_RATE is not None else "—", eng_delta, accent=ORANGE), unsafe_allow_html=True)
    with ka4: st.markdown(kpi("Páginas / Sessão", f"{PPG:.1f}" if PPG is not None else "—", ppg_delta, accent=PURPLE), unsafe_allow_html=True)

    spacer()

    ca1, ca2 = st.columns([3, 1])
    with ca1:
        section(f"Sessões crescem para {fmt_k(SESS_CW)} na semana" if SESS_CW is not None else "Sessões na semana")
        if audience_weekly_df.empty:
            empty_state()
        else:
            takeaway(
                f"<strong>Takeaway:</strong> o volume avançou <strong>{dsess:.1f}% vs semana anterior</strong> "
                f"e a linha de 2026 foi destacada para acelerar a leitura.",
                "good" if (dsess or 0) >= 0 else "alert",
            )
            fig_sess = go.Figure()
            fig_sess.add_trace(go.Bar(
                x=audience_labels, y=sess_yoy, name="2025",
                marker_color=TRACK_STRONG,
            ))
            fig_sess.add_trace(go.Scatter(
                x=audience_labels, y=sess_wk, name="2026",
                mode="lines+markers",
                line=dict(color=PURPLE, width=2.5),
                marker=dict(size=7, color=PURPLE, line=dict(color=CARD, width=1.5)),
                hovertemplate="%{y:,.0f}<extra>2026</extra>",
            ))
            fig_sess.update_layout(**plotly_layout(height=265, barmode="overlay"))
            fig_sess.update_yaxes(tickformat=",")
            st.plotly_chart(fig_sess, width="stretch", config=cfg)

    with ca2:
        if channel_revenue_df.empty:
            section("Audiência por canal")
            empty_state()
        else:
            sess_sorted = sorted(zip(CHS, ch_sess, CHS_PAL), key=lambda item: item[1], reverse=True)
            top_aud = sess_sorted[0][0]
            total_sess = sum(ch_sess)
            section(f"{top_aud} concentra a maior audiência")
            takeaway(
                f"<strong>Takeaway:</strong> {top_aud} representa <strong>{sess_sorted[0][1] / total_sess * 100:.0f}% das sessões</strong>, "
                f"com comparação direta entre canais por comprimento, não por área.",
                "accent",
            )
            fig_caud = go.Figure(go.Bar(
                x=[item[1] for item in sess_sorted],
                y=[item[0] for item in sess_sorted],
                orientation="h",
                marker_color=[item[2] for item in sess_sorted],
                text=[f"{fmt_k(item[1])} · {item[1] / total_sess * 100:.0f}%" for item in sess_sorted],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=10, color=TEXT),
                hovertemplate="%{y}: %{x:,} sessões<extra></extra>",
            ))
            fig_caud.update_layout(**plotly_layout(height=265, showlegend=False))
            fig_caud.update_xaxes(visible=False, showgrid=False, range=[0, sess_sorted[0][1] * 1.28])
            fig_caud.update_yaxes(showgrid=False, categoryorder="array", categoryarray=[item[0] for item in sess_sorted[::-1]])
            st.plotly_chart(fig_caud, width="stretch", config=cfg)

    section("Quem mais monetiza dentro da audiência")
    takeaway(
        "<strong>Takeaway:</strong> a mesma audiência não vale igual em receita. O bloco abaixo prioriza "
        "os segmentos com maior conversão antes da leitura demográfica/comportamental da base.",
        "accent",
    )
    st.markdown(f"""<div class="info-box">
      💡 <b>Assinantes ativos</b> representam 24,5% das sessões mas respondem por
      <b>35,1% da receita total</b>. Usuários reativados convertem 2,3× mais que novos —
      campanhas de reativação com ROI positivo.
    </div>""", unsafe_allow_html=True)

    seg_data = AUDIENCE_MONETIZATION_SEGMENTS
    fig_seg = go.Figure()
    seg_colors = [ORANGE, PINK, PURPLE, GREEN]
    for i, (seg, cv) in enumerate(zip(seg_data["Segmento"], seg_data["Conv. (%)"])):
        fig_seg.add_trace(go.Bar(
            name=seg, x=[seg], y=[cv],
            marker_color=seg_colors[i],
            text=[f"{cv:.1f}%"], textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11),
        ))
    fig_seg.update_layout(**plotly_layout(
        height=240,
        showlegend=False,
        barmode="group",
        bargap=0.38,
    ))
    fig_seg.update_yaxes(ticksuffix="%", title="Taxa de Conversão")
    st.plotly_chart(fig_seg, width="stretch", config=cfg)

    spacer()
    section("Como a base está distribuída hoje")
    cd1, cd2, cd3 = st.columns(3)

    def dim_block(col, title: str, items: list):
        with col:
            st.markdown(f'<div style="font-size:11px;color:{MUTED};text-transform:uppercase;'
                        f'letter-spacing:.07em;margin-bottom:10px;">{title}</div>',
                        unsafe_allow_html=True)
            total = sum(v for _, v, _ in items)
            for lbl, val, color in items:
                pct = val / total * 100
                st.markdown(f"""
                <div class="band" style="flex-direction:column;align-items:flex-start;gap:6px;">
                  <div style="display:flex;justify-content:space-between;width:100%;">
                    <div class="band-label" style="font-size:12px;">{lbl}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{color};">
                      {fmt_k(val)}
                      <span style="color:{MUTED};font-size:10px;"> {pct:.0f}%</span>
                    </div>
                  </div>
                  <div style="width:100%;height:4px;background:{TRACK};border-radius:2px;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    if audience_profile_df.empty:
        empty_state()
    else:
        profile_map = {
            "dim1": [
                ("Não cadastrados", "nao_cadastrados", MUTED),
                ("Cadastrados não-log.", "cadastrados_nao_logados", ORANGE),
                ("Cadastrados logados", "cadastrados_logados", PURPLE),
            ],
            "dim2": [
                ("Nunca compraram", "nunca_compraram", MUTED),
                ("Já compraram (n-ass.)", "ja_compraram", ORANGE),
                ("Assinantes ativos", "assinantes_ativos", PURPLE),
            ],
            "dim3": [
                ("Novos usuários", "novos", ORANGE),
                ("Recorrentes", "recorrentes", PINK),
                ("Reativados", "reativados", PURPLE),
            ],
        }

        def profile_items(dim_key: str) -> list:
            dim_df = audience_profile_df[audience_profile_df["dimensao"] == dim_key].copy()
            dim_df["sessoes"] = pd.to_numeric(dim_df["sessoes"], errors="coerce").fillna(0)
            values = dim_df.set_index("segmento")["sessoes"].to_dict()
            return [(label, int(values.get(segmento, 0)), color) for label, segmento, color in profile_map[dim_key]]

        dim_block(cd1, "Dim 1 — Relacionamento c/ cadastro", profile_items("dim1"))
        dim_block(cd2, "Dim 2 — Relacionamento comercial", profile_items("dim2"))
        dim_block(cd3, "Dim 3 — Frequência de visita", profile_items("dim3"))


# ───────────────────────────────────────────────────────────────
#  TAB 4 — CADASTROS
# ───────────────────────────────────────────────────────────────
with tab4:
    kr1, kr2, kr3, kr4 = st.columns(4)
    reg_total = REG_FUNNEL[-1][1] if REG_FUNNEL else None
    reg_score_delta = safe_pct_change(REG_SCORE, score_trend[-2] if len(score_trend) > 1 else None)
    reg_conv = (
        float(np.average(registration_by_channel_df["conversao_para_venda"], weights=registration_by_channel_df["cadastros"]))
        if not registration_by_channel_df.empty and registration_by_channel_df["cadastros"].sum() > 0 else None
    )
    with kr1: st.markdown(kpi("Cadastros na semana", f"{int(reg_total):,}".replace(",", ".") if reg_total is not None else "—", None, accent=PURPLE), unsafe_allow_html=True)
    with kr2: st.markdown(kpi("Score médio", f"{REG_SCORE:.1f}/100" if REG_SCORE is not None else "—", reg_score_delta, accent=PINK), unsafe_allow_html=True)
    with kr3: st.markdown(kpi("Conv. cadastro→venda", f"{reg_conv:.1f}%" if reg_conv is not None else "—", None, accent=ORANGE), unsafe_allow_html=True)
    with kr4: st.markdown(kpi("Cadastros Completos", "8,4%", -0.7, accent=PURPLE), unsafe_allow_html=True)

    spacer()

    cf1, cf2 = st.columns([2, 1])

    with cf1:
        section("Maior perda acontece no fechamento do cadastro")
        if not REG_FUNNEL:
            empty_state()
        else:
            takeaway(
                "<strong>Takeaway:</strong> o maior gargalo está entre início do formulário e cadastro efetivado, "
                "então a clareza do fluxo final importa mais do que trazer novos visitantes para o topo.",
                "alert",
            )
            FCOLORS = [PURPLE, NAVY, PINK, GREEN, ORANGE]
            total_v = REG_FUNNEL[0][1]
            for i, (label, val, conv) in enumerate(REG_FUNNEL):
                pct = val / total_v * 100
                color = FCOLORS[i]
                sub = (f'<div class="frow-sub">{conv:.1f}% da etapa anterior</div>'
                       if conv else "")
                st.markdown(f"""
                <div class="frow" style="border-left-color:{color};">
                  <div>
                    <div class="frow-label">{label}</div>
                    {sub}
                  </div>
                  <div>
                    <div class="frow-n" style="color:{color};">{val:,}</div>
                    <div class="frow-pct">{pct:.1f}% do início</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            fig_fnn = go.Figure(go.Funnel(
                y=[r[0] for r in REG_FUNNEL],
                x=[r[1] for r in REG_FUNNEL],
                textinfo="value+percent initial",
                marker=dict(color=FCOLORS),
                connector=dict(line=dict(color=BORDER, width=1)),
                textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
            ))
            fig_fnn.update_layout(**plotly_layout(height=280))
            st.plotly_chart(fig_fnn, width="stretch", config=cfg)

    with cf2:
        section("Qualidade dos cadastros")
        total_q = sum(v for _, v, _ in REG_QUALITY)
        for name, qty, color in REG_QUALITY:
            pct = qty / total_q * 100
            st.markdown(f"""
            <div class="band" style="flex-direction:column;gap:6px;align-items:flex-start;">
              <div style="display:flex;justify-content:space-between;width:100%;">
                <div style="font-size:12.5px;">{name}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{color};">
                  {qty:,} <span style="color:{MUTED};font-size:10px;">{pct:.0f}%</span>
                </div>
              </div>
              <div style="width:100%;height:5px;background:{TRACK};border-radius:2px;">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

        spacer(10)
        if registration_score_trend_df.empty:
            empty_state()
        else:
            fig_sc = go.Figure(go.Scatter(
                x=week_labels(registration_score_trend_df), y=score_trend,
                mode="lines+markers",
                line=dict(color=PINK, width=2.5),
                marker=dict(size=6, color=PINK),
                fill="tozeroy", fillcolor=PINK_SOFT,
                hovertemplate="Score: %{y:.1f}<extra></extra>",
            ))
            fig_sc.add_hline(y=60, line_dash="dot", line_color=MUTED,
                              annotation_text="meta 60",
                              annotation_font_color=MUTED, annotation_font_size=10)
            fig_sc.update_layout(**plotly_layout(
                height=190,
                showlegend=False,
                title=dict(text="Evolução do score médio", font=dict(size=11, color=MUTED)),
            ))
            fig_sc.update_yaxes(range=[50, 78])
            st.plotly_chart(fig_sc, width="stretch", config=cfg)

    section("Cadastros por canal de origem")
    if registration_by_channel_df.empty:
        empty_state()
    else:
        rows = ""
        total_reg_channel = registration_by_channel_df["cadastros"].sum()
        for ch, qty, score_avg, conv_v in REG_CH:
            sb = (f'<span class="bg">{score_avg:.1f}</span>' if score_avg >= 65
                  else f'<span class="bp">{score_avg:.1f}</span>' if score_avg >= 55
                  else f'<span class="bo">{score_avg:.1f}</span>')
            share = (qty / total_reg_channel * 100) if total_reg_channel else 0
            rows += (f"<tr><td><b>{ch}</b></td>"
                     f"<td class='mono'>{int(qty):,}</td>"
                     f"<td class='mono'>{share:.1f}%</td>"
                     f"<td>{sb}</td>"
                     f"<td class='mono'>{conv_v:.1f}%</td></tr>")
        st.markdown(f"""
        <table class="dtable">
          <thead><tr>
            <th>Canal</th><th>Cadastros</th><th>% do total</th>
            <th>Score médio</th><th>Conv. → venda</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    spacer()
    section("Tabela de pontuação — critérios de qualidade")
    attr_rows = """
    <tr><td>Cadastro completo (obrigatórios)</td><td class='mono'>20 pts</td><td><span class='bp'>base</span></td></tr>
    <tr><td>Hora de nascimento</td><td class='mono'>35 pts</td><td><span class='bg'>alto impacto</span></td></tr>
    <tr><td>Opt-in alertas de trânsitos (e-mail)</td><td class='mono'>35 pts</td><td><span class='bg'>alto impacto</span></td></tr>
    <tr><td>Opt-in notificações do navegador</td><td class='mono'>5 pts</td><td><span class='bo'>complementar</span></td></tr>
    <tr><td>Opt-in promoções e novidades</td><td class='mono'>5 pts</td><td><span class='bo'>complementar</span></td></tr>
    """
    st.markdown(f"""
    <table class="dtable">
      <thead><tr><th>Atributo</th><th>Pontos</th><th>Relevância</th></tr></thead>
      <tbody>{attr_rows}</tbody>
    </table>""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
#  TAB 5 — CHECKOUT
# ───────────────────────────────────────────────────────────────
with tab5:
    kch1, kch2, kch3, kch4 = st.columns(4)
    started_trad = CART_TRAD[0][1] if CART_TRAD else 0
    started_quick = CART_QUICK[0][1] if CART_QUICK else 0
    with kch1: st.markdown(kpi("Carrinhos iniciados", f"{started_trad + started_quick:,}" if (started_trad + started_quick) else "—", None, accent=PURPLE), unsafe_allow_html=True)
    with kch2: st.markdown(kpi("Conv. carrinho trad.", f"{(CART_CONV_TRAD or 0) * 100:.1f}%" if CART_CONV_TRAD is not None else "—", None, accent=PINK), unsafe_allow_html=True)
    with kch3: st.markdown(kpi("Conv. compra rápida", f"{(CART_CONV_QUICK or 0) * 100:.1f}%" if CART_CONV_QUICK is not None else "—", None, accent=ORANGE), unsafe_allow_html=True)
    with kch4: st.markdown(kpi("Ticket médio geral", fmt_brl(TK_CW) if TK_CW is not None else "—", dtk, accent=PURPLE), unsafe_allow_html=True)

    spacer()
    section("Onde perdemos conversão ao longo do checkout")
    takeaway(
        "<strong>Takeaway:</strong> a leitura desta aba foi reorganizada para seguir a sequência real da jornada: "
        "perda no funil, recuperação, meio de pagamento, ticket incremental e perfil de conversão.",
        "accent",
    )

    cc1, cc2 = st.columns(2)

    # ── Traditional cart funnel ─────────────────────────────────
    with cc1:
        section("Carrinho tradicional")
        if not CART_TRAD:
            empty_state()
        else:
            fig_ct = go.Figure(go.Funnel(
                y=[r[0] for r in CART_TRAD],
                x=[r[1] for r in CART_TRAD],
                textinfo="value+percent initial",
                marker=dict(color=[PURPLE, NAVY, PINK, GREEN, ORANGE]),
                connector=dict(line=dict(color=BORDER, width=1)),
                textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
            ))
            fig_ct.update_layout(**plotly_layout(height=290))
            st.plotly_chart(fig_ct, width="stretch", config=cfg)

            for label, val, conv, aband in CART_TRAD[1:]:
                if aband is not None:
                    aband_color = ORANGE if aband > 10 else MUTED
                    st.markdown(f"""
                    <div class="band">
                      <div class="band-label" style="font-size:12px;">{label}</div>
                      <div style="display:flex;gap:12px;align-items:center;">
                        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{GREEN};">
                          ✓ {conv:.1f}%</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{aband_color};">
                          ✗ {aband:.1f}%</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

    # ── Quick buy funnel ────────────────────────────────────────
    with cc2:
        section("Compra rápida")
        if not CART_QUICK:
            empty_state()
        else:
            fig_cq = go.Figure(go.Funnel(
                y=[r[0] for r in CART_QUICK[:4]],
                x=[r[1] for r in CART_QUICK[:4]],
                textinfo="value+percent initial",
                marker=dict(color=[PINK, PURPLE, ORANGE, NAVY]),
                connector=dict(line=dict(color=BORDER, width=1)),
                textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
            ))
            fig_cq.update_layout(**plotly_layout(height=290))
            st.plotly_chart(fig_cq, width="stretch", config=cfg)

            if len(CART_QUICK) >= 6:
                st.markdown(f"""<div class="alert-box">
                  ⚠️ <b>{CART_QUICK[4][1]} falhas de processamento</b>
                  ({CART_QUICK[4][2]:.1f}% dos inícios).
                  {CART_QUICK[5][1]} usuários migraram para o carrinho tradicional
                  ({CART_QUICK[5][2]:.1f}% das falhas).
                </div>""", unsafe_allow_html=True)

        section("O que recupera receita após abandono")
        if cart_recovery_df.empty:
            empty_state()
        else:
            rec_items = [
                ("Carrinhos elegíveis", f"{ABAND_ELIG:,}", TEXT),
                ("Mensagens enviadas", f"{MSGS_SENT:,}", TEXT),
                ("Carrinhos recuperados", f"{RECOVERED:,}", GREEN),
                ("Taxa de recuperação", f"{(REC_RATE or 0) * 100:.1f}%", GREEN),
                ("Receita recuperada", fmt_brl(REC_REV or 0), PINK),
            ]
            for lbl, val, color in rec_items:
                st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                            f'<div class="band-val" style="color:{color};">{val}</div>'
                            f'</div>', unsafe_allow_html=True)

    # ── Payment + Product conversion ────────────────────────────
    spacer()
    section("O que mais ajuda a fechar e ampliar ticket")
    cp1, cp2 = st.columns(2)

    with cp1:
        if not PAYMENTS:
            section("Meio de pagamento")
            empty_state()
        else:
            best_payment = max(PAYMENTS, key=lambda item: item[2])
            section(f"Meio de pagamento: {best_payment[0]} lidera a conversão")
            takeaway(
                f"<strong>Takeaway:</strong> {best_payment[0]} converte <strong>{best_payment[2] * 100:.1f}% </strong>, "
                "enquanto os demais meios aparecem como comparação de suporte.",
                "good",
            )
            pay_labels = [p[0] for p in PAYMENTS]
            pay_conc = [p[2] * 100 for p in PAYMENTS]
            pay_aband = [p[3] * 100 for p in PAYMENTS]
            fig_pay = go.Figure()
            fig_pay.add_trace(go.Bar(
                name="Concluídos", x=pay_labels, y=pay_conc,
                marker_color=PURPLE,
                text=[f"{v:.1f}%" for v in pay_conc],
                textposition="inside",
                textfont=dict(family="JetBrains Mono", size=10, color="white"),
            ))
            fig_pay.add_trace(go.Bar(
                name="Abandonados", x=pay_labels, y=pay_aband,
                marker_color=ORANGE,
                text=[f"{v:.1f}%" for v in pay_aband],
                textposition="inside",
                textfont=dict(family="JetBrains Mono", size=10, color="white"),
            ))
            fig_pay.update_layout(**plotly_layout(height=270, barmode="stack", bargap=0.35))
            fig_pay.update_yaxes(ticksuffix="%")
            st.plotly_chart(fig_pay, width="stretch", config=cfg)

    with cp2:
        section("Produtos com maior conversão após adição ao carrinho")
        if not PRODS:
            empty_state()
        else:
            sorted_p = sorted(PRODS, key=lambda x: x["conv"], reverse=True)
            fig_pcv = go.Figure(go.Bar(
                x=[p["name"] for p in sorted_p],
                y=[p["conv"] * 100 for p in sorted_p],
                marker=dict(
                    color=[p["conv"] * 100 for p in sorted_p],
                    colorscale=[[0, ORANGE], [0.5, PURPLE], [1, GREEN]],
                ),
                text=[f"{p['conv']*100:.1f}%" for p in sorted_p],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=9),
                hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
            ))
            fig_pcv.update_layout(**plotly_layout(
                height=270,
                bargap=0.3,
                xaxis=dict(tickangle=-35, tickfont=dict(size=9)),
                yaxis=dict(ticksuffix="%"),
            ))
            st.plotly_chart(fig_pcv, width="stretch", config=cfg)

    # ── Upsell vitrine ──────────────────────────────────────────
    spacer()
    section("Onde ampliamos ticket dentro do carrinho")
    cu1, cu2, cu3, cu4 = st.columns(4)
    upsell_taxa = normalize_ratio(pd.to_numeric(UPSELL_ROW.get("taxa_adicao"), errors="coerce")) if not UPSELL_ROW.empty else None
    upsell_ticket = float(pd.to_numeric(UPSELL_ROW.get("impacto_ticket_medio"), errors="coerce") or 0) if not UPSELL_ROW.empty else None
    upsell_carts = int(pd.to_numeric(UPSELL_ROW.get("carrinhos_com_upsell"), errors="coerce") or 0) if not UPSELL_ROW.empty else None
    upsell_revenue = float(pd.to_numeric(UPSELL_ROW.get("receita_incremental"), errors="coerce") or 0) if not UPSELL_ROW.empty else None
    with cu1: st.markdown(kpi("Taxa de adição", f"{(upsell_taxa or 0) * 100:.1f}%" if upsell_taxa is not None else "—", None, accent=PURPLE), unsafe_allow_html=True)
    with cu2: st.markdown(kpi("Impacto no ticket", f"+R$ {upsell_ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if upsell_ticket is not None else "—", None, accent=PINK), unsafe_allow_html=True)
    with cu3: st.markdown(kpi("Carrinhos c/ upsell", f"{upsell_carts:,}" if upsell_carts is not None else "—", None, accent=ORANGE), unsafe_allow_html=True)
    with cu4: st.markdown(kpi("Receita incremental", fmt_brl(upsell_revenue) if upsell_revenue is not None else "—", None, accent=PURPLE), unsafe_allow_html=True)

    # ── Segmentation deep-dives ─────────────────────────────────
    spacer()
    section("Quem converte melhor no checkout")
    cs1, cs2, cs3 = st.columns(3)

    seg_comercial = []
    seg_engagement = []
    seg_safra = []
    if not conversion_by_segment_df.empty:
        conversion_by_segment_df["conversao_pct"] = pd.to_numeric(conversion_by_segment_df["conversao_pct"], errors="coerce").fillna(0)
        color_maps = {
            "perfil_comercial": [ORANGE, PINK, PURPLE],
            "perfil_engajamento": [ORANGE, PINK, PURPLE],
            "safra_cadastro": [MUTED, ORANGE, PINK, PURPLE],
        }

        def segment_block_data(key: str) -> list:
            seg_df = conversion_by_segment_df[conversion_by_segment_df["segmentacao"] == key]
            return [
                (row.segmento, float(row.conversao_pct), color_maps[key][idx])
                for idx, row in enumerate(seg_df.itertuples(index=False))
            ]

        seg_comercial = segment_block_data("perfil_comercial")
        seg_engagement = segment_block_data("perfil_engajamento")
        seg_safra = segment_block_data("safra_cadastro")

    def conv_seg_block(col, title, data):
        with col:
            st.markdown(f'<div class="sec-title" style="font-size:14px;">{title}</div>',
                        unsafe_allow_html=True)
            for lbl, val, color in data:
                bar_w = min(val, 100)
                st.markdown(f"""
                <div class="band" style="flex-direction:column;gap:5px;align-items:flex-start;">
                  <div style="display:flex;justify-content:space-between;width:100%;">
                    <div class="band-label" style="font-size:12px;">{lbl}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{color};">{val:.1f}%</div>
                  </div>
                  <div style="width:100%;height:4px;background:{TRACK};border-radius:2px;">
                    <div style="width:{bar_w}%;height:100%;background:{color};border-radius:2px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    if conversion_by_segment_df.empty:
        empty_state()
    else:
        conv_seg_block(cs1, "Por perfil comercial", seg_comercial)
        conv_seg_block(cs2, "Por perfil de engajamento", seg_engagement)
        conv_seg_block(cs3, "Por safra de cadastro", seg_safra)


# ───────────────────────────────────────────────────────────────
#  TAB 6 — FORECAST
# ───────────────────────────────────────────────────────────────
with tab6:
    next_month_growth = (REV_FORECAST_BASE[0] - REV_MONTH_HIST[-1]) / REV_MONTH_HIST[-1] * 100
    sixth_month_growth = (REV_FORECAST_BASE[-1] - REV_MONTH_HIST[-1]) / REV_MONTH_HIST[-1] * 100
    base_6m = sum(REV_FORECAST_BASE)
    hist_6m = sum(REV_MONTH_HIST)
    acc_growth = (base_6m - hist_6m) / hist_6m * 100
    gap_to_target = (sum(REV_FORECAST_BASE) - sum(REV_TARGET)) / sum(REV_TARGET) * 100

    kf1, kf2, kf3, kf4 = st.columns(4)
    with kf1: st.markdown(kpi("Receita proj. próximo mês", fmt_brl(REV_FORECAST_BASE[0]), next_month_growth, accent=PINK), unsafe_allow_html=True)
    with kf2: st.markdown(kpi("Receita proj. 6º mês", fmt_brl(REV_FORECAST_BASE[-1]), sixth_month_growth, accent=PURPLE), unsafe_allow_html=True)
    with kf3: st.markdown(kpi("Acumulado proj. 6 meses", fmt_brl(base_6m), acc_growth, accent=ORANGE), unsafe_allow_html=True)
    with kf4: st.markdown(kpi("Gap p/ meta 6 meses", f"{gap_to_target:.1f}%", gap_to_target, good_if_positive=False, accent=GREEN), unsafe_allow_html=True)

    spacer()

    ff1, ff2 = st.columns([2.2, 1])
    with ff1:
        section("Receita deve seguir crescendo nos próximos 6 meses")
        takeaway(
            f"<strong>Takeaway:</strong> o cenário base projeta saída de <strong>{fmt_brl(REV_MONTH_HIST[-1])}</strong> "
            f"em {MONTHS_HIST[-1]} para <strong>{fmt_brl(REV_FORECAST_BASE[-1])}</strong> em {MONTHS_FORECAST[-1]}, "
            f"com faixa provável entre <strong>{fmt_brl(REV_FORECAST_LOW[-1])}</strong> e <strong>{fmt_brl(REV_FORECAST_HIGH[-1])}</strong>.",
            "good",
        )
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Bar(
            x=MONTHS_HIST,
            y=REV_MONTH_HIST,
            name="Realizado",
            marker_color=TRACK_STRONG,
            hovertemplate="Realizado: R$ %{y:,.0f}<extra></extra>",
        ))
        fig_fc.add_trace(go.Scatter(
            x=MONTHS_FORECAST,
            y=REV_FORECAST_LOW,
            mode="lines",
            line=dict(color=rgba(PURPLE, 0.12), width=1),
            hoverinfo="skip",
            showlegend=False,
        ))
        fig_fc.add_trace(go.Scatter(
            x=MONTHS_FORECAST,
            y=REV_FORECAST_HIGH,
            mode="lines",
            line=dict(color=rgba(PURPLE, 0.12), width=1),
            fill="tonexty",
            fillcolor=PURPLE_SOFT,
            name="Faixa provável",
            hovertemplate="Máximo esperado: R$ %{y:,.0f}<extra></extra>",
        ))
        fig_fc.add_trace(go.Scatter(
            x=MONTHS_FORECAST,
            y=REV_FORECAST_BASE,
            mode="lines+markers",
            name="Cenário base",
            line=dict(color=PINK, width=2.5),
            marker=dict(size=7, color=PINK, line=dict(color=CARD, width=1.5)),
            hovertemplate="Base: R$ %{y:,.0f}<extra></extra>",
        ))
        fig_fc.add_trace(go.Scatter(
            x=MONTHS_FORECAST,
            y=REV_TARGET,
            mode="lines",
            name="Meta",
            line=dict(color=GREEN, width=2, dash="dash"),
            hovertemplate="Meta: R$ %{y:,.0f}<extra></extra>",
        ))
        fig_fc.update_layout(**plotly_layout(height=320, barmode="overlay"))
        fig_fc.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
        st.plotly_chart(fig_fc, width="stretch", config=cfg)

    with ff2:
        retain_share = np.mean([r / b for r, b in zip(REV_DRIVER_RETAIN, REV_FORECAST_BASE)]) * 100
        new_share = np.mean([r / b for r, b in zip(REV_DRIVER_NEW, REV_FORECAST_BASE)]) * 100
        upsell_share = np.mean([r / b for r, b in zip(REV_DRIVER_UPSELL, REV_FORECAST_BASE)]) * 100
        section("Hipóteses que sustentam o forecast")
        for lbl, val, color in [
            ("Receita de retenção", f"{retain_share:.0f}% da base", PURPLE),
            ("Nova receita", f"{new_share:.0f}% da base", PINK),
            ("Upsell e expansão", f"{upsell_share:.0f}% da base", ORANGE),
            ("Principal risco", "renovação abaixo da média", ORANGE),
            ("Principal alavanca", "reativação + CRM próprio", GREEN),
        ]:
            st.markdown(f"""<div class="band">
              <div class="band-label">{lbl}</div>
              <div class="band-val" style="color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)

    spacer()
    section("O que sustenta a projeção mês a mês")
    takeaway(
        "<strong>Takeaway:</strong> a retenção continua sendo a maior parte da receita projetada, "
        "mas o avanço ao longo dos meses depende do ganho em nova receita e do incremento de upsell.",
        "accent",
    )
    fig_drv = go.Figure()
    fig_drv.add_trace(go.Bar(
        x=MONTHS_FORECAST,
        y=REV_DRIVER_RETAIN,
        name="Retenção",
        marker_color=PURPLE,
        hovertemplate="Retenção: R$ %{y:,.0f}<extra></extra>",
    ))
    fig_drv.add_trace(go.Bar(
        x=MONTHS_FORECAST,
        y=REV_DRIVER_NEW,
        name="Nova receita",
        marker_color=PINK,
        hovertemplate="Nova receita: R$ %{y:,.0f}<extra></extra>",
    ))
    fig_drv.add_trace(go.Bar(
        x=MONTHS_FORECAST,
        y=REV_DRIVER_UPSELL,
        name="Upsell",
        marker_color=ORANGE,
        hovertemplate="Upsell: R$ %{y:,.0f}<extra></extra>",
    ))
    fig_drv.update_layout(**plotly_layout(height=300, barmode="stack", bargap=0.3))
    fig_drv.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    st.plotly_chart(fig_drv, width="stretch", config=cfg)
