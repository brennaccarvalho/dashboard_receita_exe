"""
Analytics Dashboard
Weekly Performance Report
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  BRAND TOKENS
# ═══════════════════════════════════════════════════════════════
NAVY   = "#151731"
PURPLE = "#760681"
PINK   = "#CE008D"
ORANGE = "#EF4D03"
BG     = "#0b0d1f"
CARD   = "#13162e"
CARD2  = "#1a1e3c"
TEXT   = "#dde0f2"
MUTED  = "#6b6f8e"
GREEN  = "#4ade80"
RED_SOFT = "#f87171"

# ═══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Google Fonts ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

@font-face {{
  font-family: 'Aconchego';
  src: local('Aconchego'), local('Aconchego-Regular');
  font-weight: normal; font-style: normal;
}}

/* ── Base ───────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [class*="css"], .stApp, .main {{
  font-family: 'Figtree', sans-serif !important;
  background-color: {BG} !important;
  color: {TEXT} !important;
}}

h1, h2, h3, h4 {{
  font-family: 'Aconchego', 'Georgia', serif !important;
  font-weight: normal !important;
  color: {TEXT} !important;
}}

/* ── Hide Streamlit chrome ──────────────────────── */
#MainMenu, footer, .stDeployButton {{ visibility: hidden; }}
.block-container {{
  padding: 1.8rem 2rem 3rem 2rem !important;
  max-width: 1440px !important;
}}

/* ── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] > div:first-child {{
  background: {NAVY} !important;
  border-right: 1px solid rgba(255,255,255,0.05);
}}
[data-testid="stSidebar"] * {{
  color: {TEXT} !important;
}}

/* ── Tabs ───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
  background: {NAVY};
  border-radius: 12px;
  padding: 5px;
  gap: 3px;
  border: 1px solid rgba(255,255,255,0.06);
  flex-wrap: nowrap;
}}
.stTabs [data-baseweb="tab"] {{
  font-family: 'Figtree', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: {MUTED};
  border-radius: 8px;
  padding: 8px 20px;
  border: none !important;
  background: transparent !important;
  white-space: nowrap;
}}
.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, {PURPLE}, {PINK}) !important;
  color: #fff !important;
  font-weight: 600 !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
  background: transparent !important;
  padding: 0 !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}

/* ── KPI Card ───────────────────────────────────── */
.kpi-card {{
  background: {CARD};
  border-radius: 14px;
  padding: 18px 20px 16px 20px;
  border: 1px solid rgba(255,255,255,0.06);
  height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}}
.kpi-card::before {{
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  border-radius: 0 0 14px 14px;
}}
.kpi-label {{
  font-size: 10.5px;
  font-weight: 600;
  color: {MUTED};
  text-transform: uppercase;
  letter-spacing: 0.09em;
  font-family: 'Figtree', sans-serif;
}}
.kpi-value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 600;
  color: {TEXT};
  line-height: 1;
}}
.kpi-delta-pos {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {GREEN};
}}
.kpi-delta-neg {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {ORANGE};
}}
.kpi-delta-neu {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: {MUTED};
}}

/* ── Section Title ──────────────────────────────── */
.sec-title {{
  font-family: 'Aconchego', 'Georgia', serif;
  font-size: 17px;
  font-weight: normal;
  color: {TEXT};
  margin: 1.4rem 0 0.75rem 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}}

/* ── Data Table ─────────────────────────────────── */
.dtable {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  font-family: 'Figtree', sans-serif;
}}
.dtable th {{
  background: rgba(255,255,255,0.03);
  color: {MUTED};
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}}
.dtable td {{
  padding: 9px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  color: {TEXT};
  vertical-align: middle;
}}
.dtable tr:last-child td {{ border-bottom: none; }}
.dtable tr:hover td {{ background: rgba(255,255,255,0.02); }}
.mono {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; }}

/* ── Badges ─────────────────────────────────────── */
.bg {{ background:rgba(74,222,128,.14); color:{GREEN}; padding:2px 8px; border-radius:4px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bo {{ background:rgba(239,77,3,.14); color:{ORANGE}; padding:2px 8px; border-radius:4px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bp {{ background:rgba(118,6,129,.14); color:#d490e4; padding:2px 8px; border-radius:4px; font-size:11px; font-family:'JetBrains Mono',monospace; }}
.bk {{ background:rgba(206,0,141,.14); color:{PINK}; padding:2px 8px; border-radius:4px; font-size:11px; font-family:'JetBrains Mono',monospace; }}

/* ── Band Row ───────────────────────────────────── */
.band {{
  background: {CARD};
  border-radius: 9px;
  padding: 11px 16px;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid rgba(255,255,255,0.04);
}}
.band-label {{ font-size: 12.5px; color: {TEXT}; }}
.band-val {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; }}

/* ── Funnel Row ─────────────────────────────────── */
.frow {{
  background: {CARD};
  border-radius: 10px;
  padding: 13px 16px;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 3px solid transparent;
}}
.frow-label {{ font-size: 12.5px; font-weight: 500; color: {TEXT}; }}
.frow-sub   {{ font-size: 10.5px; color: {MUTED}; font-family: 'JetBrains Mono', monospace; margin-top:2px; }}
.frow-n     {{ font-family: 'JetBrains Mono', monospace; font-size: 17px; font-weight: 600; text-align:right; }}
.frow-pct   {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {MUTED}; text-align:right; }}

/* ── Alert / Info ───────────────────────────────── */
.alert-box {{
  background: rgba(239,77,3,.10);
  border: 1px solid rgba(239,77,3,.25);
  border-radius: 9px;
  padding: 11px 15px;
  font-size: 12.5px;
  color: #ffb08a;
  margin-bottom: 10px;
}}
.info-box {{
  background: rgba(118,6,129,.10);
  border: 1px solid rgba(118,6,129,.25);
  border-radius: 9px;
  padding: 11px 15px;
  font-size: 12.5px;
  color: #d4a0de;
  margin-bottom: 10px;
}}

/* ── Bar mini ───────────────────────────────────── */
.mini-bar-wrap {{
  flex: 1; margin: 0 14px;
  height: 5px;
  background: rgba(255,255,255,.07);
  border-radius: 3px;
  overflow: hidden;
}}
.mini-bar-fill {{ height: 100%; border-radius: 3px; }}

/* ── Selectbox / inputs ─────────────────────────── */
[data-baseweb="select"] > div {{
  background: {CARD2} !important;
  border-color: rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
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

/* ── Divider ────────────────────────────────────── */
hr {{ border-color: rgba(255,255,255,0.07) !important; }}

/* ── Scrollbar ──────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.12); border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def fmt_brl(v: float) -> str:
    s = f"{abs(v):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + "R$ " + s

def fmt_k(v: float) -> str:
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.1f}k"
    return str(int(v))

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

def plotly_theme() -> dict:
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Figtree, sans-serif", color=TEXT, size=12),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)",
                   linecolor="rgba(255,255,255,0.08)",
                   tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)",
                   linecolor="rgba(255,255,255,0.08)",
                   tickfont=dict(size=11)),
        margin=dict(l=8, r=8, t=30, b=8),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
        hoverlabel=dict(bgcolor=NAVY, font=dict(family="Figtree", size=12),
                        bordercolor="rgba(255,255,255,0.15)"),
    )

cfg = {"displayModeBar": False, "responsive": True}


# ═══════════════════════════════════════════════════════════════
#  MOCK DATA  (seeded for reproducibility)
# ═══════════════════════════════════════════════════════════════
rng = np.random.default_rng(42)
TODAY = datetime(2026, 3, 17)
N = 8
WEEKS = [(TODAY - timedelta(weeks=N - 1 - i)).strftime("%d/%m") for i in range(N)]
CW = WEEKS[-1]   # current week label

# ── Revenue ──────────────────────────────────────────────────
rev     = [88400., 76200., 92100., 84600., 79800., 96300., 88700., 94200.]
rev_yoy = [r * rng.uniform(0.72, 0.86) for r in rev]
trx     = [int(r / rng.uniform(88, 116)) for r in rev]
ticket  = [r / t for r, t in zip(rev, trx)]

rev_pt  = [r * rng.uniform(0.62, 0.72) for r in rev]
rev_ass = [r - p for r, p in zip(rev, rev_pt)]

REV_CW = rev[-1]; REV_PW = rev[-2]
TRX_CW = trx[-1]; TRX_PW = trx[-2]
TK_CW  = ticket[-1]; TK_PW  = ticket[-2]
ARR    = 498_600.; ARR_PW = 490_100.
RENEW_WEEK  = 0.836
RENEW_12M   = 0.814
renew_trend = [0.78, 0.82, 0.86, 0.81, 0.79, 0.84, 0.88, 0.836]
new_arr     = [3200, 4100, 5800, 3600, 4400, 6200, 3800, 4900]
SUBS_VENCE  = {"30d": 118, "60d": 204, "90d": 337}

# ── Products ─────────────────────────────────────────────────
PRODS = [
    {"name": "Mapa Astral",           "price": 89.99, "ini": 312, "conc": 198},
    {"name": "Tarot e o Amor",        "price": 39.95, "ini": 487, "conc": 362},
    {"name": "Clube Premium",         "price": 330.00,"ini": 88,  "conc": 41 },
    {"name": "Revolução Solar",       "price": 69.29, "ini": 224, "conc": 142},
    {"name": "Previsões da sua Vida", "price": 69.87, "ini": 195, "conc": 114},
    {"name": "Tarot Mensal",          "price": 39.95, "ini": 318, "conc": 253},
    {"name": "Sinastria Amorosa",     "price": 59.93, "ini": 147, "conc": 88 },
    {"name": "Mapa do Ano / Tarot",   "price": 69.29, "ini": 178, "conc": 109},
]
for p in PRODS:
    p["conv"]   = p["conc"] / p["ini"]
    p["receita"]= p["conc"] * p["price"]
df_prods = pd.DataFrame(PRODS).sort_values("receita", ascending=False)

# ── Channels ─────────────────────────────────────────────────
CHS     = ["Orgânico", "E-mail", "Direto", "Redes Sociais", "Pago", "Alertas"]
ch_rev  = [33200, 19400, 13800, 10100,  8600,  9100]
ch_sess = [44800, 11200, 17600,  9400,  5800,  5200]
ch_conv = [r/s*100 for r, s in zip(ch_rev, ch_sess)]
CHS_PAL = [PURPLE, PINK, ORANGE, "#5b2d8e", "#ff6b35", "#a0259a"]

# ── Audience ─────────────────────────────────────────────────
SESS_CW   = 94_000; SESS_PW = 87_400
UV_CW     = 61_200
ENG_RATE  = 0.524
PPG       = 3.7
sess_wk   = [82400, 71200, 89600, 84100, 76800, 93400, 87400, 94000]
sess_yoy  = [s * rng.uniform(0.74, 0.88) for s in sess_wk]

# ── GSC ──────────────────────────────────────────────────────
gsc_imp = [1_240_000, 1_180_000, 1_310_000, 1_290_000,
           1_220_000, 1_380_000, 1_340_000, 1_410_000]
gsc_clk = [28400, 25100, 31200, 29800, 27600, 33100, 30800, 34200]
gsc_ctr = [c/i*100 for c, i in zip(gsc_clk, gsc_imp)]
gsc_pos = [18.4, 18.9, 17.8, 17.6, 18.1, 17.2, 17.4, 16.9]

# ── Registrations ────────────────────────────────────────────
REG_FUNNEL = [
    ("Visitantes não-logados",                94000, None),
    ("Encontraram barreira de cadastro",       18700, 19.9),
    ("Acessaram página de login / cadastro",   11400, 61.0),
    ("Iniciaram formulário",                    8900, 78.1),
    ("Cadastros efetivados",                    3240, 36.4),
]
REG_SCORE   = 62.4
REG_CH = [
    ("Orgânico",     1210, 64.2, 14.8),
    ("E-mail",        680, 71.8, 17.2),
    ("Direto",        540, 58.9, 13.6),
    ("Redes Sociais", 480, 52.3, 11.8),
    ("Pago",          220, 67.1, 15.9),
    ("Alertas",       110, 55.4, 12.4),
]
score_trend = [58.2, 59.8, 61.0, 59.4, 60.1, 61.8, 59.3, 62.4]

# ── Checkout ─────────────────────────────────────────────────
CART_TRAD = [
    ("Início (produto ao carrinho)",  4820, None, None),
    ("Escolha do meio de pagamento",  3960, 82.2, 17.8),
    ("Vitrine de upsell",             3780, 95.5, 4.5),
    ("Início do processamento",       3540, 93.7, 6.3),
    ("Carrinho concluído",            3018, 85.3, 14.7),
]
CART_QUICK = [
    ("Início (clique compra rápida)", 2140, None, None),
    ("Confirmação de login",          1820, 85.0, 15.0),
    ("Início do processamento",       1710, 93.9, 6.1),
    ("Concluída com sucesso",         1490, 87.1, None),
    ("Falha no processamento",         220, 12.9, None),
    ("Migração p/ carrinho trad.",      96, 43.6, None),
]
CART_CONV_TRAD  = 3018 / 4820
CART_CONV_QUICK = 1490 / 2140

PAYMENTS = [
    ("Cartão de Crédito", 1842, 0.892, 0.108),
    ("Pix",               1024, 0.934, 0.066),
    ("Boleto",             284, 0.761, 0.239),
    ("Cartão de Débito",   112, 0.848, 0.152),
]
ABAND_ELIG = 1802; MSGS_SENT = 1540; RECOVERED = 312
REC_RATE   = RECOVERED / ABAND_ELIG
REC_REV    = RECOVERED * 84.6


# ───────────────────────────────────────────────────────────────
#  DATA SOURCE (plug & play)
# ───────────────────────────────────────────────────────────────
_MOCK_DATA = {k: v for k, v in globals().items() if k.isupper()}


def get_data(use_mock: bool = True) -> dict:
    """Returns all dashboard variables.

    - use_mock=True: returns built-in mock dataset (default).
    - use_mock=False: implement loading from real sources (DB/APIs) here.
    """
    if use_mock:
        return _MOCK_DATA

    st.warning(
        "Modo conectado: dados reais não configurados. "
        "Implemente get_data(use_mock=False) para carregar dados reais."
    )

    # TODO: carregue dados reais aqui, mantendo as mesmas chaves/variáveis.
    return _MOCK_DATA


USE_MOCK_DATA = st.sidebar.checkbox(
    "Usar dados mock (sem conexão)", True,
    help="Desative para usar dados reais (requer implementação em get_data).",
)


data = get_data(USE_MOCK_DATA)
globals().update(data)


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0 28px 0;">
      <div style="font-size:38px; margin-bottom:6px;">�</div>
      <div style="font-family:'Aconchego','Georgia',serif; font-size:22px;
                  color:{TEXT}; letter-spacing:0.02em;">Analytics</div>
      <div style="font-size:10px; color:{MUTED}; text-transform:uppercase;
                  letter-spacing:0.14em; margin-top:2px;">Dashboard semanal</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;color:{MUTED};text-transform:uppercase;"
                f"letter-spacing:.08em;margin-bottom:6px;'>Semana de referência</div>",
                unsafe_allow_html=True)
    week_sel = st.selectbox("", WEEKS, index=len(WEEKS) - 1, label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;color:{MUTED};text-transform:uppercase;"
                f"letter-spacing:.08em;margin-bottom:6px;'>Comparação</div>",
                unsafe_allow_html=True)
    compare = st.radio("", ["4 semanas anteriores", "Ano anterior (YoY)", "Ambos"],
                       index=2, label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Status bullets
    st.markdown(f"""
    <div style="background:{CARD}; border-radius:10px; padding:14px 15px;
                border:1px solid rgba(255,255,255,.05);">
      <div style="font-size:10px;color:{MUTED};text-transform:uppercase;
                  letter-spacing:.08em;margin-bottom:10px;">Status da semana</div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <div style="width:7px;height:7px;border-radius:50%;background:{GREEN};flex-shrink:0;"></div>
        <div style="font-size:12px;color:{TEXT};">Receita <b>+6,2%</b> vs meta</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <div style="width:7px;height:7px;border-radius:50%;background:{ORANGE};flex-shrink:0;"></div>
        <div style="font-size:12px;color:{TEXT};">Renovações abaixo da média</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <div style="width:7px;height:7px;border-radius:50%;background:{PURPLE};flex-shrink:0;"></div>
        <div style="font-size:12px;color:{TEXT};">Score de cadastros crescendo</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:7px;height:7px;border-radius:50%;background:{PINK};flex-shrink:0;"></div>
        <div style="font-size:12px;color:{TEXT};">Compra rápida: queda de falhas</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10.5px;color:{MUTED};text-align:center;'>"
                f"Atualizado em {TODAY.strftime('%d/%m/%Y')}</div>",
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-bottom:1.6rem;">
  <div style="font-family:'Aconchego','Georgia',serif; font-size:30px;
              color:{TEXT}; line-height:1.2; font-weight:normal;">
    Report Semanal de Performance
  </div>
  <div style="font-size:13px; color:{MUTED}; margin-top:5px;">
    Semana de referência:
    <span style="color:{TEXT}; font-family:'JetBrains Mono',monospace;">{week_sel}</span>
    &nbsp;·&nbsp;
    Gerado em {TODAY.strftime('%d de %B de %Y')}
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰  Receita",
    "📡  Canais",
    "👥  Audiência",
    "📝  Cadastros",
    "🛒  Checkout",
])


