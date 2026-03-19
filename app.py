
import streamlit as st
import streamlit.components.v1
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retirement Planning | The Mountain Path Academy",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── THEME & STYLES ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --darkblue: #003366;
    --midblue:  #004d80;
    --card:     #112240;
    --gold:     #FFD700;
    --lightblue:#ADD8E6;
    --txt:      #e6f1ff;
    --muted:    #a8b2d8;
    --grn:      #28a745;
    --red:      #dc3545;
    --bg1:      #1a2332;
    --bg2:      #243447;
    --bg3:      #2a3f5f;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--txt);
}

.stApp {
    background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 50%, var(--bg3) 100%);
    min-height: 100vh;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, var(--card) 100%) !important;
    border-right: 1px solid rgba(255,215,0,0.15);
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--gold) !important;
    font-family: 'Playfair Display', serif;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(255,215,0,0.25);
    padding-bottom: 6px;
    margin-top: 20px;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--txt) !important;
}

/* ─── ALL text globally — force bright on dark bg ─── */
p, span, li, div { color: inherit; }

/* ─── Captions — override Streamlit's near-invisible default ─── */
[data-testid="stCaptionContainer"] p,
.stCaption, .stCaption p,
[class*="caption"] {
    color: var(--lightblue) !important;
    font-size: 0.82rem !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}

/* ─── Markdown headings — force visibility (main area only) ─── */
.stMarkdown h1 { color: var(--gold) !important; font-family: 'Playfair Display', serif; }
.stMarkdown h2 { color: var(--gold) !important; font-family: 'Playfair Display', serif; }
.stMarkdown h3 { color: var(--lightblue) !important; }
/* h4 scoped to main content — NOT sidebar, to avoid overriding widget labels */
[data-testid="stMain"] .stMarkdown h4,
section[data-testid="stMain"] h4 {
    color: #c8d8f0 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-top: 16px !important;
}
.stMarkdown p  { color: var(--txt) !important; line-height: 1.7; }
.stMarkdown strong { color: var(--gold) !important; }
.stMarkdown li { color: var(--txt) !important; line-height: 1.8; }

/* ─── Info / Warning / Success boxes ─── */
[data-testid="stInfo"] {
    background: rgba(0,77,128,0.5) !important;
    border-left: 4px solid var(--lightblue) !important;
    border-radius: 8px !important;
    color: var(--txt) !important;
}
[data-testid="stInfo"] p,
[data-testid="stInfo"] span { color: var(--txt) !important; }

[data-testid="stWarning"] {
    background: rgba(255,193,7,0.15) !important;
    border-left: 4px solid #FFC107 !important;
    border-radius: 8px !important;
}
[data-testid="stWarning"] p { color: #ffe082 !important; }

[data-testid="stSuccess"] {
    background: rgba(40,167,69,0.15) !important;
    border-left: 4px solid var(--grn) !important;
    border-radius: 8px !important;
}
[data-testid="stSuccess"] p { color: #a8e6b8 !important; }

/* ─── Sliders & Inputs ─── */
[data-testid="stSlider"] > div > div > div {
    background: var(--gold) !important;
}

/* ─── Sidebar widget labels — force lightblue, never gold ─── */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] label span,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--lightblue) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}
/* Slider value bubble (the "7.00" above the thumb) — gold only in sidebar */
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    color: var(--gold) !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
}
/* Main area slider labels — white-blue, NOT gold */
[data-testid="stMain"] [data-testid="stWidgetLabel"] p,
[data-testid="stMain"] [data-testid="stWidgetLabel"] span {
    color: var(--lightblue) !important;
    font-weight: 500 !important;
}
/* Main area slider value display — gold */
[data-testid="stMain"] [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    color: var(--gold) !important;
    font-weight: 700 !important;
}

/* ─── Metric Cards ─── */
[data-testid="stMetric"] {
    background: rgba(17,34,64,0.85);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
[data-testid="stMetricLabel"] { color: var(--lightblue) !important; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: var(--gold) !important; font-family: 'Playfair Display', serif; font-size: 1.6rem; }
[data-testid="stMetricDelta"] { font-size: 0.78rem; }

/* ─── Sub-tabs (used inside sections like TVM, Case Studies etc.) ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.3);
    border-radius: 8px;
    padding: 3px;
    gap: 3px;
    flex-wrap: nowrap;
}
.stTabs [data-baseweb="tab"] {
    color: #c8d8f0 !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    border-radius: 6px;
    padding: 6px 12px;
    background: rgba(0,20,50,0.5) !important;
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    background: var(--darkblue) !important;
    color: var(--gold) !important;
    border: 1px solid rgba(255,215,0,0.4) !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 16px !important;
}

/* ─── Expanders ─── */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary,
[data-testid="stExpanderToggleIcon"],
details > summary {
    background: rgba(0,51,102,0.55) !important;
    border: 1px solid rgba(173,216,230,0.3) !important;
    border-radius: 8px !important;
    color: #e0eeff !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
}
.streamlit-expanderHeader:hover,
[data-testid="stExpander"] summary:hover {
    background: rgba(0,77,128,0.7) !important;
    border-color: rgba(255,215,0,0.4) !important;
}
/* Expander content area */
[data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
    background: rgba(10,22,40,0.6) !important;
    border: 1px solid rgba(173,216,230,0.15) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 12px !important;
}

/* ─── Dividers ─── */
hr { border-color: rgba(255,215,0,0.15) !important; }

/* ─── DataFrames / Tables ─── */
.stDataFrame { border: 1px solid rgba(255,215,0,0.15) !important; border-radius: 8px; }
.stDataFrame th { background: var(--darkblue) !important; color: var(--gold) !important; font-weight: 600 !important; }
.stDataFrame td { background: rgba(17,34,64,0.8) !important; color: var(--txt) !important; }
/* Markdown tables */
.stMarkdown table { border-collapse: collapse; width: 100%; }
.stMarkdown table th { background: rgba(0,51,102,0.8) !important; color: var(--gold) !important; padding: 8px 12px; border: 1px solid rgba(255,215,0,0.2); }
.stMarkdown table td { background: rgba(17,34,64,0.6) !important; color: var(--txt) !important; padding: 7px 12px; border: 1px solid rgba(255,255,255,0.08); }
.stMarkdown table tr:hover td { background: rgba(0,51,102,0.5) !important; }

/* ─── Alerts ─── */
.stAlert { border-radius: 10px; border-left: 4px solid; }

/* ─── Selectbox — full overhaul targeting BaseUI components ─── */
/* The closed box (trigger) */
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child,
[data-testid="stSelectbox"] [data-baseweb="select"] div[class*="control"],
[data-testid="stSelectbox"] div[role="combobox"],
[data-testid="stSelectbox"] div[role="combobox"] > div {
    background: rgba(0, 51, 102, 0.7) !important;
    border: 1px solid rgba(255, 215, 0, 0.45) !important;
    border-radius: 8px !important;
    color: #e6f1ff !important;
}
/* The selected value text inside the closed box */
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div[class*="singleValue"],
[data-testid="stSelectbox"] [data-baseweb="select"] [class*="placeholder"],
[data-testid="stSelectbox"] div[role="combobox"] span {
    color: #e6f1ff !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}
/* Dropdown chevron/arrow */
[data-testid="stSelectbox"] svg {
    fill: #FFD700 !important;
    color: #FFD700 !important;
}
/* The open dropdown list container */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[data-baseweb="menu"],
[data-testid="stSelectbox"] + div,
div[class*="menu"],
div[class*="menuList"] {
    background: #0d1f3c !important;
    border: 1px solid rgba(255, 215, 0, 0.3) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
}
/* Each option item in the dropdown */
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"],
ul[data-baseweb="menu"] li,
div[class*="option"] {
    background: #0d1f3c !important;
    color: #c8d8f0 !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
}
/* Hover state on options */
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"],
div[class*="option"]:hover {
    background: rgba(0, 77, 128, 0.8) !important;
    color: #FFD700 !important;
}
/* Number input +/- buttons */
.stNumberInput button {
    color: var(--gold) !important;
    background: rgba(0, 51, 102, 0.5) !important;
    border-color: rgba(255, 215, 0, 0.3) !important;
}
/* Number input field itself */
.stNumberInput input, .stTextInput input {
    background: rgba(0, 51, 102, 0.4) !important;
    border: 1px solid rgba(255, 215, 0, 0.3) !important;
    color: #e6f1ff !important;
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem !important;
}

/* ─── hide hamburger & Streamlit footer ─── */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def fmt_inr(n, decimals=0):
    """Format number in Indian system: Crores above 1Cr, Lakhs above 1L, else Indian comma."""
    n = float(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1e7:
        return f"{sign}₹{n/1e7:.2f} Cr"
    elif n >= 1e5:
        return f"{sign}₹{n/1e5:.2f} L"
    elif n >= 1e3:
        return f"{sign}₹{n/1e3:.1f}K"
    else:
        return f"{sign}₹{n:,.{decimals}f}"

def fmt_usd(n):
    """Format number in US system with $ symbol."""
    n = float(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1e6:
        return f"{sign}${n/1e6:.2f}M"
    elif n >= 1e3:
        return f"{sign}${n/1e3:.1f}K"
    else:
        return f"{sign}${n:,.0f}"

def pv_annuity(pmt, r, n):
    if r == 0:
        return pmt * n
    return pmt * (1 - (1+r)**-n) / r

def fv_growing_annuity(pmt, g, r, n):
    """FV of growing annuity: pmt grows at g, earns r, over n years."""
    if abs(r - g) < 1e-10:
        return pmt * n * (1+r)**(n-1)
    return pmt * ((1+r)**n - (1+g)**n) / (r - g)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(0,51,102,0.95) 0%, rgba(0,77,128,0.85) 100%);
    border: 1px solid rgba(255,215,0,0.35);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
">
<div style="position:absolute;top:-20px;right:-20px;width:160px;height:160px;
    background:radial-gradient(circle, rgba(255,215,0,0.08) 0%, transparent 70%);border-radius:50%;"></div>
<div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;">
    <span style="font-size:2.4rem;">🏔️</span>
    <div>
        <div style="font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;
            color:#FFD700;letter-spacing:0.02em;line-height:1.1;">
            Retirement Planning Suite
        </div>
        <div style="font-size:0.78rem;color:#ADD8E6;letter-spacing:0.12em;text-transform:uppercase;margin-top:3px;">
            The Mountain Path Academy · World of Finance
        </div>
    </div>
</div>
<div style="font-size:0.82rem;color:#8892b0;max-width:680px;line-height:1.6;">
    A comprehensive, TVM-powered retirement planning model — incorporating savings accumulation,
    corpus estimation, withdrawal modelling, Monte Carlo simulation, and sensitivity analysis.
    Built for students, advisors, and anyone planning their financial future.
</div>
<div style="margin-top:14px;display:flex;gap:20px;flex-wrap:wrap;">
    <a href="https://themountainpathacademy.com" target="_blank" style="color:#FFD700;font-size:0.75rem;text-decoration:none;letter-spacing:0.06em;">
        🌐 themountainpathacademy.com
    </a>
    <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:#ADD8E6;font-size:0.75rem;text-decoration:none;letter-spacing:0.06em;">
        💼 LinkedIn
    </a>
    <a href="https://github.com/trichyravis" target="_blank" style="color:#ADD8E6;font-size:0.75rem;text-decoration:none;letter-spacing:0.06em;">
        💻 GitHub
    </a>
    <span style="color:#8892b0;font-size:0.75rem;">Prof. V. Ravichandran · 28+ Yrs Corporate Finance & Banking</span>
</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── NAVIGATION SETUP (before sidebar so state is ready) ─────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
NAV_SECTIONS = [
    ("dashboard",   "📊", "Dashboard",          "analysis"),
    ("savings",     "📈", "Savings Growth",      "analysis"),
    ("retirement",  "🏦", "Retirement Needs",    "analysis"),
    ("withdrawal",  "💸", "Withdrawal Plan",     "analysis"),
    ("sensitivity", "🔬", "Sensitivity",         "analysis"),
    ("montecarlo",  "🎲", "Monte Carlo",         "education"),
    ("tvm",         "📚", "TVM Basics",          "education"),
    ("casestudies", "🎓", "Case Studies",        "education"),
    ("behavioural", "⚖️", "Behavioural Finance", "education"),
    ("glossary",    "📖", "Glossary & Formulas", "education"),
]
if "active_section" not in st.session_state:
    st.session_state["active_section"] = "dashboard"

def _nav_click(key):
    st.session_state["active_section"] = key

# ═══════════════════════════════════════════════════════════════════════════════
# ─── SIDEBAR INPUTS ───────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 👤 Personal Profile")
    current_age      = st.slider("Current Age", 18, 70, 30, 1)
    retirement_age   = st.slider("Retirement Age", current_age+5, 80, 65, 1)
    life_expectancy  = st.slider("Life Expectancy", retirement_age+5, 100, 90, 1)

    years_to_ret  = retirement_age - current_age
    years_in_ret  = life_expectancy - retirement_age

    st.markdown(f"""
    <div style="background:rgba(0,51,102,0.5);border:1px solid rgba(255,215,0,0.2);
        border-radius:8px;padding:10px 14px;margin:8px 0;font-size:0.78rem;color:#ADD8E6;">
        📅 <b style="color:#FFD700;">{years_to_ret}</b> years to retire &nbsp;|&nbsp;
        🏖️ <b style="color:#FFD700;">{years_in_ret}</b> years in retirement
    </div>""", unsafe_allow_html=True)

    st.markdown("## 💰 Income & Savings")

    # ── Currency selector with auto-reset on switch ──────────────────────────
    # Detect currency change via session_state; reset all numeric inputs to
    # correct defaults so no stale INR value pollutes USD fields or vice-versa.
    if "currency" not in st.session_state:
        st.session_state["currency"] = "₹ INR (Lakhs/Crores)"

    currency = st.selectbox(
        "Currency",
        ["₹ INR (Lakhs/Crores)", "$ USD (Thousands)"],
        key="currency"
    )
    curr_sym  = "₹" if "INR" in currency else "$"
    is_inr    = "INR" in currency

    # Detect switch and reset all dependent widget keys
    _prev_cur = st.session_state.get("_prev_currency", currency)
    if _prev_cur != currency:
        # Wipe all number_input keys so they revert to new-currency defaults
        for _k in ["sb_inc","sb_sav","sb_spc","sb_pen","sb_oth"]:
            if _k in st.session_state:
                del st.session_state[_k]
    st.session_state["_prev_currency"] = currency

    # All min/max/default/step scale with currency
    if is_inr:
        INC  = dict(mn=100_000,    mx=100_000_000, df=1_500_000, st=50_000)
        SAV  = dict(mn=0,          mx=500_000_000, df=500_000,   st=10_000)
        SPC  = dict(mn=50_000,     mx=50_000_000,  df=1_000_000, st=25_000)
        PEN  = dict(mn=0,          mx=5_000_000,   df=120_000,   st=10_000)
        OTH  = dict(mn=0,          mx=5_000_000,   df=0,         st=10_000)
    else:
        INC  = dict(mn=10_000,     mx=2_000_000,   df=75_000,    st=1_000)
        SAV  = dict(mn=0,          mx=5_000_000,   df=25_000,    st=500)
        SPC  = dict(mn=5_000,      mx=1_000_000,   df=50_000,    st=500)
        PEN  = dict(mn=0,          mx=200_000,     df=18_000,    st=500)
        OTH  = dict(mn=0,          mx=200_000,     df=0,         st=500)

    curr_income  = st.number_input(f"Annual Income ({curr_sym})",
                                   INC["mn"], INC["mx"], INC["df"], INC["st"],
                                   key="sb_inc")

    # Human-readable income interpretation (converts raw number to Lakhs/Crores or K/M)
    if is_inr:
        _inc_fmt = f"₹{curr_income/1e5:.2f} Lakhs" if curr_income < 1e7 else f"₹{curr_income/1e7:.2f} Crores"
    else:
        _inc_fmt = f"${curr_income/1e3:.1f}K" if curr_income < 1e6 else f"${curr_income/1e6:.2f}M"
    st.markdown(
        f'<div style="font-size:0.75rem;color:#a8c4e0;margin:-8px 0 8px 2px;font-style:italic;">'
        f'≡ {_inc_fmt} per year</div>',
        unsafe_allow_html=True
    )

    income_growth= st.slider("Income Growth Rate (%)", 0.0, 15.0, 7.0 if is_inr else 3.0, 0.5) / 100
    savings_rate = st.slider("Savings Rate (% of Income)", 1.0, 50.0, 20.0 if is_inr else 15.0, 0.5) / 100
    curr_savings = st.number_input(f"Current Savings ({curr_sym})",
                                   SAV["mn"], SAV["mx"], SAV["df"], SAV["st"],
                                   key="sb_sav")
    if is_inr:
        _sav_fmt = f"₹{curr_savings/1e5:.2f} Lakhs" if curr_savings < 1e7 else f"₹{curr_savings/1e7:.2f} Crores"
    else:
        _sav_fmt = f"${curr_savings/1e3:.1f}K" if curr_savings < 1e6 else f"${curr_savings/1e6:.2f}M"
    st.markdown(
        f'<div style="font-size:0.75rem;color:#a8c4e0;margin:-8px 0 8px 2px;font-style:italic;">'
        f'≡ {_sav_fmt} accumulated so far</div>',
        unsafe_allow_html=True
    )

    # Live savings preview — uses proper Lakhs/Crores or K/M formatting
    _ann_prev = curr_income * savings_rate
    _mon_prev = _ann_prev / 12
    if is_inr:
        _ann_disp = f"₹{_ann_prev/1e5:.2f} L" if _ann_prev < 1e7 else f"₹{_ann_prev/1e7:.2f} Cr"
        _mon_disp = f"₹{_mon_prev/1e3:.2f}K" if _mon_prev >= 1000 else f"₹{_mon_prev:,.0f}"
    else:
        _ann_disp = f"${_ann_prev/1e3:.1f}K" if _ann_prev >= 1000 else f"${_ann_prev:,.0f}"
        _mon_disp = f"${_mon_prev:,.0f}"
    st.markdown(
        f'<div style="background:rgba(0,51,102,0.45);border:1px solid rgba(255,215,0,0.18);'
        f'border-radius:6px;padding:7px 12px;margin-bottom:8px;font-size:0.77rem;color:#ADD8E6;">'
        f'💾 Saves <b style="color:#FFD700;">{_ann_disp}</b>/year'
        f'&nbsp;·&nbsp;<b style="color:#FFD700;">{_mon_disp}</b>/month'
        f'&nbsp;·&nbsp;<span style="color:#c8dff0;">{savings_rate*100:.1f}% of income</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("## 📈 Returns & Inflation")
    pre_ret_return  = st.slider("Pre-Retirement Return (%)", 1.0, 20.0, 12.0 if is_inr else 8.0, 0.5) / 100
    post_ret_return = st.slider("Post-Retirement Return (%)", 1.0, 15.0, 7.0 if is_inr else 5.0, 0.5) / 100
    inflation_rate  = st.slider("Inflation Rate (%)", 0.5, 12.0, 6.0 if is_inr else 3.0, 0.5) / 100
    tax_rate        = st.slider("Tax Rate on Withdrawals (%)", 0.0, 40.0, 20.0 if is_inr else 15.0, 1.0) / 100

    st.markdown("## 🏠 Retirement Spending")
    desired_spending = st.number_input(f"Desired Annual Spending Today ({curr_sym})",
                                       SPC["mn"], SPC["mx"], SPC["df"], SPC["st"],
                                       key="sb_spc")
    if is_inr:
        _spc_fmt = f"₹{desired_spending/1e5:.2f} Lakhs/yr" if desired_spending < 1e7 else f"₹{desired_spending/1e7:.2f} Crores/yr"
    else:
        _spc_fmt = f"${desired_spending/1e3:.1f}K/yr"
    st.markdown(f'<div style="font-size:0.75rem;color:#a8c4e0;margin:-8px 0 8px 2px;font-style:italic;">≡ {_spc_fmt} · Monthly: {curr_sym}{desired_spending/12:,.0f}</div>', unsafe_allow_html=True)

    replacement_ratio= st.slider("Income Replacement Ratio (%)", 40.0, 100.0, 75.0, 5.0) / 100
    pension_income   = st.number_input(f"Annual Pension / Social Security ({curr_sym})",
                                       PEN["mn"], PEN["mx"], PEN["df"], PEN["st"],
                                       key="sb_pen")
    if pension_income > 0:
        if is_inr:
            _pen_fmt = f"₹{pension_income/1e5:.2f} L/yr · ₹{pension_income/12/1000:.1f}K/mo"
        else:
            _pen_fmt = f"${pension_income/1e3:.1f}K/yr · ${pension_income/12:,.0f}/mo"
        st.markdown(f'<div style="font-size:0.75rem;color:#a8c4e0;margin:-8px 0 8px 2px;font-style:italic;">≡ {_pen_fmt}</div>', unsafe_allow_html=True)
    other_income     = st.number_input(f"Other Retirement Income ({curr_sym})",
                                       OTH["mn"], OTH["mx"], OTH["df"], OTH["st"],
                                       key="sb_oth")

    st.markdown("## 🎲 Monte Carlo")
    mc_sims      = st.slider("Simulations", 500, 5000, 1000, 500)
    return_std   = st.slider("Return Volatility (Std Dev %)", 1.0, 25.0, 8.0 if is_inr else 12.0, 1.0) / 100
    inflation_std= st.slider("Inflation Volatility (Std Dev %)", 0.5, 5.0, 1.5, 0.5) / 100

# ═══════════════════════════════════════════════════════════════════════════════
# ─── CORE CALCULATIONS ────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
ann_savings        = curr_income * savings_rate
monthly_savings    = ann_savings / 12
pre_real_ret       = (1 + pre_ret_return) / (1 + inflation_rate) - 1
post_real_ret      = (1 + post_ret_return) / (1 + inflation_rate) - 1

# Spending at retirement (inflation-adjusted)
spending_at_ret    = desired_spending * (1 + inflation_rate) ** years_to_ret
annual_gap         = max(0, spending_at_ret - pension_income - other_income)
# annual_gap_after_tax: gross-up for tax — used ONLY for corpus sizing & withdrawal schedule
# annual_gap is the pre-tax gap shown in Plan Summary (more intuitive)
annual_gap_after_tax = annual_gap / (1 - tax_rate) if tax_rate < 1 else annual_gap

# Required corpus (PV of retirement annuity - real return)
required_corpus    = pv_annuity(annual_gap_after_tax, post_real_ret, years_in_ret)

# Projected savings (FV of current savings + FV of growing annuity)
fv_current         = curr_savings * (1 + pre_ret_return) ** years_to_ret
fv_contributions   = fv_growing_annuity(ann_savings, income_growth, pre_ret_return, years_to_ret)
projected_savings  = fv_current + fv_contributions

surplus_shortfall  = projected_savings - required_corpus
funding_ratio      = projected_savings / required_corpus if required_corpus > 0 else 0
safe_wr            = annual_gap / projected_savings if projected_savings > 0 else 0

# Required monthly savings — use NOMINAL monthly rate (contributions are in nominal ₹, not real ₹)
# Formula: PMT = (FV_target - FV_current_savings) × r_mo / ((1+r_mo)^n - 1)
_r_mo = pre_ret_return / 12
_n_mo = years_to_ret * 12
_fv_curr_nom = curr_savings * (1 + _r_mo) ** _n_mo
if _r_mo > 0 and required_corpus > _fv_curr_nom:
    req_monthly_pmt = (required_corpus - _fv_curr_nom) * _r_mo / ((1 + _r_mo) ** _n_mo - 1)
elif required_corpus <= _fv_curr_nom:
    req_monthly_pmt = 0.0  # existing savings already enough
else:
    req_monthly_pmt = (required_corpus - _fv_curr_nom) / _n_mo

# ─── Year-by-year savings schedule ───
def build_savings_schedule(n_years, start_bal, start_income, income_g, sav_rate, ret):
    rows = []
    bal = start_bal
    inc = start_income
    for yr in range(1, n_years+1):
        age     = current_age + yr
        contrib = inc * sav_rate
        invest_r= bal * ret
        end_bal = bal + contrib + invest_r
        rows.append({"Year": yr, "Age": age,
                     "Beginning Balance": bal,
                     "Annual Income": inc,
                     "Contribution": contrib,
                     "Investment Return": invest_r,
                     "Ending Balance": end_bal})
        bal = end_bal
        inc = inc * (1 + income_g)
    return pd.DataFrame(rows)

savings_df = build_savings_schedule(years_to_ret, curr_savings, curr_income, income_growth, savings_rate, pre_ret_return)

# ─── Withdrawal schedule ───
def build_withdrawal_schedule(corpus, annual_gap_yr1, post_ret, infl, n_yrs, ret_age):
    rows = []
    bal  = corpus
    wd   = annual_gap_yr1
    for yr in range(1, n_yrs+1):
        age    = ret_age + yr - 1
        inv_r  = (bal - wd/2) * post_ret
        end_b  = bal + inv_r - wd
        rows.append({"Year": yr, "Age": age,
                     "Beginning Balance": bal,
                     "Withdrawal": wd,
                     "Investment Return": inv_r,
                     "Ending Balance": max(0, end_b)})
        bal = max(0, end_b)
        wd  = wd * (1 + infl)
    return pd.DataFrame(rows)

withdrawal_df = build_withdrawal_schedule(
    projected_savings, annual_gap_after_tax, post_ret_return, inflation_rate, years_in_ret, retirement_age)

# ─── Monte Carlo ───
@st.cache_data(show_spinner=False)
def run_monte_carlo(curr_sav, ann_sav, inc_g, sav_rt, curr_inc,
                    pre_ret, post_ret, infl, ret_vol, infl_vol,
                    yrs_acc, yrs_ret, req_corpus, n_sims, seed=42):
    rng = np.random.default_rng(seed)
    success, final_corpora = 0, []
    for _ in range(n_sims):
        bal = curr_sav
        inc = curr_inc
        for _ in range(yrs_acc):
            r = rng.normal(pre_ret, ret_vol)
            contrib = inc * sav_rt
            bal = bal * (1 + r) + contrib
            inc = inc * (1 + inc_g)
        fc = bal
        final_corpora.append(fc)
        # retirement phase
        wd = req_corpus / yrs_ret * 0.04  # proxy: 4% SWR
        for _ in range(yrs_ret):
            r = rng.normal(post_ret, ret_vol * 0.6)
            bal = bal * (1 + r) - wd
            wd = wd * (1 + rng.normal(infl, infl_vol))
            if bal <= 0:
                bal = 0
                break
        if bal > 0:
            success += 1
    return success / n_sims * 100, np.array(final_corpora)

success_rate, corpus_dist = run_monte_carlo(
    curr_savings, ann_savings, income_growth, savings_rate, curr_income,
    pre_ret_return, post_ret_return, inflation_rate, return_std, inflation_std,
    years_to_ret, years_in_ret, required_corpus, mc_sims)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── KPI STRIP ────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
fmt = fmt_inr if is_inr else fmt_usd
status_color = "#28a745" if surplus_shortfall >= 0 else "#dc3545"
status_icon  = "✅" if surplus_shortfall >= 0 else "⚠️"

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Projected Corpus", fmt(projected_savings))
c2.metric("Required Corpus",  fmt(required_corpus))
c3.metric("Surplus/(Shortfall)", fmt(surplus_shortfall),
          delta=f"{'+' if surplus_shortfall>=0 else ''}{surplus_shortfall/required_corpus*100:.1f}% vs target",
          delta_color="normal" if surplus_shortfall>=0 else "inverse")
c4.metric("Funding Ratio",   f"{funding_ratio*100:.1f}%",
          delta="On Track" if funding_ratio>=1 else "Action Needed",
          delta_color="normal" if funding_ratio>=1 else "inverse")
c5.metric("Safe Withdrawal Rate", f"{safe_wr*100:.2f}%",
          delta="<4% ✓ Safe" if safe_wr<0.04 else ">4% ⚠️ High")
c6.metric("MC Success Rate",  f"{success_rate:.1f}%",
          delta="High Confidence" if success_rate>=75 else "Review Plan",
          delta_color="normal" if success_rate>=75 else "inverse")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# ─── TWO-ROW NAVIGATION ───────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
active = st.session_state["active_section"]

# ── Row 1: Analysis Tools ─────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
  <span style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:900;
    color:#FFD700;text-shadow:0 0 20px rgba(255,215,0,0.4);">
    📐 Analysis Tools
  </span>
  <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(255,215,0,0.5),transparent);"></div>
</div>""", unsafe_allow_html=True)

r1 = st.columns(5)
for col, (key, emoji, label, _) in zip(r1, [s for s in NAV_SECTIONS if s[3]=="analysis"]):
    with col:
        if active == key:
            st.markdown(
                f'<div style="background:rgba(0,51,102,0.95);border:2px solid #FFD700;'
                f'border-radius:9px;padding:10px 4px;text-align:center;'
                f'box-shadow:0 0 14px rgba(255,215,0,0.35);">'
                f'<div style="font-size:1.15rem;">{emoji}</div>'
                f'<div style="color:#FFD700;font-size:0.73rem;font-weight:700;margin-top:3px;">{label}</div>'
                f'<div style="width:24px;height:3px;background:#FFD700;border-radius:2px;margin:5px auto 0;"></div>'
                f'</div>', unsafe_allow_html=True)
        else:
            st.button(f"{emoji}\n{label}", key=f"nav_{key}",
                      on_click=_nav_click, args=(key,), use_container_width=True)

# ── Row 2: Education & Learning ───────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin:12px 0 8px 0;">
  <span style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:900;
    color:#ADD8E6;text-shadow:0 0 20px rgba(173,216,230,0.35);">
    📚 Education &amp; Learning
  </span>
  <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(173,216,230,0.4),transparent);"></div>
</div>""", unsafe_allow_html=True)

r2 = st.columns(5)
for col, (key, emoji, label, _) in zip(r2, [s for s in NAV_SECTIONS if s[3]=="education"]):
    with col:
        if active == key:
            st.markdown(
                f'<div style="background:rgba(0,30,60,0.95);border:2px solid #ADD8E6;'
                f'border-radius:9px;padding:10px 4px;text-align:center;'
                f'box-shadow:0 0 14px rgba(173,216,230,0.3);">'
                f'<div style="font-size:1.15rem;">{emoji}</div>'
                f'<div style="color:#ADD8E6;font-size:0.73rem;font-weight:700;margin-top:3px;">{label}</div>'
                f'<div style="width:24px;height:3px;background:#ADD8E6;border-radius:2px;margin:5px auto 0;"></div>'
                f'</div>', unsafe_allow_html=True)
        else:
            st.button(f"{emoji}\n{label}", key=f"nav_{key}",
                      on_click=_nav_click, args=(key,), use_container_width=True)

# ── Active section indicator bar ─────────────────────────────────────────────
_sec = next(s for s in NAV_SECTIONS if s[0] == active)
_rc  = "#FFD700" if _sec[3] == "analysis" else "#ADD8E6"
st.markdown(
    f'<div style="border-top:2px solid {_rc};margin:10px 0 18px 0;padding-top:8px;">'
    f'<span style="background:{_rc};color:#001a33;font-size:0.72rem;font-weight:800;'
    f'padding:3px 14px;border-radius:0 0 8px 8px;letter-spacing:0.08em;">'
    f'▼ &nbsp;{_sec[1]} {_sec[2].upper()}'
    f'</span></div>',
    unsafe_allow_html=True
)

# ── Button CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMain"] .stButton > button {
    background: rgba(0,30,60,0.65) !important;
    border: 1px solid rgba(173,216,230,0.3) !important;
    border-radius: 9px !important;
    color: #c8d8f0 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 8px 4px !important;
    white-space: pre-line !important;
    line-height: 1.4 !important;
    min-height: 58px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stMain"] .stButton > button:hover {
    background: rgba(0,51,102,0.9) !important;
    border-color: rgba(255,215,0,0.6) !important;
    color: #FFD700 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(255,215,0,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Section context managers (compatible with all existing `with tab1:` blocks) ─
import contextlib

@contextlib.contextmanager
def _section(name):
    if st.session_state["active_section"] == name:
        yield True
    else:
        yield False

tab1  = _section("dashboard")
tab2  = _section("savings")
tab3  = _section("retirement")
tab4  = _section("withdrawal")
tab5  = _section("sensitivity")
tab6  = _section("montecarlo")
tab7  = _section("tvm")
tab8  = _section("casestudies")
tab9  = _section("behavioural")
tab10 = _section("glossary")

PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG= "rgba(17,34,64,0.0)"
GOLD    = "#FFD700"
LB      = "#ADD8E6"
GRN     = "#28a745"
RED     = "#dc3545"
GRID    = "rgba(255,255,255,0.06)"

def base_layout(title="", h=420, xaxis_extra=None, yaxis_extra=None, **kwargs):
    xax = dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    if xaxis_extra:
        xax.update(xaxis_extra)
    yax = dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    if yaxis_extra:
        yax.update(yaxis_extra)
    layout = dict(
        title=dict(text=title, font=dict(family="Playfair Display", size=16, color=GOLD), x=0.01),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family="DM Sans", color="#e6f1ff", size=11),
        xaxis=xax, yaxis=yax,
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,215,0,0.2)",
                    borderwidth=1, font=dict(size=10)),
        margin=dict(l=50, r=20, t=50, b=40),
        height=h,
    )
    layout.update(kwargs)
    return layout