# ───────────────────────────────────────────────────────────────
#  TAB 1 — RECEITA
# ───────────────────────────────────────────────────────────────
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    drev = (REV_CW - REV_PW) / REV_PW * 100
    dtrx = (TRX_CW - TRX_PW) / TRX_PW * 100
    dtk  = (TK_CW  - TK_PW)  / TK_PW  * 100
    darr = (ARR - ARR_PW)     / ARR_PW  * 100
    with c1: st.markdown(kpi("Receita Total",   fmt_brl(REV_CW), drev,  accent=PINK),   unsafe_allow_html=True)
    with c2: st.markdown(kpi("Transações",      f"{TRX_CW:,}",   dtrx,  accent=PURPLE), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Ticket Médio",    fmt_brl(TK_CW),  dtk,   accent=ORANGE), unsafe_allow_html=True)
    with c4: st.markdown(kpi("ARR Total",       fmt_brl(ARR),    darr,  accent=PURPLE), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Revenue trend + Mix
    ca, cb = st.columns([3, 1])

    with ca:
        section("Receita semanal — evolução e comparativo YoY")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=WEEKS, y=rev_yoy, name="2025",
            marker_color="rgba(255,255,255,0.07)",
            hovertemplate="%{y:,.0f}<extra>2025</extra>",
        ))
        fig.add_trace(go.Scatter(
            x=WEEKS, y=rev, name="2026",
            mode="lines+markers",
            line=dict(color=PINK, width=2.5),
            marker=dict(size=7, color=PINK, line=dict(color="white", width=1.5)),
            fill="tonexty", fillcolor="rgba(206,0,141,0.07)",
            hovertemplate="R$ %{y:,.0f}<extra>2026</extra>",
        ))
        fig.update_layout(**plotly_theme(), height=265, barmode="overlay")
        fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True, config=cfg)

    with cb:
        section("Mix de receita")
        fig_mix = go.Figure(go.Pie(
            labels=["Pontual", "Assinatura"],
            values=[rev_pt[-1], rev_ass[-1]],
            hole=0.62,
            marker=dict(colors=[PINK, PURPLE]),
            textfont=dict(family="JetBrains Mono", size=11),
            hovertemplate="%{label}: R$ %{value:,.0f}<extra></extra>",
        ))
        fig_mix.add_annotation(
            text=(f"<b>{rev_pt[-1]/REV_CW*100:.0f}%</b><br>"
                  f"<span style='font-size:9px'>pontual</span>"),
            x=0.5, y=0.5, showarrow=False,
            font=dict(color=TEXT, size=14, family="JetBrains Mono"),
        )
        fig_mix.update_layout(**plotly_theme(), height=265, showlegend=True,
                               legend=dict(orientation="v", x=0.75, y=0.5,
                                           font=dict(size=11)))
        st.plotly_chart(fig_mix, use_container_width=True, config=cfg)

    # Product table + Subscriptions
    col_p, col_s = st.columns([2, 1])

    with col_p:
        section("Performance por produto — semana atual")
        rows = ""
        for _, r in df_prods.iterrows():
            cv = r["conv"] * 100
            if   cv >= 70: badge = f'<span class="bg">{cv:.1f}%</span>'
            elif cv < 55:  badge = f'<span class="bo">{cv:.1f}%</span>'
            else:          badge = f'<span class="bp">{cv:.1f}%</span>'
            rows += (f"<tr><td>{r['name']}</td>"
                     f"<td class='mono'>{fmt_brl(r['price'])}</td>"
                     f"<td class='mono'>{r['ini']:,}</td>"
                     f"<td class='mono'>{r['conc']:,}</td>"
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
        subs_items = [
            ("Nova ARR (média 4 sem.)", fmt_brl(sum(new_arr[-4:]) / 4), TEXT),
            ("Taxa de renovação (sem.)", f"{RENEW_WEEK*100:.1f}%",
             GREEN if RENEW_WEEK >= 0.82 else ORANGE),
            ("Taxa renovação acum. 12m", f"{RENEW_12M*100:.1f}%", TEXT),
            ("Venc. próx. 30 dias",  str(SUBS_VENCE['30d']), ORANGE),
            ("Venc. próx. 60 dias",  str(SUBS_VENCE['60d']), ORANGE),
            ("Venc. próx. 90 dias",  str(SUBS_VENCE['90d']), MUTED),
        ]
        for lbl, val, color in subs_items:
            st.markdown(f"""<div class="band">
              <div class="band-label">{lbl}</div>
              <div class="band-val" style="color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)

        fig_ren = go.Figure(go.Scatter(
            x=WEEKS, y=[r * 100 for r in renew_trend],
            mode="lines+markers",
            line=dict(color=PURPLE, width=2),
            marker=dict(size=5, color=PURPLE),
            fill="tozeroy", fillcolor="rgba(118,6,129,0.10)",
            hovertemplate="%{y:.1f}%<extra></extra>",
        ))
        fig_ren.add_hline(y=RENEW_12M * 100, line_dash="dot", line_color=MUTED,
                          annotation_text="média 12m",
                          annotation_font_color=MUTED, annotation_font_size=10)
        fig_ren.update_layout(**plotly_theme(), height=165, showlegend=False,
                               margin=dict(l=0, r=0, t=8, b=0))
        fig_ren.update_yaxes(ticksuffix="%", range=[65, 100])
        st.plotly_chart(fig_ren, use_container_width=True, config=cfg)

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
    with kc1: st.markdown(kpi("Receita — Orgânico",     fmt_brl(ch_rev[0]),  4.2,  accent=PURPLE), unsafe_allow_html=True)
    with kc2: st.markdown(kpi("Receita — E-mail",       fmt_brl(ch_rev[1]), -1.8,  accent=PINK),   unsafe_allow_html=True)
    with kc3: st.markdown(kpi("Receita — Direto",       fmt_brl(ch_rev[2]),  2.1,  accent=ORANGE), unsafe_allow_html=True)
    with kc4: st.markdown(kpi("Receita — Alertas",      fmt_brl(ch_rev[5]),  8.4,  accent=PURPLE), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    cb1, cb2 = st.columns([2, 1])
    with cb1:
        section("Receita por canal")
        fig_chr = go.Figure(go.Bar(
            x=CHS, y=ch_rev,
            marker_color=CHS_PAL,
            text=[fmt_brl(r) for r in ch_rev],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color=TEXT),
            hovertemplate="%{x}: R$ %{y:,.0f}<extra></extra>",
        ))
        fig_chr.update_layout(**plotly_theme(), height=270, bargap=0.35,
                               yaxis=dict(visible=False))
        st.plotly_chart(fig_chr, use_container_width=True, config=cfg)

    with cb2:
        section("Conv. por canal (R$/Sessão)")
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
        fig_ccv.update_layout(**plotly_theme(), height=270,
                               xaxis=dict(visible=False),
                               yaxis=dict(gridcolor="transparent"))
        st.plotly_chart(fig_ccv, use_container_width=True, config=cfg)

    section("Detalhamento por canal")
    rows = ""
    ch_deltas = [4.2, -1.8, 2.1, -3.4, 6.7, 8.4]
    for ch, rev_v, sess, conv, delta_v in zip(CHS, ch_rev, ch_sess, ch_conv, ch_deltas):
        b = (f'<span class="bg">▲ {delta_v:.1f}%</span>' if delta_v > 0
             else f'<span class="bo">▼ {abs(delta_v):.1f}%</span>')
        rows += (f"<tr><td><b>{ch}</b></td>"
                 f"<td class='mono'>{fmt_brl(rev_v)}</td>"
                 f"<td class='mono'>{fmt_k(sess)}</td>"
                 f"<td class='mono'>{conv:.2f}%</td>"
                 f"<td>{b}</td></tr>")
    st.markdown(f"""
    <table class="dtable">
      <thead><tr>
        <th>Canal</th><th>Receita</th><th>Sessões</th>
        <th>Conversão (R$/Sessão)</th><th>vs Sem. Ant.</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    ce1, ce2 = st.columns(2)
    with ce1:
        section("E-mail marketing")
        for lbl, val in [("Emails enviados","48.200"),("Sessões geradas","11.200"),
                         ("CTR médio","4,84%"),("Receita atribuída", fmt_brl(ch_rev[1]))]:
            st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                        f'<div class="band-val">{val}</div></div>', unsafe_allow_html=True)

    with ce2:
        section("Alertas de trânsitos")
        for lbl, val in [("Alertas enviados","62.400"),("Sessões geradas","5.200"),
                         ("CTR médio","8,33%"),("Receita atribuída", fmt_brl(ch_rev[5]))]:
            st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                        f'<div class="band-val">{val}</div></div>', unsafe_allow_html=True)

    section("Google Search Console — evolução semanal")
    cg1, cg2 = st.columns(2)
    with cg1:
        fig_gsc = go.Figure()
        fig_gsc.add_trace(go.Scatter(
            x=WEEKS, y=gsc_imp, name="Impressões",
            mode="lines+markers",
            line=dict(color=PURPLE, width=2),
            marker=dict(size=5),
            yaxis="y",
        ))
        fig_gsc.add_trace(go.Scatter(
            x=WEEKS, y=gsc_clk, name="Cliques",
            mode="lines+markers",
            line=dict(color=PINK, width=2),
            marker=dict(size=5),
            yaxis="y2",
        ))
        layout2 = {**plotly_theme(), "height": 230,
                   "yaxis": dict(title="Impressões", gridcolor="rgba(255,255,255,.06)",
                                 tickformat=",.0f"),
                   "yaxis2": dict(title="Cliques", overlaying="y", side="right",
                                  gridcolor="transparent", tickformat=",.0f")}
        fig_gsc.update_layout(**layout2)
        st.plotly_chart(fig_gsc, use_container_width=True, config=cfg)

    with cg2:
        fig_pos = go.Figure(go.Scatter(
            x=WEEKS, y=gsc_pos,
            mode="lines+markers",
            line=dict(color=ORANGE, width=2.5),
            marker=dict(size=6, color=ORANGE),
            fill="tozeroy", fillcolor="rgba(239,77,3,.08)",
            hovertemplate="Posição %{y:.1f}<extra></extra>",
        ))
        fig_pos.update_layout(**plotly_theme(), height=230, showlegend=False,
                               title=dict(text="Posição média — quanto menor, melhor",
                                          font=dict(size=11, color=MUTED)))
        fig_pos.update_yaxes(autorange="reversed", title="Posição média")
        st.plotly_chart(fig_pos, use_container_width=True, config=cfg)