# ───────────────────────────────────────
# TAB 1 – DASHBOARD
# ───────────────────────────────────────
with tab1:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Savings trajectory chart
        ages    = savings_df["Age"].tolist()
        balances= savings_df["Ending Balance"].tolist()
        req_line= [required_corpus] * len(ages)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages, y=balances, name="Projected Savings",
            line=dict(color=GOLD, width=3), fill="tozeroy",
            fillcolor="rgba(255,215,0,0.08)"))
        fig.add_trace(go.Scatter(x=ages, y=req_line, name="Required Corpus",
            line=dict(color=RED, width=2, dash="dash")))
        # Crossover annotation
        crossover = next((i for i,b in enumerate(balances) if b >= required_corpus), None)
        if crossover is not None:
            fig.add_vline(x=ages[crossover], line_dash="dot", line_color=GRN, opacity=0.7,
                annotation_text=f"Funded at {ages[crossover]}", annotation_font_color=GRN)
        fig.update_layout(**base_layout("Savings Trajectory vs Required Corpus", h=350))
        fig.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)

        # Withdrawal phase
        wd_ages   = withdrawal_df["Age"].tolist()
        wd_bals   = withdrawal_df["Ending Balance"].tolist()
        wd_wds    = withdrawal_df["Withdrawal"].tolist()

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=wd_ages, y=wd_wds, name="Annual Withdrawal",
            marker_color="rgba(173,216,230,0.55)", marker_line_color=LB, marker_line_width=0.5), secondary_y=True)
        fig2.add_trace(go.Scatter(x=wd_ages, y=wd_bals, name="Portfolio Balance",
            line=dict(color=GOLD, width=2.5), fill="tozeroy", fillcolor="rgba(255,215,0,0.06)"), secondary_y=False)
        fig2.update_layout(**base_layout("Retirement Portfolio Drawdown", h=320))
        fig2.update_yaxes(tickformat=".2s", secondary_y=False, title_text="Balance", gridcolor=GRID)
        fig2.update_yaxes(tickformat=".2s", secondary_y=True, title_text="Withdrawal", gridcolor=GRID, showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        # Gauge – Funding Ratio
        gauge_val = min(funding_ratio * 100, 200)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=funding_ratio * 100,
            delta={"reference": 100, "suffix": "%"},
            title={"text": "Funding Ratio", "font": {"size": 14, "color": GOLD,
                                                      "family": "Playfair Display"}},
            number={"suffix": "%", "font": {"size": 32, "color": GOLD}},
            gauge={
                "axis": {"range": [0, 200], "tickcolor": "#8892b0",
                          "tickvals": [0,50,100,150,200],
                          "ticktext": ["0%","50%","100%","150%","200%"]},
                "bar": {"color": GRN if funding_ratio >= 1 else RED, "thickness": 0.3},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 75],   "color": "rgba(220,53,69,0.15)"},
                    {"range": [75, 100], "color": "rgba(255,193,7,0.15)"},
                    {"range": [100, 200],"color": "rgba(40,167,69,0.15)"},
                ],
                "threshold": {"line": {"color": GOLD, "width": 3},
                              "thickness": 0.8, "value": 100}
            }
        ))
        fig_g.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                            height=260, margin=dict(t=30,b=0,l=20,r=20),
                            font=dict(color="#e6f1ff"))
        st.plotly_chart(fig_g, use_container_width=True)

        # Key metrics summary card — built as explicit string to avoid f-string/markdown HTML escaping
        _req_color = "#28a745" if req_monthly_pmt <= monthly_savings else "#dc3545"
        _req_label = "✅ On Track" if req_monthly_pmt <= monthly_savings else "⬆ Need More"

        def _row(label, value, val_color="#e6f1ff", val_weight="500", suffix=""):
            return (
                f'<span style="color:#a8b2d8;font-size:0.76rem;">{label}</span>'
                f'<span style="color:{val_color};text-align:right;font-weight:{val_weight};">'
                f'{value}'
                f'{"<br><small style=color:#8892b0;font-size:0.68rem;>" + suffix + "</small>" if suffix else ""}'
                f'</span>'
            )

        _summary_html = (
            '<div style="background:rgba(0,51,102,0.55);border:1px solid rgba(255,215,0,0.25);'
            'border-radius:12px;padding:18px;font-size:0.8rem;line-height:1.9;">'

            '<div style="color:#FFD700;font-family:Playfair Display,serif;font-size:0.95rem;'
            'margin-bottom:10px;border-bottom:1px solid rgba(255,215,0,0.15);padding-bottom:6px;">'
            '📋 Plan Summary</div>'

            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 8px;">'

            + _row("Annual Savings",        fmt(ann_savings))
            + _row("Monthly Savings",       fmt(monthly_savings))
            + _row("Spending @ Retirement", fmt(spending_at_ret))
            + _row("Annual Gap (pre-tax)",  fmt(annual_gap))
            + _row("Annual Gap (gross-up)", fmt(annual_gap_after_tax), suffix="incl. tax gross-up")
            + _row("Pre-Ret Real Return",
                   f"{pre_real_ret*100:.2f}%",
                   suffix=f"{pre_ret_return*100:.0f}% nominal − {inflation_rate*100:.0f}% inflation")
            + _row("Post-Ret Real Return",
                   f"{post_real_ret*100:.2f}%",
                   suffix=f"{post_ret_return*100:.0f}% nominal − {inflation_rate*100:.0f}% inflation")
            + _row("Req. Monthly (nominal)",
                   f"{fmt(req_monthly_pmt)} &nbsp;<small style='font-weight:400;font-size:0.7rem;'>{_req_label}</small>",
                   val_color=_req_color, val_weight="700")
            + _row("Your Monthly Savings",  fmt(monthly_savings), val_color="#FFD700", val_weight="700")

            + '</div></div>'
        )
        st.markdown(_summary_html, unsafe_allow_html=True)

        # Waterfall – corpus build-up
        st.markdown("<br>", unsafe_allow_html=True)
        fig_wf = go.Figure(go.Waterfall(
            x=["Current Savings FV", "Contribution FV", "Projected Corpus",
               "Required Corpus", "Surplus/Shortfall"],
            measure=["absolute","relative","total","absolute","relative"],
            y=[fv_current, fv_contributions, 0, -required_corpus, 0],
            connector={"line": {"color": "rgba(255,215,0,0.3)"}},
            increasing={"marker": {"color": GRN}},
            decreasing={"marker": {"color": RED}},
            totals={"marker": {"color": GOLD}},
            textposition="outside",
            text=[fmt(fv_current), fmt(fv_contributions), fmt(projected_savings),
                  fmt(required_corpus), fmt(surplus_shortfall)],
            textfont=dict(size=9, color="#e6f1ff")
        ))
        fig_wf.update_layout(**base_layout("Corpus Waterfall", h=280))
        fig_wf.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig_wf, use_container_width=True)

# ───────────────────────────────────────
# TAB 2 – SAVINGS GROWTH
# ───────────────────────────────────────
with tab2:
    st.markdown("### 📈 Year-by-Year Savings Accumulation")
    col1, col2 = st.columns([3, 2])
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=savings_df["Age"], y=savings_df["Ending Balance"],
            name="Savings Balance", fill="tozeroy", line=dict(color=GOLD, width=3),
            fillcolor="rgba(255,215,0,0.07)"))
        fig.add_trace(go.Bar(x=savings_df["Age"], y=savings_df["Contribution"],
            name="Annual Contribution", marker_color="rgba(40,167,69,0.5)",
            yaxis="y2"))
        fig.add_trace(go.Bar(x=savings_df["Age"], y=savings_df["Investment Return"],
            name="Investment Return", marker_color="rgba(173,216,230,0.4)",
            yaxis="y2"))
        fig.update_layout(
            **base_layout("Savings Growth — Contributions vs Investment Returns", h=420,
                          yaxis_extra=dict(title="Portfolio Balance", tickformat=".2s")),
            barmode="stack",
            yaxis2=dict(overlaying="y", side="right", showgrid=False,
                        title="Annual Amount", tickformat=".2s"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Milestone markers
        milestones = {}
        for mult, label in [(100000 if is_inr else 100000,"₹1L/$100K"),
                            (500000 if is_inr else 500000,"₹5L/$500K"),
                            (1000000 if is_inr else 1000000,"₹10L/$1M"),
                            (required_corpus,"Required Corpus")]:
            row = savings_df[savings_df["Ending Balance"] >= mult]
            if not row.empty:
                milestones[label] = int(row.iloc[0]["Age"])

        st.markdown("""
        <div style="background:rgba(0,51,102,0.5);border:1px solid rgba(255,215,0,0.2);
            border-radius:12px;padding:16px;margin-bottom:16px;">
        <div style="color:#FFD700;font-family:'Playfair Display';margin-bottom:10px;">🏁 Wealth Milestones</div>
        """, unsafe_allow_html=True)
        for label, age in milestones.items():
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
                <span style="color:#8892b0;font-size:0.78rem;">{label}</span>
                <span style="color:#ADD8E6;font-weight:600;">Age {age}</span></div>""",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Compound growth driver pie
        total_contrib = savings_df["Contribution"].sum()
        total_invest  = savings_df["Investment Return"].sum()
        fig_pie = go.Figure(go.Pie(
            labels=["Contributions", "Investment Returns"],
            values=[total_contrib, total_invest],
            marker=dict(colors=[GRN, GOLD]),
            hole=0.55,
            textfont=dict(size=11, color="white")
        ))
        fig_pie.add_annotation(text=f"Power of<br>Compounding",
            x=0.5, y=0.5, font=dict(size=11, color=GOLD, family="Playfair Display"),
            showarrow=False)
        fig_pie.update_layout(**base_layout("Wealth Driver Breakdown", h=280))
        fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Data table
    with st.expander("📄 View Full Savings Schedule"):
        disp = savings_df.copy()
        for col in ["Beginning Balance","Annual Income","Contribution","Investment Return","Ending Balance"]:
            disp[col] = disp[col].apply(lambda x: f"{x:,.0f}")
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ───────────────────────────────────────
# TAB 3 – RETIREMENT NEEDS
# ───────────────────────────────────────
with tab3:
    st.markdown("### 🏦 Retirement Corpus Estimation")
    col1, col2, col3 = st.columns(3)

    # Three methods
    corpus_pv    = required_corpus
    corpus_25x   = annual_gap_after_tax * 25
    corpus_30x   = annual_gap_after_tax * 30
    corpus_33x   = annual_gap_after_tax * 33

    col1.metric("PV Annuity Method", fmt(corpus_pv), help="Present value of inflation-adjusted withdrawals")
    col2.metric("25× Rule (4% SWR)", fmt(corpus_25x), help="Traditional safe withdrawal rule")
    col3.metric("30× Rule (3.3% SWR)", fmt(corpus_30x), help="Conservative for early retirees")

    # Comparison bar
    methods     = ["PV Annuity", "25x Rule", "30x Rule", "33x Rule", "Projected Savings"]
    values      = [corpus_pv, corpus_25x, corpus_30x, corpus_33x, projected_savings]
    colors      = [GOLD, LB, LB, LB, GRN if projected_savings >= corpus_pv else RED]

    fig = go.Figure(go.Bar(
        x=methods, y=values, marker_color=colors,
        text=[fmt(v) for v in values], textposition="outside",
        textfont=dict(size=10, color="#e6f1ff")
    ))
    fig.add_hline(y=projected_savings, line_dash="dash", line_color=GRN,
                  annotation_text="Your Projected Savings", annotation_font_color=GRN)
    fig.update_layout(**base_layout("Corpus Requirements — Multiple Methods", h=380))
    fig.update_yaxes(tickformat=".2s")
    st.plotly_chart(fig, use_container_width=True)

    # Annuity sensitivity to return rate
    st.markdown("#### Corpus vs Post-Retirement Return Rate")
    ret_range  = np.linspace(0.02, 0.12, 40)
    corpus_r   = [pv_annuity(annual_gap_after_tax, (1+r)/(1+inflation_rate)-1, years_in_ret) for r in ret_range]
    fig2 = go.Figure(go.Scatter(x=ret_range*100, y=corpus_r, line=dict(color=GOLD, width=2.5),
                                fill="tozeroy", fillcolor="rgba(255,215,0,0.05)"))
    fig2.add_vline(x=post_ret_return*100, line_dash="dot", line_color=LB,
                   annotation_text=f"Your Rate: {post_ret_return*100:.1f}%", annotation_font_color=LB)
    fig2.update_layout(**base_layout("Required Corpus vs Post-Retirement Return Rate", h=320))
    fig2.update_yaxes(tickformat=".2s", title="Required Corpus")
    fig2.update_xaxes(title="Post-Retirement Return Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)

# ───────────────────────────────────────
# TAB 4 – WITHDRAWAL PLAN
# ───────────────────────────────────────
with tab4:
    st.markdown("### 💸 Systematic Withdrawal Plan (SWP)")

    c1, c2, c3 = st.columns(3)
    final_balance = withdrawal_df["Ending Balance"].iloc[-1]
    c1.metric("Starting Corpus",     fmt(projected_savings))
    c2.metric("Final Balance",        fmt(final_balance), 
              delta="Funds intact ✓" if final_balance>0 else "Depleted ⚠️",
              delta_color="normal" if final_balance>0 else "inverse")
    c3.metric("Year 1 Withdrawal",   fmt(annual_gap_after_tax))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=withdrawal_df["Age"], y=withdrawal_df["Ending Balance"],
        name="Portfolio Balance", line=dict(color=GOLD, width=3),
        fill="tozeroy", fillcolor="rgba(255,215,0,0.06)"), secondary_y=False)
    fig.add_trace(go.Bar(x=withdrawal_df["Age"], y=withdrawal_df["Withdrawal"],
        name="Annual Withdrawal", marker_color="rgba(173,216,230,0.45)"), secondary_y=True)
    fig.add_trace(go.Bar(x=withdrawal_df["Age"], y=withdrawal_df["Investment Return"],
        name="Investment Return", marker_color="rgba(40,167,69,0.35)"), secondary_y=True)
    fig.update_layout(
        **base_layout("Portfolio Drawdown & Annual Cash Flows", h=420,
                      yaxis_extra=dict(title="Portfolio Balance", tickformat=".2s")),
        barmode="group",
        yaxis2=dict(title="Annual Amount", tickformat=".2s", showgrid=False))
    st.plotly_chart(fig, use_container_width=True)

    # Depletion analysis — different return scenarios
    st.markdown("#### Corpus Longevity — Return Scenario Analysis")
    scenarios = {"Bear (−3%)": post_ret_return - 0.03,
                 "Base Case":  post_ret_return,
                 "Bull (+3%)": post_ret_return + 0.03}
    sc_colors = [RED, GOLD, GRN]
    fig3 = go.Figure()
    for (sc_name, sc_ret), sc_col in zip(scenarios.items(), sc_colors):
        sc_df = build_withdrawal_schedule(projected_savings, annual_gap_after_tax,
                                          sc_ret, inflation_rate, years_in_ret, retirement_age)
        fig3.add_trace(go.Scatter(x=sc_df["Age"], y=sc_df["Ending Balance"],
            name=sc_name, line=dict(color=sc_col, width=2.5)))
    fig3.update_layout(**base_layout("Portfolio Balance Under Different Return Scenarios", h=320))
    fig3.update_yaxes(tickformat=".2s")
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📄 View Full Withdrawal Schedule"):
        disp_wd = withdrawal_df.copy()
        for col in ["Beginning Balance","Withdrawal","Investment Return","Ending Balance"]:
            disp_wd[col] = disp_wd[col].apply(lambda x: f"{x:,.0f}")
        st.dataframe(disp_wd, use_container_width=True, hide_index=True)

# ───────────────────────────────────────
# TAB 5 – SENSITIVITY
# ───────────────────────────────────────
with tab5:
    st.markdown("### 🔬 Sensitivity & Scenario Analysis")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        # Table 1: Savings Rate vs Return → Projected Corpus
        st.markdown("#### Table 1: Projected Corpus")
        st.markdown('<p style="color:#ADD8E6;font-size:0.8rem;margin:-4px 0 8px 0;">📋 Savings Rate (rows) × Pre-Retirement Return (columns)</p>', unsafe_allow_html=True)
        sav_rates = np.arange(0.05, 0.31, 0.05)
        ret_rates = np.arange(0.04, 0.15, 0.02)
        tbl1 = pd.DataFrame(index=[f"{r*100:.0f}%" for r in sav_rates],
                            columns=[f"{r*100:.0f}%" for r in ret_rates])
        for sr in sav_rates:
            for rr in ret_rates:
                fc = curr_savings*(1+rr)**years_to_ret + \
                     fv_growing_annuity(curr_income*sr, income_growth, rr, years_to_ret)
                tbl1.loc[f"{sr*100:.0f}%", f"{rr*100:.0f}%"] = f"{fc/1e6:.2f}M" if not is_inr else \
                    (f"{fc/1e7:.2f}Cr" if fc>=1e7 else f"{fc/1e5:.1f}L")
        st.dataframe(tbl1, use_container_width=True)

    with col_s2:
        # Table 2: Retire Age vs Inflation → Required Corpus
        st.markdown("#### Table 2: Required Corpus")
        st.markdown('<p style="color:#ADD8E6;font-size:0.8rem;margin:-4px 0 8px 0;">📋 Retirement Age (rows) × Inflation Rate (columns)</p>', unsafe_allow_html=True)
        ret_ages  = range(max(current_age+5, 50), min(75, life_expectancy-5), 3)
        infl_rates= np.arange(0.02, 0.10, 0.01)
        tbl2 = pd.DataFrame(index=[f"Age {a}" for a in ret_ages],
                            columns=[f"{r*100:.0f}%" for r in infl_rates])
        for ra in ret_ages:
            ytr = ra - current_age
            yir = life_expectancy - ra
            for ir in infl_rates:
                sp  = desired_spending * (1+ir)**ytr
                gap = max(0, sp - pension_income - other_income) / (1-tax_rate)
                prr = (1+post_ret_return)/(1+ir)-1
                rc  = pv_annuity(gap, prr, yir)
                tbl2.loc[f"Age {ra}", f"{ir*100:.0f}%"] = f"{rc/1e6:.2f}M" if not is_inr else \
                    (f"{rc/1e7:.2f}Cr" if rc>=1e7 else f"{rc/1e5:.1f}L")
        st.dataframe(tbl2, use_container_width=True)

    # Tornado chart
    st.markdown("#### Tornado Chart — Impact on Projected Corpus")
    base_corpus = projected_savings
    params = {
        "Pre-Ret Return ±2%":   [fv_current + fv_growing_annuity(ann_savings, income_growth, pre_ret_return-0.02, years_to_ret),
                                  fv_current + fv_growing_annuity(ann_savings, income_growth, pre_ret_return+0.02, years_to_ret)],
        "Savings Rate ±5%":      [curr_savings*(1+pre_ret_return)**years_to_ret + fv_growing_annuity(curr_income*(savings_rate-0.05), income_growth, pre_ret_return, years_to_ret),
                                  curr_savings*(1+pre_ret_return)**years_to_ret + fv_growing_annuity(curr_income*(savings_rate+0.05), income_growth, pre_ret_return, years_to_ret)],
        "Income Growth ±2%":     [curr_savings*(1+pre_ret_return)**years_to_ret + fv_growing_annuity(ann_savings, max(0,income_growth-0.02), pre_ret_return, years_to_ret),
                                  curr_savings*(1+pre_ret_return)**years_to_ret + fv_growing_annuity(ann_savings, income_growth+0.02, pre_ret_return, years_to_ret)],
        "Retire 5 Yrs Earlier":  [curr_savings*(1+pre_ret_return)**(years_to_ret-5) + fv_growing_annuity(ann_savings, income_growth, pre_ret_return, years_to_ret-5), base_corpus],
        "Current Savings ±50%":  [curr_savings*0.5*(1+pre_ret_return)**years_to_ret + fv_contributions,
                                  curr_savings*1.5*(1+pre_ret_return)**years_to_ret + fv_contributions],
    }
    low_vals  = [(v[0]-base_corpus)/base_corpus*100 for v in params.values()]
    high_vals = [(v[1]-base_corpus)/base_corpus*100 for v in params.values()]
    param_names = list(params.keys())
    sorted_idx  = np.argsort([abs(h-l) for h,l in zip(high_vals, low_vals)])[::-1]

    fig_t = go.Figure()
    for i in sorted_idx:
        fig_t.add_trace(go.Bar(y=[param_names[i]], x=[low_vals[i]],
            orientation="h", marker_color=RED, showlegend=False,
            text=f"{low_vals[i]:+.1f}%", textposition="outside",
            textfont=dict(size=9, color=RED)))
        fig_t.add_trace(go.Bar(y=[param_names[i]], x=[high_vals[i]],
            orientation="h", marker_color=GRN, showlegend=False,
            text=f"{high_vals[i]:+.1f}%", textposition="outside",
            textfont=dict(size=9, color=GRN)))
    fig_t.add_vline(x=0, line_color=GOLD, line_width=1.5)
    fig_t.update_layout(
        **base_layout("Tornado — Sensitivity of Projected Corpus", h=340,
                      xaxis_extra=dict(title="% Change vs Base Case")),
        barmode="overlay")
    st.plotly_chart(fig_t, use_container_width=True)

# ───────────────────────────────────────
# TAB 6 – MONTE CARLO
# ───────────────────────────────────────
with tab6:
    st.markdown("### 🎲 Monte Carlo Simulation")
    st.info(f"Running **{mc_sims:,} simulations** with return volatility σ = {return_std*100:.1f}% and inflation σ = {inflation_std*100:.1f}%")

    c1, c2, c3 = st.columns(3)
    c1.metric("Success Rate", f"{success_rate:.1f}%",
              delta="Funds last lifetime" if success_rate>=75 else "Risk of depletion",
              delta_color="normal" if success_rate>=75 else "inverse")
    c2.metric("Median Corpus @ Retirement", fmt(np.median(corpus_dist)))
    c3.metric("5th Percentile (Worst 5%)",  fmt(np.percentile(corpus_dist, 5)))

    fig_mc = go.Figure()
    fig_mc.add_trace(go.Histogram(x=corpus_dist, nbinsx=60,
        name="Simulated Corpus", marker_color="rgba(255,215,0,0.55)",
        marker_line_color=GOLD, marker_line_width=0.5))
    fig_mc.add_vline(x=required_corpus, line_dash="dash", line_color=RED, line_width=2,
                     annotation_text="Required Corpus", annotation_font_color=RED)
    fig_mc.add_vline(x=np.median(corpus_dist), line_dash="dot", line_color=GRN,
                     annotation_text="Median", annotation_font_color=GRN)
    for pct, col, label in [(5,RED,"P5"),(25,LB,"P25"),(75,LB,"P75"),(95,GRN,"P95")]:
        fig_mc.add_vline(x=np.percentile(corpus_dist, pct), line_dash="dot",
                         line_color=col, line_width=0.8,
                         annotation_text=label, annotation_font_color=col,
                         annotation_font_size=9)
    fig_mc.update_layout(**base_layout("Distribution of Projected Corpus at Retirement", h=380))
    fig_mc.update_xaxes(tickformat=".2s", title="Projected Corpus")
    fig_mc.update_yaxes(title="Number of Simulations")
    st.plotly_chart(fig_mc, use_container_width=True)

    # Percentile table
    pcts = [5, 10, 25, 50, 75, 90, 95]
    pct_vals = [np.percentile(corpus_dist, p) for p in pcts]
    pct_df = pd.DataFrame({
        "Percentile": [f"P{p}" for p in pcts],
        "Corpus": [fmt(v) for v in pct_vals],
        "vs Required": [f"{'✅ ' if v>=required_corpus else '❌ '}{(v/required_corpus-1)*100:+.1f}%" for v in pct_vals],
        "Funded?": ["✅ Yes" if v>=required_corpus else "❌ No" for v in pct_vals]
    })
    st.dataframe(pct_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="background:rgba(0,51,102,0.4);border-left:3px solid #FFD700;
        border-radius:8px;padding:12px 16px;margin-top:12px;font-size:0.78rem;color:#8892b0;">
    <b style="color:#FFD700;">📌 Interpretation:</b> Monte Carlo simulates thousands of possible futures by randomly varying 
    investment returns and inflation each year. A success rate above 75% is generally considered robust. 
    The P5 (5th percentile) represents the worst 5% of outcomes — your "safety floor."
    </div>""", unsafe_allow_html=True)

# ───────────────────────────────────────
# TAB 7 – TVM BASICS
# ───────────────────────────────────────
with tab7:
    st.markdown("### 📚 Time Value of Money — Interactive Learning Module")
    st.markdown('<p style="color:#ADD8E6;font-size:0.83rem;margin:-4px 0 12px 0;padding:6px 14px;background:rgba(0,51,102,0.4);border-left:3px solid #ADD8E6;border-radius:0 6px 6px 0;">🎛️ Adjust inputs to see how TVM formulas power retirement planning</p>', unsafe_allow_html=True)

    tvm1, tvm2, tvm3, tvm4, tvm5 = st.tabs(["FV — Future Value","PV — Present Value","PMT — Payment","NPER — Periods","RATE"])

    with tvm1:
        c1,c2 = st.columns(2)
        with c1:
            pv_in = st.number_input(f"Present Value (PV) ({curr_sym})",
                                    1000 if is_inr else 100,
                                    10_000_000 if is_inr else 500_000,
                                    100_000 if is_inr else 10_000,
                                    10_000 if is_inr else 1_000, key="fv_pv")
            r_in  = st.slider("Annual Rate (%)", 1.0, 20.0, 8.0, 0.5, key="fv_r")
            n_in  = st.slider("Years", 1, 50, 30, 1, key="fv_n")
            cpd   = st.selectbox("Compounding", [1,12,365], index=1, format_func=lambda x: {1:"Annual",12:"Monthly",365:"Daily"}[x], key="fv_cpd")
        fv_val = pv_in * (1 + r_in/100/cpd) ** (n_in*cpd)
        with c2:
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:24px;text-align:center;">
            <div style="color:#8892b0;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;">Future Value</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">{fmt(fv_val)}</div>
            <div style="color:#ADD8E6;font-size:0.75rem;">Growth: {fv_val/pv_in:.2f}×  |  Gain: {fmt(fv_val-pv_in)}</div>
            <div style="color:#8892b0;font-size:0.7rem;margin-top:8px;">FV = PV × (1 + r/m)^(n×m)</div>
            </div>""", unsafe_allow_html=True)
        years_range = range(1, n_in+1)
        fv_traj = [pv_in*(1+r_in/100/cpd)**(y*cpd) for y in years_range]
        fig = go.Figure(go.Scatter(x=list(years_range), y=fv_traj, fill="tozeroy",
            line=dict(color=GOLD, width=2.5), fillcolor="rgba(255,215,0,0.07)"))
        fig.update_layout(**base_layout("Compound Growth Trajectory", h=250))
        fig.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)

    with tvm2:
        c1,c2 = st.columns(2)
        with c1:
            fv_in2 = st.number_input(f"Future Amount Needed ({curr_sym})",
                                     100_000 if is_inr else 10_000,
                                     100_000_000 if is_inr else 5_000_000,
                                     10_000_000 if is_inr else 500_000,
                                     500_000 if is_inr else 10_000, key="pv_fv")
            r_in2  = st.slider("Discount Rate (%)", 1.0, 20.0, 7.0, 0.5, key="pv_r")
            n_in2  = st.slider("Years Until Needed", 1, 50, 25, 1, key="pv_n")
        pv_val = fv_in2 / (1+r_in2/100)**n_in2
        discount_pct = (1 - pv_val/fv_in2)*100
        with c2:
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:24px;text-align:center;">
            <div style="color:#8892b0;font-size:0.78rem;text-transform:uppercase;">Present Value</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">{fmt(pv_val)}</div>
            <div style="color:#ADD8E6;font-size:0.75rem;">Discounted by {discount_pct:.1f}% over {n_in2} years</div>
            <div style="color:#8892b0;font-size:0.7rem;margin-top:8px;">PV = FV / (1 + r)^n</div>
            </div>""", unsafe_allow_html=True)

    with tvm3:
        c1,c2 = st.columns(2)
        with c1:
            target_fv = st.number_input(f"Target Future Value ({curr_sym})",
                                        100_000 if is_inr else 10_000,
                                        100_000_000 if is_inr else 5_000_000,
                                        10_000_000 if is_inr else 500_000,
                                        500_000 if is_inr else 10_000, key="pmt_fv")
            r_pmt     = st.slider("Annual Rate (%)", 1.0, 20.0, 10.0, 0.5, key="pmt_r")
            n_pmt     = st.slider("Years to Save", 1, 50, 30, 1, key="pmt_n")
            freq_pmt  = st.selectbox("Payment Frequency", [12,1,4,26], index=0,
                                     format_func=lambda x:{12:"Monthly",1:"Annual",4:"Quarterly",26:"Bi-weekly"}[x], key="pmt_f")
        r_per = r_pmt/100/freq_pmt
        n_per = n_pmt * freq_pmt
        pmt_val = target_fv * r_per / ((1+r_per)**n_per - 1)
        total_paid = pmt_val * n_per
        with c2:
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:24px;text-align:center;">
            <div style="color:#8892b0;font-size:0.78rem;text-transform:uppercase;">Required Payment</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">{fmt(pmt_val)}</div>
            <div style="color:#ADD8E6;font-size:0.75rem;">Per period | Total paid: {fmt(total_paid)}</div>
            <div style="color:#28a745;font-size:0.75rem;">Interest earned: {fmt(target_fv-total_paid)}</div>
            <div style="color:#8892b0;font-size:0.7rem;margin-top:8px;">PMT = FV × r / ((1+r)^n - 1)</div>
            </div>""", unsafe_allow_html=True)

    with tvm4:
        c1,c2 = st.columns(2)
        with c1:
            mo_sav  = st.number_input(f"Monthly Savings ({curr_sym})",
                                      1_000 if is_inr else 100,
                                      1_000_000 if is_inr else 50_000,
                                      25_000 if is_inr else 1_000,
                                      1_000 if is_inr else 100, key="np_ms")
            curr_sv = st.number_input(f"Current Savings ({curr_sym})",
                                      0,
                                      50_000_000 if is_inr else 2_000_000,
                                      500_000 if is_inr else 50_000,
                                      10_000 if is_inr else 1_000, key="np_cs")
            goal_am = st.number_input(f"Target Amount ({curr_sym})",
                                      100_000 if is_inr else 10_000,
                                      500_000_000 if is_inr else 10_000_000,
                                      10_000_000 if is_inr else 1_000_000,
                                      100_000 if is_inr else 10_000, key="np_ga")
            r_np    = st.slider("Annual Return (%)", 1.0, 20.0, 10.0, 0.5, key="np_r")
        try:
            r_mo = r_np/100/12
            nper_val = math.log((goal_am*r_mo + mo_sav) / (curr_sv*r_mo + mo_sav)) / math.log(1+r_mo)
            years_to_goal = nper_val / 12
        except:
            years_to_goal = float("nan")
        with c2:
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:24px;text-align:center;">
            <div style="color:#8892b0;font-size:0.78rem;text-transform:uppercase;">Years to Goal</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">
                {years_to_goal:.1f} yrs</div>
            <div style="color:#ADD8E6;font-size:0.75rem;">Reach goal at age {current_age+int(years_to_goal)}</div>
            </div>""", unsafe_allow_html=True)

    with tvm5:
        c1,c2 = st.columns(2)
        with c1:
            curr_sv5 = st.number_input(f"Current Savings ({curr_sym})",
                                       0,
                                       50_000_000 if is_inr else 2_000_000,
                                       500_000 if is_inr else 50_000,
                                       10_000 if is_inr else 1_000, key="rt_cs")
            mo_con5  = st.number_input(f"Monthly Contribution ({curr_sym})",
                                       1_000 if is_inr else 100,
                                       1_000_000 if is_inr else 50_000,
                                       25_000 if is_inr else 1_000,
                                       1_000 if is_inr else 100, key="rt_mc")
            target5  = st.number_input(f"Target Corpus ({curr_sym})",
                                       100_000 if is_inr else 10_000,
                                       500_000_000 if is_inr else 10_000_000,
                                       20_000_000 if is_inr else 1_500_000,
                                       100_000 if is_inr else 10_000, key="rt_tg")
            years5   = st.slider("Years to Retirement", 5, 50, years_to_ret, 1, key="rt_yr")
        # Solve for rate numerically
        def corpus_at_rate(r_annual):
            r_mo = r_annual/12
            return curr_sv5*(1+r_mo)**(years5*12) + mo_con5*((1+r_mo)**(years5*12)-1)/r_mo if r_mo>0 else curr_sv5+mo_con5*years5*12
        from scipy.optimize import brentq
        try:
            req_rate = brentq(lambda r: corpus_at_rate(r)-target5, 0.001, 0.5)
        except:
            req_rate = float("nan")
        with c2:
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:24px;text-align:center;">
            <div style="color:#8892b0;font-size:0.78rem;text-transform:uppercase;">Required Annual Return</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">
                {req_rate*100:.2f}%</div>
            <div style="color:#ADD8E6;font-size:0.75rem;">To reach {fmt(target5)} in {years5} years</div>
            </div>""", unsafe_allow_html=True)

# ───────────────────────────────────────
# TAB 8 – CASE STUDIES
# ───────────────────────────────────────
with tab8:
    st.markdown("### 🎓 Real-World Case Studies in Retirement Planning")
    st.markdown('<p style="color:#ADD8E6;font-size:0.83rem;margin:-4px 0 14px 0;padding:8px 14px;background:rgba(0,51,102,0.35);border-left:3px solid #FFD700;border-radius:0 8px 8px 0;line-height:1.6;">📚 Interactive case studies drawn from Indian and global financial planning practice. Work through each scenario, change the assumptions, and see the outcomes.</p>', unsafe_allow_html=True)

    cs_tabs = st.tabs([
        "📘 Case 1 · The Late Starter",
        "📗 Case 2 · The Early Bird",
        "📙 Case 3 · The Dual-Income Couple",
        "📕 Case 4 · Inflation Shock",
        "📓 Case 5 · The Entrepreneur",
    ])

    # ── Shared case-study helpers ──────────────────────────────────────────────
    def case_card(title, subtitle, color="#003366"):
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{color},rgba(0,51,102,0.75));
            border:1px solid rgba(255,215,0,0.4);border-radius:14px;padding:22px 26px;margin-bottom:18px;
            box-shadow:0 4px 20px rgba(0,0,0,0.4);">
        <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#FFD700;
            margin-bottom:6px;font-weight:700;">{title}</div>
        <div style="font-size:0.83rem;color:#c8dff0;line-height:1.7;font-weight:400;">{subtitle}</div>
        </div>""", unsafe_allow_html=True)

    def insight_box(text, icon="💡"):
        st.markdown(f"""
        <div style="background:rgba(255,215,0,0.12);border-left:4px solid #FFD700;
            border-radius:0 10px 10px 0;padding:14px 18px;margin:12px 0;
            font-size:0.83rem;color:#e6f1ff;line-height:1.8;
            box-shadow:0 2px 12px rgba(0,0,0,0.2);">
        <span style="font-size:1rem;">{icon}</span> {text}
        </div>""", unsafe_allow_html=True)

    def lesson_box(text):
        st.markdown(f"""
        <div style="background:rgba(40,167,69,0.18);border:1px solid rgba(40,167,69,0.4);
            border-left:5px solid #28a745;border-radius:0 10px 10px 0;
            padding:14px 18px;margin:12px 0;font-size:0.83rem;color:#e6f1ff;line-height:1.8;
            box-shadow:0 2px 12px rgba(0,0,0,0.2);">
        🎯 <b style="color:#5dd879;font-size:0.85rem;letter-spacing:0.04em;">LEARNING OUTCOME:</b><br>
        <span style="color:#d4f4dd;">{text}</span>
        </div>""", unsafe_allow_html=True)

    def warning_box(text):
        st.markdown(f"""
        <div style="background:rgba(220,53,69,0.18);border:1px solid rgba(220,53,69,0.4);
            border-left:5px solid #dc3545;border-radius:0 10px 10px 0;
            padding:14px 18px;margin:12px 0;font-size:0.83rem;color:#e6f1ff;line-height:1.8;
            box-shadow:0 2px 12px rgba(0,0,0,0.2);">
        ⚠️ <b style="color:#f18a94;font-size:0.85rem;letter-spacing:0.04em;">CAUTION:</b><br>
        <span style="color:#ffd4d8;">{text}</span>
        </div>""", unsafe_allow_html=True)

    # ── CASE 1 · THE LATE STARTER ─────────────────────────────────────────────
    with cs_tabs[0]:
        case_card(
            "Rajan Mehta — The Late Starter",
            "Age 45 · Senior Manager at an IT firm · ₹18L annual income · Only ₹5L saved so far · Wants to retire at 62"
        )
        st.markdown("""
        **Situation:** Rajan spent his 30s paying off a home loan and children's education. At 45, 
        he has just ₹5 lakhs in his PPF and now wants to build a retirement corpus of ₹2 Crore by 62.
        He can save aggressively — up to 30% of income. What does the math say?
        """)

        col1, col2 = st.columns(2)
        with col1:
            cs1_income    = st.number_input("Annual Income (₹)", 500000, 10000000, 1800000, 100000, key="cs1_inc")
            cs1_savings_r = st.slider("Savings Rate (%)", 5, 50, 30, 5, key="cs1_sr") / 100
            cs1_curr_sav  = st.number_input("Current Savings (₹)", 0, 5000000, 500000, 50000, key="cs1_cs")
            cs1_ret       = st.slider("Expected Return (%)", 6.0, 16.0, 11.0, 0.5, key="cs1_r") / 100
            cs1_infl      = st.slider("Inflation (%)", 3.0, 9.0, 6.0, 0.5, key="cs1_inf") / 100
            cs1_inc_g     = st.slider("Income Growth (%)", 2.0, 10.0, 5.0, 0.5, key="cs1_ig") / 100
            cs1_years     = 62 - 45  # 17 years
            cs1_ann_sav   = cs1_income * cs1_savings_r

        cs1_fv_curr  = cs1_curr_sav * (1 + cs1_ret) ** cs1_years
        cs1_fv_cont  = fv_growing_annuity(cs1_ann_sav, cs1_inc_g, cs1_ret, cs1_years)
        cs1_projected = cs1_fv_curr + cs1_fv_cont
        cs1_target    = 20000000  # ₹2 Cr

        with col2:
            funded = cs1_projected >= cs1_target
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:20px;text-align:center;margin-top:8px;">
            <div style="color:#8892b0;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">Projected Corpus @ 62</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">
                ₹{cs1_projected/1e7:.2f} Cr</div>
            <div style="color:{'#28a745' if funded else '#dc3545'};font-size:0.85rem;font-weight:600;">
                {'✅ Target of ₹2 Cr Achieved!' if funded else f'❌ Shortfall: ₹{(cs1_target-cs1_projected)/1e5:.1f}L'}</div>
            <hr style="border-color:rgba(255,215,0,0.15);margin:10px 0;">
            <div style="font-size:0.75rem;color:#8892b0;">Annual Savings: ₹{cs1_ann_sav/1e5:.1f}L</div>
            <div style="font-size:0.75rem;color:#8892b0;">Monthly: ₹{cs1_ann_sav/12/1000:.1f}K</div>
            <div style="font-size:0.75rem;color:#8892b0;">Compounding: {cs1_years} years</div>
            </div>""", unsafe_allow_html=True)

        # Year-by-year chart
        cs1_rows = []
        bal, inc = cs1_curr_sav, cs1_income
        for yr in range(1, cs1_years + 1):
            contrib = inc * cs1_savings_r
            inv_r   = bal * cs1_ret
            bal     = bal + contrib + inv_r
            inc    *= (1 + cs1_inc_g)
            cs1_rows.append({"Age": 45 + yr, "Balance": bal, "Contribution": contrib, "Return": inv_r})
        cs1_df = pd.DataFrame(cs1_rows)

        fig_cs1 = go.Figure()
        fig_cs1.add_trace(go.Scatter(x=cs1_df["Age"], y=cs1_df["Balance"], name="Projected Balance",
            line=dict(color=GOLD, width=3), fill="tozeroy", fillcolor="rgba(255,215,0,0.07)"))
        fig_cs1.add_hline(y=cs1_target, line_dash="dash", line_color=RED,
            annotation_text="₹2 Cr Target", annotation_font_color=RED)
        fig_cs1.update_layout(**base_layout("Rajan's Wealth Accumulation (Age 45 → 62)", h=320))
        fig_cs1.update_yaxes(tickformat=".2s", title="Portfolio Value (₹)")
        st.plotly_chart(fig_cs1, use_container_width=True)

        insight_box("""
        Rajan's situation demonstrates the <b>cost of delay</b>. Had he started at 30 with the same savings rate,
        he would need only ₹8,500/month to reach ₹2 Cr. Starting at 45, he needs ₹45,000/month — <b>5× more</b>.
        This is the compounding penalty — often called the "cost of waiting."
        """)

        st.markdown("#### 📊 Sensitivity — Required Savings Rate to Hit ₹2 Cr")
        ret_vals = [0.08, 0.10, 0.12, 0.14]
        sr_vals  = np.arange(0.10, 0.51, 0.05)
        fig_s1 = go.Figure()
        colors_s = [RED, GOLD, GRN, LB]
        for ret_v, col_v in zip(ret_vals, colors_s):
            projected_v = [cs1_curr_sav*(1+ret_v)**cs1_years +
                           fv_growing_annuity(cs1_income*sr, cs1_inc_g, ret_v, cs1_years)
                           for sr in sr_vals]
            fig_s1.add_trace(go.Scatter(x=sr_vals*100, y=projected_v,
                name=f"Return={ret_v*100:.0f}%", line=dict(color=col_v, width=2)))
        fig_s1.add_hline(y=cs1_target, line_dash="dot", line_color="white",
                         annotation_text="₹2 Cr Target", annotation_font_color="white")
        fig_s1.update_layout(**base_layout("Savings Rate vs Projected Corpus (₹)", h=300))
        fig_s1.update_yaxes(tickformat=".2s")
        fig_s1.update_xaxes(title="Savings Rate (%)")
        st.plotly_chart(fig_s1, use_container_width=True)

        lesson_box("""
        Every year of delay roughly requires <b>doubling your savings rate</b> to compensate. 
        The solution for late starters: maximize ELSS, NPS, PPF simultaneously, and consider working 
        2–3 extra years — each extra year adds both accumulation time AND removes one retirement year.
        """)

    # ── CASE 2 · THE EARLY BIRD ───────────────────────────────────────────────
    with cs_tabs[1]:
        case_card(
            "Priya Sharma — The Early Bird",
            "Age 24 · Software Engineer · ₹9L CTC · ₹50K savings so far · Goal: Retire at 50 with ₹5 Crore",
            color="rgba(0,77,0,0.6)"
        )
        st.markdown("""
        **Situation:** Priya just started her career and wants to retire by 50 — a **FIRE** (Financial Independence, 
        Retire Early) goal. She has 26 years. Can disciplined saving starting early create extraordinary wealth?
        """)

        col1, col2 = st.columns(2)
        with col1:
            cs2_inc    = st.number_input("Starting Annual Income (₹)", 300000, 5000000, 900000, 50000, key="cs2_inc")
            cs2_sr     = st.slider("Savings Rate (%)", 10, 60, 35, 5, key="cs2_sr") / 100
            cs2_ig     = st.slider("Income Growth (%) — career progression", 5.0, 20.0, 12.0, 1.0, key="cs2_ig") / 100
            cs2_ret    = st.slider("Investment Return (%)", 8.0, 18.0, 13.0, 0.5, key="cs2_ret") / 100
            cs2_infl   = st.slider("Inflation (%)", 3.0, 9.0, 6.0, 0.5, key="cs2_inf") / 100
            cs2_yrs    = 50 - 24  # 26 years
            cs2_target = st.number_input("FIRE Target Corpus (₹)", 1000000, 100000000, 50000000, 1000000, key="cs2_tgt")

        cs2_fv_curr = 50000 * (1 + cs2_ret) ** cs2_yrs
        cs2_fv_cont = fv_growing_annuity(cs2_inc * cs2_sr, cs2_ig, cs2_ret, cs2_yrs)
        cs2_proj    = cs2_fv_curr + cs2_fv_cont

        with col2:
            funded2 = cs2_proj >= cs2_target
            # 4% rule: how much can she withdraw at 50?
            annual_wd_4pct = cs2_proj * 0.04
            monthly_wd_4pct= annual_wd_4pct / 12
            st.markdown(f"""
            <div style="background:rgba(0,77,0,0.4);border:1px solid rgba(255,215,0,0.3);
                border-radius:12px;padding:20px;text-align:center;margin-top:8px;">
            <div style="color:#8892b0;font-size:0.75rem;text-transform:uppercase;">Corpus at Age 50</div>
            <div style="font-family:'Playfair Display';font-size:2.2rem;color:#FFD700;margin:8px 0;">
                ₹{cs2_proj/1e7:.2f} Cr</div>
            <div style="color:{'#28a745' if funded2 else '#dc3545'};font-size:0.85rem;font-weight:600;">
                {'✅ FIRE Goal Achieved!' if funded2 else f'❌ Short by ₹{(cs2_target-cs2_proj)/1e7:.2f} Cr'}</div>
            <hr style="border-color:rgba(255,215,0,0.15);margin:10px 0;">
            <div style="font-size:0.78rem;color:#ADD8E6;"><b>4% Rule Annual Withdrawal:</b> ₹{annual_wd_4pct/1e5:.1f}L</div>
            <div style="font-size:0.78rem;color:#ADD8E6;"><b>Monthly Income @ FIRE:</b> ₹{monthly_wd_4pct/1000:.1f}K</div>
            <div style="font-size:0.78rem;color:#8892b0;">Compounding: {cs2_yrs} years of growth</div>
            </div>""", unsafe_allow_html=True)

        # Early vs Late comparison chart
        ages_early = list(range(24, 51))
        bal_e, inc_e = 50000, cs2_inc
        bal_early = []
        for yr in range(26):
            bal_e = bal_e * (1 + cs2_ret) + inc_e * cs2_sr
            inc_e *= (1 + cs2_ig)
            bal_early.append(bal_e)

        ages_late = list(range(35, 51))
        bal_l, inc_l = 50000, cs2_inc * (1 + cs2_ig) ** 11
        bal_late = []
        for yr in range(15):
            bal_l = bal_l * (1 + cs2_ret) + inc_l * cs2_sr
            inc_l *= (1 + cs2_ig)
            bal_late.append(bal_l)

        fig_cs2 = go.Figure()
        fig_cs2.add_trace(go.Scatter(x=ages_early, y=bal_early, name="Starts at 24",
            line=dict(color=GRN, width=3), fill="tozeroy", fillcolor="rgba(40,167,69,0.08)"))
        fig_cs2.add_trace(go.Scatter(x=ages_late, y=bal_late, name="Starts at 35",
            line=dict(color=RED, width=2, dash="dash")))
        fig_cs2.add_hline(y=cs2_target, line_dash="dot", line_color=GOLD,
            annotation_text="FIRE Target", annotation_font_color=GOLD)
        fig_cs2.update_layout(**base_layout("Early vs Late Starter — Wealth at Each Age", h=330))
        fig_cs2.update_yaxes(tickformat=".2s", title="Portfolio Value (₹)")
        st.plotly_chart(fig_cs2, use_container_width=True)

        # Power of compounding breakdown
        total_invested = sum(cs2_inc * cs2_sr * (1 + cs2_ig)**yr for yr in range(cs2_yrs))
        invest_gain    = cs2_proj - total_invested if cs2_proj > total_invested else 0
        fig_donut = go.Figure(go.Pie(
            labels=["Total Contributed", "Investment Gains (Compounding Power)"],
            values=[max(0, total_invested), invest_gain],
            marker=dict(colors=[LB, GOLD]),
            hole=0.6, textfont=dict(size=11, color="white")
        ))
        fig_donut.add_annotation(text=f"₹{cs2_proj/1e7:.1f}Cr<br>Total",
            x=0.5, y=0.5, font=dict(size=12, color=GOLD, family="Playfair Display"), showarrow=False)
        fig_donut.update_layout(**base_layout("Where Does the Wealth Come From?", h=300))
        fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_donut, use_container_width=True)

        insight_box("""
        Priya's 26-year head start means <b>investment gains can exceed her lifetime contributions by 3–5×</b>. 
        This is Einstein's "eighth wonder" — compound interest. Each rupee saved at 24 becomes ₹25+ by 50 at 13% return.
        At 35, the same rupee becomes only ₹5.
        """)
        lesson_box("""
        FIRE requires two things: a <b>high savings rate (30–50%)</b> AND disciplined equity allocation for inflation-beating returns. 
        Index funds (Nifty 50, global ETFs) in a long accumulation phase minimize costs and maximize compounding.
        """)

    # ── CASE 3 · DUAL-INCOME COUPLE ──────────────────────────────────────────
    with cs_tabs[2]:
        case_card(
            "Vikram & Deepa Nair — Dual-Income Couple",
            "Ages 38 & 36 · Combined income ₹42L · Separate EPF/NPS · Retire together at 60 · Target ₹6 Crore combined",
            color="rgba(0,51,100,0.7)"
        )
        st.markdown("""
        **Situation:** Vikram (₹25L) and Deepa (₹17L) both contribute to retirement separately. 
        Vikram has EPF of ₹8L; Deepa has NPS of ₹4L. How does coordinating their retirement 
        strategy optimize their combined corpus?
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👨 Vikram's Profile**")
            v_inc   = st.number_input("Vikram's Income (₹)", 500000, 20000000, 2500000, 100000, key="v_inc")
            v_sr    = st.slider("Vikram's Savings Rate (%)", 5, 50, 25, 5, key="v_sr") / 100
            v_ret   = st.slider("Vikram's Return (%)", 6.0, 16.0, 10.0, 0.5, key="v_ret") / 100
            v_curr  = st.number_input("Vikram's Current Savings (₹)", 0, 20000000, 800000, 100000, key="v_curr")
            v_yrs   = 60 - 38

        with col2:
            st.markdown("**👩 Deepa's Profile**")
            d_inc   = st.number_input("Deepa's Income (₹)", 500000, 20000000, 1700000, 100000, key="d_inc")
            d_sr    = st.slider("Deepa's Savings Rate (%)", 5, 50, 30, 5, key="d_sr") / 100
            d_ret   = st.slider("Deepa's Return (%)", 6.0, 16.0, 12.0, 0.5, key="d_ret") / 100
            d_curr  = st.number_input("Deepa's Current Savings (₹)", 0, 20000000, 400000, 100000, key="d_curr")
            d_yrs   = 60 - 36

        v_proj = v_curr * (1+v_ret)**v_yrs + fv_growing_annuity(v_inc*v_sr, 0.06, v_ret, v_yrs)
        d_proj = d_curr * (1+d_ret)**d_yrs + fv_growing_annuity(d_inc*d_sr, 0.06, d_ret, d_yrs)
        combined = v_proj + d_proj
        target3  = 60000000

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Vikram's Corpus", f"₹{v_proj/1e7:.2f}Cr")
        m2.metric("Deepa's Corpus", f"₹{d_proj/1e7:.2f}Cr")
        m3.metric("Combined Corpus", f"₹{combined/1e7:.2f}Cr",
                  delta=f"{'✅ Above' if combined>=target3 else '❌ Below'} ₹6Cr target")
        m4.metric("Funding Ratio", f"{combined/target3*100:.1f}%")

        # Timeline comparison
        ages_v = list(range(38, 61))
        ages_d = list(range(36, 61))
        bal_v, bal_d = v_curr, d_curr
        inc_v, inc_d = v_inc, d_inc
        bals_v, bals_d = [], []
        for yr in range(22):
            bal_v = bal_v*(1+v_ret) + inc_v*v_sr; inc_v*=1.06
            bal_d = bal_d*(1+d_ret) + inc_d*d_sr; inc_d*=1.06
            bals_v.append(bal_v)
            bals_d.append(bal_d)

        fig_cs3 = go.Figure()
        fig_cs3.add_trace(go.Scatter(x=ages_v[:len(bals_v)], y=bals_v, name="Vikram", line=dict(color=LB, width=2.5)))
        fig_cs3.add_trace(go.Scatter(x=ages_d[:len(bals_d)], y=bals_d, name="Deepa", line=dict(color=GOLD, width=2.5)))
        combined_by_yr = [a+b for a,b in zip(bals_v, bals_d)]
        fig_cs3.add_trace(go.Scatter(x=ages_v[:len(combined_by_yr)], y=combined_by_yr,
            name="Combined", line=dict(color=GRN, width=3, dash="dot"),
            fill="tozeroy", fillcolor="rgba(40,167,69,0.05)"))
        fig_cs3.add_hline(y=target3, line_dash="dash", line_color=RED, annotation_text="₹6 Cr Target")
        fig_cs3.update_layout(**base_layout("Vikram & Deepa — Wealth Trajectories", h=340))
        fig_cs3.update_yaxes(tickformat=".2s", title="Portfolio Value (₹)")
        st.plotly_chart(fig_cs3, use_container_width=True)

        st.markdown("#### 🔄 Asset Allocation Optimization for Couples")
        st.markdown("""
        | Strategy | Vikram (Older, 38) | Deepa (Younger, 36) | Rationale |
        |---|---|---|---|
        | **Equity Allocation** | 60% | 75% | Deepa has 2 more years — higher risk capacity |
        | **Debt Allocation** | 30% | 20% | EPF counts as debt; balance in bonds |
        | **Alternative** | 10% | 5% | REITs, Gold for diversification |
        | **Key Vehicle** | EPF + PPF | NPS Tier-I + ELSS | Tax-optimized per profile |
        """)

        insight_box("""
        Dual-income couples benefit from <b>asset location arbitrage</b>: one partner can hold equity-heavy 
        instruments while the other holds debt — combined the portfolio is balanced, but each benefits from 
        optimal tax treatment. EPF (debt) + ELSS (equity) + NPS is a powerful tax-efficient trio.
        """)
        lesson_box("""
        A couple's retirement plan should be treated as <b>one portfolio, two contributors</b>. 
        Coordinate asset allocation, not just savings rates. The younger spouse should carry more equity risk. 
        Never optimize each person's portfolio in isolation.
        """)

    # ── CASE 4 · INFLATION SHOCK ──────────────────────────────────────────────
    with cs_tabs[3]:
        case_card(
            "The Inflation Shock Scenario",
            "Retiree Radhakrishnan, 65 · ₹50L corpus · Planned 5% return · Actual inflation: surges to 9% for 5 years",
            color="rgba(100,20,0,0.6)"
        )
        st.markdown("""
        **Situation:** Radhakrishnan retired at 65 with ₹50 lakhs, planning to withdraw ₹3L/year (inflation-adjusted at 6%).
        Post-retirement, India experiences an inflation surge to 9% for 5 years. How does this derail the plan?
        This case shows why <b>sequence-of-returns and inflation risk</b> are the biggest threats in retirement.
        """)

        col1, col2 = st.columns([1, 2])
        with col1:
            cs4_corpus  = st.number_input("Starting Corpus (₹)", 1000000, 20000000, 5000000, 500000, key="cs4_c")
            cs4_wd1     = st.number_input("Year-1 Withdrawal (₹)", 50000, 2000000, 300000, 25000, key="cs4_w")
            cs4_ret     = st.slider("Post-Ret Investment Return (%)", 4.0, 12.0, 7.0, 0.5, key="cs4_r") / 100
            cs4_normal_infl = st.slider("Normal Inflation (%)", 3.0, 8.0, 6.0, 0.5, key="cs4_ni") / 100
            cs4_shock_infl  = st.slider("Shock Inflation (%) — Years 1–5", 5.0, 15.0, 9.0, 0.5, key="cs4_si") / 100
            cs4_yrs         = st.slider("Retirement Duration (years)", 10, 35, 25, 1, key="cs4_y")

        # Two scenarios: base vs shock
        def simulate_retirement(corpus, wd1, ret, infl_schedule):
            rows, bal, wd = [], corpus, wd1
            for yr, infl in enumerate(infl_schedule, 1):
                inv_r  = (bal - wd/2) * ret
                end_b  = max(0, bal + inv_r - wd)
                rows.append({"Year": yr, "Age": 64+yr, "Balance": end_b,
                             "Withdrawal": wd, "Inflation": infl*100})
                bal = end_b
                wd  = wd * (1 + infl)
                if bal <= 0:
                    for remaining in range(yr+1, len(infl_schedule)+1):
                        rows.append({"Year": remaining, "Age": 64+remaining, "Balance": 0,
                                     "Withdrawal": wd, "Inflation": infl_schedule[remaining-1]*100})
                    break
            return pd.DataFrame(rows)

        base_schedule  = [cs4_normal_infl] * cs4_yrs
        shock_schedule = [cs4_shock_infl]*5 + [cs4_normal_infl]*(cs4_yrs-5)

        df_base  = simulate_retirement(cs4_corpus, cs4_wd1, cs4_ret, base_schedule)
        df_shock = simulate_retirement(cs4_corpus, cs4_wd1, cs4_ret, shock_schedule)

        with col2:
            depletes_base  = (df_base["Balance"] == 0).any()
            depletes_shock = (df_shock["Balance"] == 0).any()

            m1, m2 = st.columns(2)
            m1.metric("Final Balance (Base)", f"₹{df_base['Balance'].iloc[-1]/1e5:.1f}L",
                      delta="✅ Funds Intact" if not depletes_base else "❌ Depleted")
            m2.metric("Final Balance (Inflation Shock)", f"₹{df_shock['Balance'].iloc[-1]/1e5:.1f}L",
                      delta="⚠️ Shock Impact" if depletes_shock else "✅ Survives",
                      delta_color="inverse" if depletes_shock else "normal")

        fig_cs4 = go.Figure()
        fig_cs4.add_trace(go.Scatter(x=df_base["Age"], y=df_base["Balance"],
            name=f"Normal Inflation ({cs4_normal_infl*100:.0f}%)", line=dict(color=GRN, width=2.5)))
        fig_cs4.add_trace(go.Scatter(x=df_shock["Age"], y=df_shock["Balance"],
            name=f"Shock Inflation ({cs4_shock_infl*100:.0f}% for 5yr)", line=dict(color=RED, width=2.5, dash="dash"),
            fill="tonexty", fillcolor="rgba(220,53,69,0.06)"))
        fig_cs4.add_vrect(x0=65, x1=70, fillcolor="rgba(220,53,69,0.08)", line_width=0,
                          annotation_text="High Inflation Period", annotation_position="top left",
                          annotation_font_color=RED)
        fig_cs4.update_layout(**base_layout("Corpus Depletion — Normal vs Inflation Shock", h=340))
        fig_cs4.update_yaxes(tickformat=".2s", title="Portfolio Balance (₹)")
        st.plotly_chart(fig_cs4, use_container_width=True)

        # Withdrawal escalation
        fig_wd = go.Figure()
        fig_wd.add_trace(go.Bar(x=df_base["Age"], y=df_base["Withdrawal"],
            name="Normal Withdrawal", marker_color="rgba(40,167,69,0.6)"))
        fig_wd.add_trace(go.Bar(x=df_shock["Age"], y=df_shock["Withdrawal"],
            name="Shock Withdrawal", marker_color="rgba(220,53,69,0.6)"))
        fig_wd.update_layout(**base_layout("Annual Withdrawal Escalation: Normal vs Shock", h=280),
            barmode="group")
        fig_wd.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig_wd, use_container_width=True)

        warning_box("""
        A 3% difference in inflation (6% → 9%) over just 5 years can reduce a retiree's corpus longevity by 
        <b>8–12 years</b>. Withdrawals compound faster than expected, creating a "death spiral" where falling 
        balance earns less, while rising withdrawals accelerate depletion.
        """)
        insight_box("""
        <b>Inflation hedges for retirees:</b><br>
        • Maintain 20–30% in equity even in retirement (reduces sequence risk)<br>
        • Hold Sovereign Gold Bonds (SGB) — gold historically beats inflation<br>
        • TIPS equivalent: RBI Inflation-Indexed Bonds<br>
        • Bucket strategy: Keep 3 years' expenses in liquid/debt, rest in equity
        """)
        lesson_box("""
        Never model retirement on a single inflation assumption. Always stress-test with inflation 2–3% above 
        your baseline. The 4% safe withdrawal rule was derived for US markets — for India, use 3–3.5% to account 
        for higher structural inflation.
        """)

    # ── CASE 5 · THE ENTREPRENEUR ────────────────────────────────────────────
    with cs_tabs[4]:
        case_card(
            "Anita Desai — The Entrepreneur",
            "Age 40 · Founder of a growing startup · Irregular income · No EPF/NPS · Equity stake in business",
            color="rgba(30,0,60,0.7)"
        )
        st.markdown("""
        **Situation:** Anita runs a profitable startup valued at ₹3 Crore (she owns 60%). Her personal income 
        is irregular — ranging ₹8L to ₹30L annually. She has no formal retirement savings but has been reinvesting 
        in her business. At 40, she must now plan retirement at 58. How should an entrepreneur structure retirement?
        """)

        col1, col2 = st.columns(2)
        with col1:
            cs5_biz_val   = st.number_input("Business Valuation (₹)", 5000000, 500000000, 30000000, 1000000, key="cs5_bv")
            cs5_stake     = st.slider("Founder's Equity Stake (%)", 20, 100, 60, 5, key="cs5_sk") / 100
            cs5_biz_grow  = st.slider("Business Growth Rate (%) p.a.", 5.0, 40.0, 20.0, 5.0, key="cs5_bg") / 100
            cs5_exit_mult = st.slider("Exit Multiple (EV/Revenue or P/E)", 2, 15, 6, 1, key="cs5_em")
            cs5_avg_inc   = st.number_input("Average Annual Personal Income (₹)", 500000, 10000000, 1500000, 100000, key="cs5_ai")
            cs5_sr        = st.slider("Personal Savings Rate (%)", 5, 60, 25, 5, key="cs5_sr") / 100
            cs5_ret_inv   = st.slider("Personal Investment Return (%)", 6.0, 16.0, 11.0, 0.5, key="cs5_ri") / 100
            cs5_yrs       = 58 - 40

        # Two wealth streams
        # Stream 1: Business exit value
        biz_stake_val  = cs5_biz_val * cs5_stake
        biz_exit_val   = biz_stake_val * (1 + cs5_biz_grow) ** cs5_yrs * cs5_exit_mult / cs5_exit_mult  # growth only
        biz_future_val = biz_stake_val * (1 + cs5_biz_grow) ** cs5_yrs
        # Stream 2: Personal savings
        personal_corp  = fv_growing_annuity(cs5_avg_inc * cs5_sr, 0.05, cs5_ret_inv, cs5_yrs)
        total_net_worth = biz_future_val + personal_corp

        with col2:
            st.markdown(f"""
            <div style="background:rgba(30,0,60,0.5);border:1px solid rgba(255,215,0,0.35);
                border-radius:12px;padding:20px;margin-top:8px;">
            <div style="color:#8892b0;font-size:0.72rem;text-transform:uppercase;margin-bottom:12px;">
                Wealth at Age 58 — Two Streams</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
              <div style="background:rgba(255,215,0,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="color:#8892b0;font-size:0.7rem;">Business Value</div>
                <div style="font-family:'Playfair Display';font-size:1.4rem;color:#FFD700;">₹{biz_future_val/1e7:.1f}Cr</div>
                <div style="font-size:0.68rem;color:#8892b0;">Stake: {cs5_stake*100:.0f}% of biz</div>
              </div>
              <div style="background:rgba(40,167,69,0.1);border-radius:8px;padding:10px;text-align:center;">
                <div style="color:#8892b0;font-size:0.7rem;">Personal Savings</div>
                <div style="font-family:'Playfair Display';font-size:1.4rem;color:#28a745;">₹{personal_corp/1e7:.1f}Cr</div>
                <div style="font-size:0.68rem;color:#8892b0;">₹{cs5_avg_inc*cs5_sr/1000:.0f}K/yr saved</div>
              </div>
            </div>
            <div style="text-align:center;margin-top:14px;">
              <div style="color:#8892b0;font-size:0.72rem;">Combined Net Worth</div>
              <div style="font-family:'Playfair Display';font-size:2rem;color:#FFD700;">₹{total_net_worth/1e7:.2f} Cr</div>
              <div style="font-size:0.72rem;color:#ADD8E6;">Business = {biz_future_val/total_net_worth*100:.0f}% of wealth</div>
            </div>
            </div>""", unsafe_allow_html=True)

        # Business vs Personal savings over time
        yr_range = list(range(1, cs5_yrs + 1))
        biz_vals  = [biz_stake_val * (1 + cs5_biz_grow)**yr for yr in yr_range]
        pers_vals = []
        bal_p, inc_p = 0, cs5_avg_inc
        for yr in yr_range:
            bal_p = bal_p*(1+cs5_ret_inv) + inc_p*cs5_sr
            inc_p *= 1.05
            pers_vals.append(bal_p)
        ages_cs5  = [40 + yr for yr in yr_range]
        combined5 = [b+p for b,p in zip(biz_vals, pers_vals)]

        fig_cs5 = go.Figure()
        fig_cs5.add_trace(go.Bar(x=ages_cs5, y=biz_vals, name="Business Stake Value",
            marker_color="rgba(255,215,0,0.6)"))
        fig_cs5.add_trace(go.Bar(x=ages_cs5, y=pers_vals, name="Personal Savings",
            marker_color="rgba(40,167,69,0.6)"))
        fig_cs5.add_trace(go.Scatter(x=ages_cs5, y=combined5, name="Total Net Worth",
            line=dict(color=LB, width=2.5)))
        fig_cs5.update_layout(**base_layout("Anita's Wealth — Business + Personal Savings", h=330),
            barmode="stack")
        fig_cs5.update_yaxes(tickformat=".2s", title="Value (₹)")
        st.plotly_chart(fig_cs5, use_container_width=True)

        st.markdown("#### 🏦 Retirement Vehicles for Entrepreneurs")
        st.markdown("""
        | Vehicle | Annual Limit | Tax Benefit | Best For |
        |---|---|---|---|
        | **NPS (Tier-I + Tier-II)** | No limit on Tier-II | 80C + 80CCD(1B) — ₹2L deduction | Disciplined pension |
        | **PPF** | ₹1.5L | 80C — EEE status | Debt allocation, tax-free |
        | **ELSS Mutual Funds** | No limit | 80C — 3-yr lock | Equity growth |
        | **REITs / InvITs** | No limit | Dividend + appreciation | Passive income |
        | **Sovereign Gold Bonds** | 4 kg/year | Tax-free on maturity | Inflation hedge |
        | **Self-employed NPS** | Up to 20% of income | Additional 10% NPS deduction | High deduction |
        """)

        warning_box("""
        <b>Concentration Risk:</b> Having 70–80% of wealth in one business is extremely high risk. 
        Even a thriving business can face disruption, regulatory changes, or key-person risk. 
        Entrepreneurs MUST build a parallel financial portfolio independent of their business.
        """)
        lesson_box("""
        For entrepreneurs: treat your salary or director's remuneration as "investor's income" and 
        automate savings before you reinvest in the business. Build a <b>"financial independence fund"</b> 
        — separate from business — that covers basic living costs. The business is the upside; the FI fund is the floor.
        """)