# ───────────────────────────────────────────────────────────────
#  TAB 3 — AUDIÊNCIA
# ───────────────────────────────────────────────────────────────
with tab3:
    ka1, ka2, ka3, ka4 = st.columns(4)
    dsess = (SESS_CW - SESS_PW) / SESS_PW * 100
    with ka1: st.markdown(kpi("Sessões",            fmt_k(SESS_CW),        dsess, accent=PURPLE), unsafe_allow_html=True)
    with ka2: st.markdown(kpi("Unique Visitors",    fmt_k(UV_CW),           8.2,  accent=PINK),   unsafe_allow_html=True)
    with ka3: st.markdown(kpi("Taxa de Engajamento",f"{ENG_RATE*100:.1f}%", 1.4,  accent=ORANGE), unsafe_allow_html=True)
    with ka4: st.markdown(kpi("Páginas / Sessão",   f"{PPG:.1f}",           0.2,  accent=PURPLE), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    ca1, ca2 = st.columns([3, 1])
    with ca1:
        section("Sessões — evolução e comparativo YoY")
        fig_sess = go.Figure()
        fig_sess.add_trace(go.Bar(
            x=WEEKS, y=sess_yoy, name="2025",
            marker_color="rgba(255,255,255,0.07)",
        ))
        fig_sess.add_trace(go.Scatter(
            x=WEEKS, y=sess_wk, name="2026",
            mode="lines+markers",
            line=dict(color=PURPLE, width=2.5),
            marker=dict(size=7, color=PURPLE, line=dict(color="white", width=1.5)),
            hovertemplate="%{y:,.0f}<extra>2026</extra>",
        ))
        fig_sess.update_layout(**plotly_theme(), height=265, barmode="overlay")
        fig_sess.update_yaxes(tickformat=",")
        st.plotly_chart(fig_sess, use_container_width=True, config=cfg)

    with ca2:
        section("Audiência por canal")
        fig_caud = go.Figure(go.Pie(
            labels=CHS, values=ch_sess,
            hole=0.55,
            marker=dict(colors=CHS_PAL),
            textfont=dict(size=10),
            hovertemplate="%{label}: %{value:,}<extra></extra>",
        ))
        fig_caud.update_layout(**plotly_theme(), height=265,
                                legend=dict(font=dict(size=10), orientation="v"))
        st.plotly_chart(fig_caud, use_container_width=True, config=cfg)

    section("Perfil da audiência — três dimensões")
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
                  <div style="width:100%;height:4px;background:rgba(255,255,255,.07);border-radius:2px;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    dim_block(cd1, "Dim 1 — Relacionamento c/ cadastro", [
        ("Não cadastrados",      49200, MUTED),
        ("Cadastrados não-log.", 27400, ORANGE),
        ("Cadastrados logados",  17400, PURPLE),
    ])
    dim_block(cd2, "Dim 2 — Relacionamento comercial", [
        ("Nunca compraram",       44200, MUTED),
        ("Já compraram (n-ass.)", 26800, ORANGE),
        ("Assinantes ativos",     23000, PURPLE),
    ])
    dim_block(cd3, "Dim 3 — Frequência de visita", [
        ("Novos usuários",  28400, ORANGE),
        ("Recorrentes",     52200, PINK),
        ("Reativados",      13400, PURPLE),
    ])

    section("Conexão audiência → receita")
    st.markdown(f"""<div class="info-box">
      💡 <b>Assinantes ativos</b> representam 24,5% das sessões mas respondem por
      <b>35,1% da receita total</b>. Usuários reativados convertem 2,3× mais que novos —
      campanhas de reativação com ROI positivo.
    </div>""", unsafe_allow_html=True)

    seg_data = {
        "Segmento":   ["Novos usuários", "Recorrentes", "Reativados", "Assinantes"],
        "Sessões":    [28400, 52200, 13400, 23000],
        "Conv. (%)":  [1.2, 2.8, 4.1, 5.9],
        "Receita":    [8400, 42600, 18200, 25000],
    }
    fig_seg = go.Figure()
    seg_colors = [ORANGE, PINK, PURPLE, GREEN]
    for i, (seg, cv) in enumerate(zip(seg_data["Segmento"], seg_data["Conv. (%)"])):
        fig_seg.add_trace(go.Bar(
            name=seg, x=[seg], y=[cv],
            marker_color=seg_colors[i],
            text=[f"{cv:.1f}%"], textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11),
        ))
    fig_seg.update_layout(**plotly_theme(), height=240, showlegend=False,
                           barmode="group", bargap=0.38)
    fig_seg.update_yaxes(ticksuffix="%", title="Taxa de Conversão")
    st.plotly_chart(fig_seg, use_container_width=True, config=cfg)