# ───────────────────────────────────────
# TAB 9 – BEHAVIOURAL FINANCE
# ───────────────────────────────────────
with tab9:
    st.markdown("### ⚖️ Behavioural Finance & Retirement Decisions")
    st.markdown('<p style="color:#ADD8E6;font-size:0.83rem;margin:-4px 0 14px 0;padding:7px 14px;background:rgba(0,51,102,0.35);border-left:3px solid #dc3545;border-radius:0 8px 8px 0;">🧠 How cognitive biases derail even the best retirement plans — and what to do about it.</p>', unsafe_allow_html=True)

    bf_tabs = st.tabs([
        "🧠 Key Biases", "📉 The Cost of Panic Selling", "⏰ Hyperbolic Discounting", "🎯 Debiasing Strategies"
    ])

    with bf_tabs[0]:
        st.markdown("#### Common Behavioural Biases in Retirement Planning")
        biases = [
            ("Present Bias", "Valuing immediate rewards over future benefits",
             "Skipping SIP this month to buy a new phone — seems small but repeated over a career, devastating.",
             "Automate SIPs. You can't spend what you never see. Set up auto-debit on salary day."),
            ("Loss Aversion", "Losses feel 2–2.5× more painful than equivalent gains feel good (Kahneman & Tversky)",
             "Exiting equity after a 15% market fall, locking in losses, then missing the recovery.",
             "Pre-commit to a rebalancing rule. Never check portfolio value more than quarterly."),
            ("Overconfidence Bias", "Believing you can time the market or pick winning stocks consistently",
             "Abandoning index funds for direct stocks/crypto, underperforming a simple Nifty 50 SIP.",
             "Track your actual return vs benchmark annually. Data humbles overconfidence."),
            ("Anchoring", "Over-weighting the first piece of information received",
             "Anchoring to the price you paid for a stock; refusing to sell even as fundamentals deteriorate.",
             "Use forward-looking metrics (PE, growth rate) — not your purchase price — for sell decisions."),
            ("Status Quo Bias", "Preferring the current state even when change is better",
             "Never increasing SIP amount despite salary raises — your savings rate shrinks in real terms.",
             "'SIP Step-up': increase SIP by 10% every year automatically. Don't rely on willpower."),
            ("Mental Accounting", "Treating money differently based on its source or label",
             "Spending an annual bonus entirely on lifestyle while struggling with monthly retirement savings.",
             "Pre-commit: 50% of every bonus/windfall goes directly to retirement. No exceptions."),
            ("Recency Bias", "Overweighting recent events in future predictions",
             "Expecting 30% returns every year because markets did well last 2 years. Or panic at every correction.",
             "Read historical return data: Nifty 50 CAGR over 20+ years is ~12–13%. Use this as your base."),
            ("Herd Behaviour", "Following the crowd — buying what everyone is buying",
             "Investing in NFO bubbles, thematic funds, or 'hot' sectors at peak valuations.",
             "When everyone is buying, valuation is highest. Be greedy when others are fearful (Buffett)."),
        ]

        for bname, definition, example, solution in biases:
            with st.expander(f"🧩 {bname}"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"""
                    <div style="background:rgba(0,51,102,0.5);border-radius:10px;padding:14px;margin-bottom:10px;">
                    <div style="color:#FFD700;font-weight:600;margin-bottom:6px;">Definition</div>
                    <div style="font-size:0.82rem;color:#e6f1ff;line-height:1.6;">{definition}</div>
                    </div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background:rgba(220,53,69,0.1);border-left:3px solid #dc3545;border-radius:0 10px 10px 0;
                        padding:12px;margin-bottom:8px;">
                    <div style="color:#dc3545;font-size:0.75rem;font-weight:600;margin-bottom:4px;">REAL-WORLD EXAMPLE</div>
                    <div style="font-size:0.8rem;color:#e6f1ff;line-height:1.6;">{example}</div>
                    </div>
                    <div style="background:rgba(40,167,69,0.1);border-left:3px solid #28a745;border-radius:0 10px 10px 0;
                        padding:12px;">
                    <div style="color:#28a745;font-size:0.75rem;font-weight:600;margin-bottom:4px;">SOLUTION</div>
                    <div style="font-size:0.8rem;color:#e6f1ff;line-height:1.6;">{solution}</div>
                    </div>""", unsafe_allow_html=True)

    with bf_tabs[1]:
        st.markdown("#### 📉 The Catastrophic Cost of Panic Selling")
        st.markdown(
            '<p style="color:#c8d8f0;font-size:0.85rem;line-height:1.7;margin-bottom:14px;">'
            'Simulates what happens when an investor exits the market during corrections vs. staying invested. '
            'Missing even a handful of the best trading days dramatically destroys long-term wealth.</p>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            bf_initial = st.number_input(f"Initial Investment ({curr_sym})",
                                         10_000 if is_inr else 1_000,
                                         10_000_000 if is_inr else 500_000,
                                         1_000_000 if is_inr else 50_000,
                                         50_000 if is_inr else 1_000, key="bf_init")
            bf_sip     = st.number_input(f"Monthly SIP ({curr_sym})",
                                         0,
                                         500_000 if is_inr else 20_000,
                                         10_000 if is_inr else 500,
                                         1_000 if is_inr else 100, key="bf_sip")
            bf_years   = st.slider("Investment Horizon (years)", 5, 40, 20, 1, key="bf_yr")
            bf_ret     = st.slider("Market Annual Return (%)", 8.0, 18.0, 13.0, 0.5, key="bf_ret") / 100
            bf_miss    = st.slider("Best Days Missed (panic selling)", 0, 30, 10, 5, key="bf_miss")

        # Stay invested vs miss best N days
        # Approximate: missing N best days reduces annualized return significantly
        # Real data: Missing 10 best days in 20 years costs ~4% p.a.
        penalty_per_day = 0.004  # ~0.4% per missed day (empirically derived from BSE data)
        bf_ret_miss = max(0.01, bf_ret - bf_miss * penalty_per_day)

        months_total   = bf_years * 12
        r_mo_stay      = bf_ret / 12
        r_mo_miss      = bf_ret_miss / 12

        def simulate_sip(initial, sip, r_mo, months):
            bal = initial
            for _ in range(months):
                bal = bal * (1 + r_mo) + sip
            return bal

        val_stay = simulate_sip(bf_initial, bf_sip, r_mo_stay, months_total)
        val_miss = simulate_sip(bf_initial, bf_sip, r_mo_miss, months_total)
        cost_of_panic = val_stay - val_miss

        with col2:
            m1, m2, m3 = st.columns(3)
            m1.metric("Stay Invested", f"₹{val_stay/1e7:.2f}Cr")
            m2.metric(f"Miss {bf_miss} Best Days", f"₹{val_miss/1e7:.2f}Cr")
            m3.metric("Cost of Panic", f"₹{cost_of_panic/1e5:.1f}L",
                      delta=f"-{cost_of_panic/val_stay*100:.1f}% of wealth",
                      delta_color="inverse")

        # Growth chart
        yrs = list(range(1, bf_years + 1))
        vals_stay_yr = [simulate_sip(bf_initial, bf_sip, r_mo_stay, y*12) for y in yrs]
        vals_miss_yr = [simulate_sip(bf_initial, bf_sip, r_mo_miss, y*12) for y in yrs]

        fig_bf = go.Figure()
        fig_bf.add_trace(go.Scatter(x=yrs, y=vals_stay_yr, name="Stay Invested",
            line=dict(color=GRN, width=3), fill="tozeroy", fillcolor="rgba(40,167,69,0.06)"))
        fig_bf.add_trace(go.Scatter(x=yrs, y=vals_miss_yr, name=f"Miss {bf_miss} Best Days",
            line=dict(color=RED, width=2.5, dash="dash")))
        fig_bf.update_layout(**base_layout(f"Wealth Impact of Missing the {bf_miss} Best Market Days", h=340))
        fig_bf.update_yaxes(tickformat=".2s", title="Portfolio Value (₹)")
        fig_bf.update_xaxes(title="Years")
        st.plotly_chart(fig_bf, use_container_width=True)

        insight_box("""
        BSE Sensex data shows: <b>missing just 10 best trading days in 20 years</b> reduces your final 
        corpus by 30–40%. These best days often come within 2 weeks of the worst days — panic sellers miss both 
        the crash and the recovery. Time IN the market beats timing the market — every time.
        """)

    with bf_tabs[2]:
        st.markdown("#### ⏰ Hyperbolic Discounting — Why We Procrastinate on Saving")
        st.markdown(
            '<p style="color:#c8d8f0;font-size:0.85rem;line-height:1.8;margin-bottom:14px;">'
            'Hyperbolic discounting means we value today far more than the future — and tomorrow becomes '
            '"today" when it arrives, so we keep delaying. This creates the '
            '<b style="color:#FFD700;">procrastination trap</b> in retirement planning.'
            '</p>',
            unsafe_allow_html=True
        )

        delay_years = st.slider("Years of delay before starting SIP", 0, 20, 5, 1)
        monthly_sip = st.number_input(f"Monthly SIP Amount ({curr_sym})",
                                      1_000 if is_inr else 100,
                                      500_000 if is_inr else 20_000,
                                      10_000 if is_inr else 500,
                                      1_000 if is_inr else 100, key="hd_sip")
        hd_ret      = st.slider("Annual Return (%)", 8.0, 18.0, 12.0, 1.0, key="hd_ret") / 100
        hd_years    = st.slider("Total Investment Horizon (years from today)", 10, 40, 30, 1, key="hd_yr")

        def sip_fv(sip, r_annual, years):
            r_mo = r_annual / 12
            return sip * ((1+r_mo)**(years*12) - 1) / r_mo * (1+r_mo)

        vals_by_delay = [sip_fv(monthly_sip, hd_ret, max(0, hd_years - d)) for d in range(0, 21)]
        opportunity_cost = vals_by_delay[0] - vals_by_delay[delay_years]

        m1, m2, m3 = st.columns(3)
        m1.metric("Start Today", f"₹{vals_by_delay[0]/1e7:.2f}Cr")
        m2.metric(f"Start After {delay_years} Years", f"₹{vals_by_delay[delay_years]/1e7:.2f}Cr")
        m3.metric("Opportunity Cost of Delay", f"₹{opportunity_cost/1e5:.1f}L",
                  delta=f"-{opportunity_cost/vals_by_delay[0]*100:.1f}%", delta_color="inverse")

        fig_hd = go.Figure()
        fig_hd.add_trace(go.Bar(x=list(range(0, 21)), y=vals_by_delay,
            marker=dict(color=[GRN if i==0 else (RED if i==delay_years else GOLD)
                               for i in range(21)]),
            text=[f"₹{v/1e7:.1f}Cr" for v in vals_by_delay],
            textposition="outside", textfont=dict(size=8, color="#e6f1ff")))
        fig_hd.update_layout(
            **base_layout("Final Corpus by Years of Delay", h=320,
                          xaxis_extra=dict(title="Years Delayed Before Starting SIP")))
        fig_hd.update_yaxes(tickformat=".2s", title="Final Corpus (₹)")
        st.plotly_chart(fig_hd, use_container_width=True)

        insight_box("""
        Each year of delay compounds against you. A 5-year delay on a ₹10K SIP at 12% for 30 years 
        costs approximately <b>₹50–70 lakhs</b> in lost wealth. The cost of "I'll start next year" 
        is not one year — it's the compounding of that delay across the entire horizon.
        """)

    with bf_tabs[3]:
        st.markdown("#### 🎯 Debiasing Your Retirement Plan")
        strategies = {
            "🤖 Automate Everything": [
                "Set SIPs on salary credit date — not manually each month",
                "Step-up SIP by 10% automatically each April",
                "Auto-rebalance portfolio annually (many platforms support this)",
                "Set direct debit for PPF, NPS contributions"
            ],
            "📅 Pre-Commitment Devices": [
                "ELSS 3-year lock-in prevents panic selling",
                "NPS lock-in until retirement prevents withdrawal",
                "PPF 15-year tenure creates forced long-horizon thinking",
                "Goal-based SIPs (label them 'Retirement 2050', not just 'SIP-1')"
            ],
            "📊 Rules-Based Investing": [
                "Rebalance when any asset class deviates >5% from target allocation",
                "Never check NAV more than once a month",
                "Use a written Investment Policy Statement (IPS) — review annually only",
                "Commit: 50% of all windfalls (bonus, gifts) go to retirement"
            ],
            "🧘 Cognitive Frameworks": [
                "Think in decades, not quarters — 'How will I feel at 70 about this decision?'",
                "Imagine your future self: write a letter from 70-year-old you",
                "'Premortem' exercise: assume retirement failed — what caused it?",
                "Find an accountability partner or fee-only financial advisor"
            ]
        }
        for strategy, points in strategies.items():
            with st.expander(strategy):
                for i, pt in enumerate(points):
                    st.markdown(f"""
                    <div style="padding:10px 14px;margin:4px 0;
                        background:rgba(0,51,102,0.5);
                        border-radius:8px;border-left:3px solid rgba(255,215,0,0.5);
                        font-size:0.84rem;color:#e6f1ff;line-height:1.6;">
                    <span style="color:#FFD700;font-weight:700;margin-right:8px;">✅</span>{pt}
                    </div>""", unsafe_allow_html=True)

        lesson_box("""
        The best retirement plan is one that <b>removes human decision-making from the equation</b>. 
        Automate contributions, lock in long-term vehicles, and commit to rules before emotions arise. 
        Behavioural discipline — not stock-picking — is the primary driver of long-term wealth.
        """)

# ───────────────────────────────────────
# TAB 10 – GLOSSARY & FORMULAS
# ───────────────────────────────────────
with tab10:
    st.markdown("### 📖 Complete Glossary, Formulas & Quick Reference")
    st.markdown('<p style="color:#ADD8E6;font-size:0.83rem;margin:-4px 0 14px 0;padding:7px 14px;background:rgba(0,51,102,0.35);border-left:3px solid #ADD8E6;border-radius:0 8px 8px 0;">📖 A comprehensive reference for all concepts used in this retirement planning suite.</p>', unsafe_allow_html=True)

    gl_tabs = st.tabs(["📐 TVM Formulas", "📑 Retirement Concepts", "🏛️ Indian Instruments", "🌍 Global Benchmarks"])

    with gl_tabs[0]:
        st.markdown("#### Time Value of Money — Master Formula Sheet")

        formulas = [
            ("Future Value (FV)", "FV = PV × (1 + r)ⁿ",
             "PV = Present Value, r = periodic rate, n = number of periods",
             "₹1L invested at 12% for 10 years → FV = 1,00,000 × (1.12)¹⁰ = ₹3,10,585"),
            ("Present Value (PV)", "PV = FV / (1 + r)ⁿ",
             "FV = future amount needed, r = discount rate, n = periods",
             "Need ₹50L in 20 years at 10% return → PV = 50,00,000 / (1.10)²⁰ = ₹7,43,218"),
            ("Future Value of Annuity", "FVA = PMT × [(1+r)ⁿ - 1] / r",
             "PMT = periodic payment, r = rate per period, n = number of periods",
             "₹10K SIP/month at 12% p.a. for 20 years → FV = ₹ 99.9 lakhs"),
            ("Present Value of Annuity", "PVA = PMT × [1 - (1+r)⁻ⁿ] / r",
             "Used to calculate corpus needed for retirement withdrawals",
             "Need ₹5L/year for 25 years at 7% → PVA = ₹58.3L corpus required"),
            ("Growing Annuity FV", "FVGA = PMT × [(1+r)ⁿ - (1+g)ⁿ] / (r - g)",
             "PMT = first payment, g = growth rate of payments, r = return rate",
             "SIP growing 10% annually, starting ₹5K, 12% return, 30 years → massive wealth"),
            ("PMT (Required Payment)", "PMT = FV × r / [(1+r)ⁿ - 1]",
             "How much to invest each period to reach a target FV",
             "Need ₹2Cr in 25 years at 12% → Monthly SIP = ₹9,244"),
            ("NPER (Periods)", "NPER = ln[(FV×r + PMT) / (PV×r + PMT)] / ln(1+r)",
             "How many periods to reach a goal",
             "₹5K SIP at 12%, current savings ₹2L, target ₹1Cr → 18.5 years"),
            ("RATE", "Solve: PV = FV/(1+r)ⁿ + PMT×[(1+r)ⁿ-1]/r numerically",
             "Required return to reach goal — solved using Newton-Raphson/Brent's method",
             "Need ₹3Cr in 20 years, saving ₹15K/month → Required rate = 15.2% p.a."),
            ("Real Return", "(1 + Nominal) / (1 + Inflation) - 1",
             "Fisher equation — removes the effect of inflation",
             "12% nominal, 6% inflation → Real return = (1.12/1.06) - 1 = 5.66%"),
            ("Safe Withdrawal Rate", "SWR = Annual Withdrawal / Starting Corpus",
             "4% rule (Bengen): withdraw 4% of corpus in Year 1, inflation-adjust thereafter",
             "₹2Cr corpus × 4% = ₹8L/year (₹67K/month) sustainable for 30 years"),
            ("Funding Ratio", "FR = Projected Corpus / Required Corpus",
             ">1.0 means fully funded; <1.0 means shortfall exists",
             "Projected ₹3.2Cr / Required ₹2.4Cr = FR of 1.33 = 33% surplus"),
        ]

        for fname, formula, explanation, example in formulas:
            with st.expander(f"📐 {fname}"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"""
                    <div style="background:rgba(0,51,102,0.6);border:1px solid rgba(255,215,0,0.3);
                        border-radius:10px;padding:16px;text-align:center;">
                    <div style="font-family:'DM Mono',monospace;font-size:1rem;color:#FFD700;
                        line-height:1.8;word-break:break-word;">{formula}</div>
                    </div>
                    <div style="margin-top:10px;font-size:0.75rem;color:#8892b0;line-height:1.6;">
                    {explanation}</div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background:rgba(255,215,0,0.07);border-left:3px solid #FFD700;
                        border-radius:0 10px 10px 0;padding:14px;font-size:0.8rem;
                        color:#e6f1ff;line-height:1.7;">
                    <b style="color:#FFD700;">Worked Example:</b><br>{example}
                    </div>""", unsafe_allow_html=True)

    with gl_tabs[1]:
        st.markdown("#### Retirement Planning Concepts — A–Z")
        concepts = {
            "4% Rule (Safe Withdrawal Rate)": "Rule of thumb: withdraw 4% of corpus in year 1, adjust for inflation annually. Based on William Bengen's 1994 study of US market data. For India, 3–3.5% is safer due to higher structural inflation.",
            "Asset Allocation": "Distribution of investments across asset classes (equity, debt, gold, real estate). Generally: (100 − age)% in equity as a starting heuristic. Should reflect risk tolerance and time horizon.",
            "Bucket Strategy": "Divide retirement corpus into 3 buckets: (1) 1–3 years expenses in liquid/FD, (2) 4–10 years in debt funds, (3) 10+ years in equity. Spend from Bucket 1, refill from others.",
            "Corpus": "Total accumulated retirement savings/investments at the time of retirement. The 'nest egg' that must sustain all retirement expenses.",
            "FIRE (Financial Independence, Retire Early)": "Goal of accumulating 25–33× annual expenses to retire much earlier than traditional age. Requires high savings rates (40–70%) and frugal lifestyle.",
            "Funding Gap": "The difference between annual retirement spending and guaranteed income (pension, Social Security). The corpus must cover the gap.",
            "Glide Path": "The shift from higher equity to higher debt allocation as retirement approaches. Most target-date funds follow a glide path automatically.",
            "Income Replacement Ratio": "Percentage of pre-retirement income needed in retirement. Typically 70–80% (housing loan paid off, children independent). Used to estimate retirement spending.",
            "Inflation Risk": "The risk that inflation erodes the purchasing power of savings. The greatest long-term threat to retirement security.",
            "Longevity Risk": "The risk of outliving your money. With life expectancy increasing, plan for 25–35 years in retirement.",
            "Monte Carlo Simulation": "Statistical technique running thousands of scenarios with random returns to estimate the probability of retirement success.",
            "Rebalancing": "Restoring original asset allocation periodically (annually). Forces buy-low/sell-high discipline. Critical to maintaining risk profile.",
            "Sequence of Returns Risk": "The order of investment returns matters in retirement. Poor returns early in retirement are far more damaging than poor returns late, because a depleted corpus can't recover.",
            "SWP (Systematic Withdrawal Plan)": "Regularly withdrawing a fixed amount from a mutual fund — the retirement-phase equivalent of an SIP.",
            "Time Value of Money (TVM)": "A rupee today is worth more than a rupee tomorrow because of its earning potential. The foundation of all retirement mathematics.",
        }
        for term, definition in concepts.items():
            st.markdown(f"""
            <div style="background:rgba(0,51,102,0.35);border:1px solid rgba(173,216,230,0.15);
                border-radius:10px;padding:14px 18px;margin-bottom:8px;">
            <div style="color:#FFD700;font-weight:600;font-size:0.85rem;margin-bottom:6px;">{term}</div>
            <div style="color:#e6f1ff;font-size:0.8rem;line-height:1.7;">{definition}</div>
            </div>""", unsafe_allow_html=True)

    with gl_tabs[2]:
        st.markdown("#### 🏛️ Indian Retirement Instruments — Comprehensive Guide")
        instruments = [
            ("EPF — Employees' Provident Fund", "8.15% (FY24)", "Till retirement", "EEE",
             "Mandatory for employees in establishments with 20+ workers. Both employer (12%) and employee (12%) contribute on basic salary. Withdraw 75% after 1 month of unemployment."),
            ("PPF — Public Provident Fund", "7.1% (quarterly revision)", "15 years (extendable)", "EEE",
             "Best debt instrument for retail investors. ₹500–₹1.5L/year limit. Loans available from Year 3. Partial withdrawal from Year 7. Sovereign guarantee."),
            ("NPS — National Pension System", "Market-linked (8–12% historically)", "Till 60", "EET (60% tax-free)",
             "Mandatory 40% in annuity on maturity. Additional ₹50K deduction under 80CCD(1B) over and above 80C limit. Tier-I locked till 60; Tier-II liquid."),
            ("Sukanya Samriddhi Yojana", "8.2% (FY24)", "21 years or girl's marriage", "EEE",
             "For daughters under 10. Minimum ₹250, maximum ₹1.5L/year. Great for daughter's education and marriage corpus."),
            ("Senior Citizen Savings Scheme (SCSS)", "8.2% (FY24)", "5 years (extendable)", "Taxable interest",
             "Available to 60+ years. Up to ₹30L investment. Quarterly interest payouts ideal for retirement income."),
            ("RBI Floating Rate Savings Bonds", "8.05% (linked to NSC rate)", "7 years", "Taxable",
             "Sovereign guarantee, floating rate linked to NSC. Better than FDs for safety. Semi-annual interest payouts."),
            ("ELSS Mutual Funds", "Market-linked (12–15% historical)", "3-year lock-in", "LTCG above ₹1L taxed at 10%",
             "Shortest lock-in under 80C. Equity exposure for wealth creation. Best for 80C utilization when retirement is 10+ years away."),
            ("Annuity Plans (LIC / private insurers)", "5–7% (immediate annuity)", "Lifetime", "Taxable as income",
             "Guaranteed income for life. Protects against longevity risk. Typically, allocate 30–40% of NPS corpus to annuity as required."),
        ]
        for iname, rate, tenure, tax, details in instruments:
            with st.expander(f"🏦 {iname}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Rate", rate)
                col2.metric("Tenure", tenure)
                col3.metric("Tax Status", tax)
                col4.metric("Type", "Debt/Govt" if any(x in iname for x in ["PPF","EPF","SCSS","RBI","Sukanya"]) else "Market-linked")
                st.markdown(f"""
                <div style="background:rgba(0,51,102,0.3);border-radius:8px;padding:12px;
                    font-size:0.8rem;color:#e6f1ff;line-height:1.7;margin-top:8px;">{details}</div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.25);
            border-radius:12px;padding:16px;margin-top:16px;">
        <div style="color:#FFD700;font-weight:600;margin-bottom:10px;">💡 Optimal Tax-Saving Stack (₹2L+ savings per year)</div>
        <div style="font-size:0.8rem;color:#e6f1ff;line-height:2;">
        1. <b>EPF</b> — mandatory, keep it (12% employer match = 100% return)<br>
        2. <b>PPF ₹1.5L</b> — fully utilise 80C, EEE status<br>
        3. <b>NPS ₹50K</b> — additional 80CCD(1B) deduction, builds pension<br>
        4. <b>ELSS</b> — any remaining 80C room + equity growth<br>
        5. <b>SGB / REITs</b> — beyond 80C, for diversification and inflation hedging
        </div></div>""", unsafe_allow_html=True)

    with gl_tabs[3]:
        st.markdown("#### 🌍 Global Retirement Benchmarks & Comparisons")
        st.markdown("""
        | Metric | India | USA | UK | Singapore | Japan |
        |---|---|---|---|---|---|
        | **Avg. Retirement Age** | 58–60 | 65 | 66 | 63 | 65 |
        | **Life Expectancy** | 70 | 79 | 81 | 85 | 84 |
        | **Avg. Retirement Duration** | 10–15 yrs | 14 yrs | 15 yrs | 22 yrs | 19 yrs |
        | **Safe Withdrawal Rate** | 3–3.5% | 4% | 3.5% | 3% | 2.5% |
        | **Inflation (Historical)** | 5–7% | 2–3% | 2–3% | 1–2% | 0–1% |
        | **Equity Historical Return** | 12–14% (Nifty) | 10% (S&P 500) | 7–8% | 8–9% | 5–6% |
        | **Real Return (Equity)** | 6–8% | 7–8% | 5–6% | 7–8% | 5–6% |
        | **Primary Retirement Vehicle** | EPF + NPS | 401(k) + IRA | ISA + Pension | CPF | iDeCo + Kokumin |
        | **Corpus Multiple Required** | 25–30× | 25× | 28× | 33× | 40× |
        """)

        st.markdown("""
        <div style="background:rgba(0,51,102,0.4);border:1px solid rgba(173,216,230,0.2);
            border-radius:12px;padding:16px;margin-top:16px;">
        <div style="color:#FFD700;font-size:0.9rem;font-weight:600;margin-bottom:10px;">🔑 Key Takeaways for Indian Planners</div>
        <div style="font-size:0.8rem;color:#e6f1ff;line-height:2;">
        • India's higher inflation (~6%) means you need a <b>higher corpus multiple (28–33×)</b> than the Western 25× rule<br>
        • India's shorter average retirement duration (low life expectancy vs Singapore/Japan) partially offsets this<br>
        • Nifty 50 at 12–14% CAGR historically gives <b>real returns of 6–8%</b> — among the world's best<br>
        • Unlike the West, Indian retirees often have <b>family support</b> reducing pure financial need by 20–30%<br>
        • Healthcare costs in India are growing at 10–15% p.a. — a critical underestimated retirement expense<br>
        • The EEE status of PPF/EPF is unique globally — <b>maximise these before taxable instruments</b>
        </div></div>""", unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:16px;font-size:0.72rem;color:#8892b0;line-height:2;">
    <span style="color:#FFD700;font-family:'Playfair Display';font-size:0.85rem;">
        🏔️ The Mountain Path Academy — World of Finance
    </span><br>
    <b style="color:#ADD8E6;">Prof. V. Ravichandran</b> · 28+ Years Corporate Finance & Banking · 10+ Years Academic Excellence<br>
    Visiting Faculty: NMIMS Bangalore · BITS Pilani · RV University · Goa Institute of Management<br>
    <a href="https://themountainpathacademy.com" target="_blank" style="color:#FFD700;">themountainpathacademy.com</a> &nbsp;|&nbsp;
    <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:#ADD8E6;">LinkedIn</a> &nbsp;|&nbsp;
    <a href="https://github.com/trichyravis" target="_blank" style="color:#ADD8E6;">GitHub</a><br>
    <span style="font-size:0.65rem;">Disclaimer: This tool is for educational purposes only and does not constitute financial advice.</span>
</div>
""", unsafe_allow_html=True)