# ───────────────────────────────────────────────────────────────
#  TAB 4 — CADASTROS
# ───────────────────────────────────────────────────────────────
with tab4:
    kr1, kr2, kr3, kr4 = st.columns(4)
    with kr1: st.markdown(kpi("Cadastros na semana",     "3.240",               6.8,  accent=PURPLE), unsafe_allow_html=True)
    with kr2: st.markdown(kpi("Score médio",             f"{REG_SCORE:.1f}/100", 3.1,  accent=PINK),   unsafe_allow_html=True)
    with kr3: st.markdown(kpi("Conv. cadastro→venda",    "14,2%",               1.4,  accent=ORANGE), unsafe_allow_html=True)
    with kr4: st.markdown(kpi("Cadastros Completos",     "8,4%",               -0.7,  accent=PURPLE), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    cf1, cf2 = st.columns([2, 1])

    with cf1:
        section("Funil de cadastro")
        FCOLORS = [PURPLE, "#8a0a9a", PINK, "#d4336b", ORANGE]
        total_v = REG_FUNNEL[0][1]
        for i, (label, val, conv) in enumerate(REG_FUNNEL):
            pct  = val / total_v * 100
            color = FCOLORS[i]
            sub  = (f'<div class="frow-sub">{conv:.1f}% da etapa anterior</div>'
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
            connector=dict(line=dict(color="rgba(255,255,255,0.08)", width=1)),
            textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
        ))
        fig_fnn.update_layout(**plotly_theme(), height=280,
                               margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_fnn, use_container_width=True, config=cfg)

    with cf2:
        section("Qualidade dos cadastros")
        quality = [
            ("Básico (20 pts)",          820,  MUTED),
            ("Intermediário (21–55)",    1140,  ORANGE),
            ("Avançado (56–90)",         1010,  PURPLE),
            ("Completo (91–100)",         270,  PINK),
        ]
        total_q = sum(v for _, v, _ in quality)
        for name, qty, color in quality:
            pct = qty / total_q * 100
            st.markdown(f"""
            <div class="band" style="flex-direction:column;gap:6px;align-items:flex-start;">
              <div style="display:flex;justify-content:space-between;width:100%;">
                <div style="font-size:12.5px;">{name}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{color};">
                  {qty:,} <span style="color:{MUTED};font-size:10px;">{pct:.0f}%</span>
                </div>
              </div>
              <div style="width:100%;height:5px;background:rgba(255,255,255,.07);border-radius:2px;">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        fig_sc = go.Figure(go.Scatter(
            x=WEEKS, y=score_trend,
            mode="lines+markers",
            line=dict(color=PINK, width=2.5),
            marker=dict(size=6, color=PINK),
            fill="tozeroy", fillcolor="rgba(206,0,141,0.08)",
            hovertemplate="Score: %{y:.1f}<extra></extra>",
        ))
        fig_sc.add_hline(y=60, line_dash="dot", line_color=MUTED,
                          annotation_text="meta 60",
                          annotation_font_color=MUTED, annotation_font_size=10)
        fig_sc.update_layout(**plotly_theme(), height=190, showlegend=False,
                              margin=dict(l=0, r=0, t=8, b=0),
                              title=dict(text="Evolução do score médio",
                                         font=dict(size=11, color=MUTED)))
        fig_sc.update_yaxes(range=[50, 78])
        st.plotly_chart(fig_sc, use_container_width=True, config=cfg)

    section("Cadastros por canal de origem")
    rows = ""
    for ch, qty, score_avg, conv_v in REG_CH:
        sb = (f'<span class="bg">{score_avg:.1f}</span>' if score_avg >= 65
              else f'<span class="bp">{score_avg:.1f}</span>' if score_avg >= 55
              else f'<span class="bo">{score_avg:.1f}</span>')
        rows += (f"<tr><td><b>{ch}</b></td>"
                 f"<td class='mono'>{qty:,}</td>"
                 f"<td class='mono'>{qty/3240*100:.1f}%</td>"
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

    st.markdown("<br/>", unsafe_allow_html=True)
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
    with kch1: st.markdown(kpi("Carrinhos iniciados",   f"{4820+2140:,}",            3.2,  accent=PURPLE), unsafe_allow_html=True)
    with kch2: st.markdown(kpi("Conv. carrinho trad.",  f"{CART_CONV_TRAD*100:.1f}%",-0.8, accent=PINK),   unsafe_allow_html=True)
    with kch3: st.markdown(kpi("Conv. compra rápida",  f"{CART_CONV_QUICK*100:.1f}%",1.4,  accent=ORANGE), unsafe_allow_html=True)
    with kch4: st.markdown(kpi("Ticket médio geral",    fmt_brl(84.6),               2.1,  accent=PURPLE), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    cc1, cc2 = st.columns(2)

    # ── Traditional cart funnel ─────────────────────────────────
    with cc1:
        section("Funil — Carrinho tradicional")
        fig_ct = go.Figure(go.Funnel(
            y=[r[0] for r in CART_TRAD],
            x=[r[1] for r in CART_TRAD],
            textinfo="value+percent initial",
            marker=dict(color=[PURPLE, "#8a0a9a", PINK, "#d4336b", ORANGE]),
            connector=dict(line=dict(color="rgba(255,255,255,0.08)", width=1)),
            textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
        ))
        fig_ct.update_layout(**plotly_theme(), height=290,
                              margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_ct, use_container_width=True, config=cfg)

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
        section("Funil — Compra rápida")
        fig_cq = go.Figure(go.Funnel(
            y=[r[0] for r in CART_QUICK[:4]],
            x=[r[1] for r in CART_QUICK[:4]],
            textinfo="value+percent initial",
            marker=dict(color=[PINK, "#d4336b", ORANGE, "#5b2d8e"]),
            connector=dict(line=dict(color="rgba(255,255,255,0.08)", width=1)),
            textfont=dict(family="JetBrains Mono", size=11, color=TEXT),
        ))
        fig_cq.update_layout(**plotly_theme(), height=290,
                              margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_cq, use_container_width=True, config=cfg)

        st.markdown(f"""<div class="alert-box">
          ⚠️ <b>{CART_QUICK[4][1]} falhas de processamento</b>
          ({CART_QUICK[4][2]:.1f}% dos inícios).
          {CART_QUICK[5][1]} usuários migraram para o carrinho tradicional
          ({CART_QUICK[5][2]:.1f}% das falhas).
        </div>""", unsafe_allow_html=True)

        section("Recuperação de carrinhos abandonados")
        rec_items = [
            ("Carrinhos elegíveis",   f"{ABAND_ELIG:,}",             TEXT),
            ("Mensagens enviadas",    f"{MSGS_SENT:,}",              TEXT),
            ("Carrinhos recuperados", f"{RECOVERED:,}",              GREEN),
            ("Taxa de recuperação",   f"{REC_RATE*100:.1f}%",        GREEN),
            ("Receita recuperada",    fmt_brl(REC_REV),              PINK),
        ]
        for lbl, val, color in rec_items:
            st.markdown(f'<div class="band"><div class="band-label">{lbl}</div>'
                        f'<div class="band-val" style="color:{color};">{val}</div>'
                        f'</div>', unsafe_allow_html=True)

    # ── Payment + Product conversion ────────────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    cp1, cp2 = st.columns(2)

    with cp1:
        section("Conversão por meio de pagamento")
        pay_labels  = [p[0] for p in PAYMENTS]
        pay_conc    = [p[2] * 100 for p in PAYMENTS]
        pay_aband   = [p[3] * 100 for p in PAYMENTS]
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
        fig_pay.update_layout(**plotly_theme(), height=270, barmode="stack", bargap=0.35)
        fig_pay.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig_pay, use_container_width=True, config=cfg)

    with cp2:
        section("Conversão por produto — após adição ao carrinho")
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
        fig_pcv.update_layout(**plotly_theme(), height=270, bargap=0.3,
                               xaxis=dict(tickangle=-35, tickfont=dict(size=9)),
                               yaxis=dict(ticksuffix="%"))
        st.plotly_chart(fig_pcv, use_container_width=True, config=cfg)

    # ── Upsell vitrine ──────────────────────────────────────────
    section("Performance da vitrine de upsell (carrinho)")
    cu1, cu2, cu3, cu4 = st.columns(4)
    with cu1: st.markdown(kpi("Taxa de adição",     "31,4%",         2.8, accent=PURPLE), unsafe_allow_html=True)
    with cu2: st.markdown(kpi("Impacto no ticket",  "+R$ 18,60",  None,   accent=PINK),   unsafe_allow_html=True)
    with cu3: st.markdown(kpi("Carrinhos c/ upsell","948",         None,   accent=ORANGE), unsafe_allow_html=True)
    with cu4: st.markdown(kpi("Receita incremental",fmt_brl(17633), None,  accent=PURPLE), unsafe_allow_html=True)

    # ── Segmentation deep-dives ─────────────────────────────────
    section("Segmentações de conversão")
    cs1, cs2, cs3 = st.columns(3)

    seg_comercial = [
        ("Novos compradores",      38.4, ORANGE),
        ("Compradores recorrentes",52.1, PINK),
        ("Assinantes ativos",      61.8, PURPLE),
    ]
    seg_engagement = [
        ("Usuários novos no site",  28.2, ORANGE),
        ("Usuários recorrentes",    49.7, PINK),
        ("Usuários reativados",     64.3, PURPLE),
    ]
    seg_safra = [
        ("Cadastro 2026",          38.1, MUTED),
        ("Cadastro 2025",          44.8, ORANGE),
        ("Cadastro 2024",          51.3, PINK),
        ("Cadastro ≤ 2023",        58.9, PURPLE),
    ]

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
                  <div style="width:100%;height:4px;background:rgba(255,255,255,.07);border-radius:2px;">
                    <div style="width:{bar_w}%;height:100%;background:{color};border-radius:2px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    conv_seg_block(cs1, "Por perfil comercial",    seg_comercial)
    conv_seg_block(cs2, "Por perfil de engajamento", seg_engagement)
    conv_seg_block(cs3, "Por safra de cadastro",   seg_safra)
