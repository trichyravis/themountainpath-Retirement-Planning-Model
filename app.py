
import streamlit as st
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
    --muted:    #8892b0;
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

/* ─── Sliders & Inputs ─── */
[data-testid="stSlider"] > div > div > div {
    background: var(--gold) !important;
}
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: rgba(0,51,102,0.4) !important;
    border: 1px solid rgba(255,215,0,0.3) !important;
    color: var(--txt) !important;
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
}
.stSlider label, .stNumberInput label, .stSelectbox label {
    color: var(--lightblue) !important;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
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

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.3);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    border-radius: 8px;
    padding: 8px 18px;
    letter-spacing: 0.04em;
}
.stTabs [aria-selected="true"] {
    background: var(--darkblue) !important;
    color: var(--gold) !important;
    border: 1px solid rgba(255,215,0,0.35) !important;
}

/* ─── Expanders ─── */
.streamlit-expanderHeader {
    background: rgba(0,51,102,0.4) !important;
    border: 1px solid rgba(173,216,230,0.2) !important;
    border-radius: 8px !important;
    color: var(--lightblue) !important;
    font-weight: 500;
}

/* ─── Dividers ─── */
hr { border-color: rgba(255,215,0,0.15) !important; }

/* ─── DataFrames ─── */
.stDataFrame { border: 1px solid rgba(255,215,0,0.15) !important; border-radius: 8px; }
.stDataFrame th { background: var(--darkblue) !important; color: var(--gold) !important; }
.stDataFrame td { background: rgba(17,34,64,0.7) !important; color: var(--txt) !important; }

/* ─── Success / Warning / Error ─── */
.stAlert { border-radius: 10px; border-left: 4px solid; }

/* hide hamburger & footer */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def fmt_inr(n, decimals=0):
    """Format number as Indian Rupee / generic currency with ₹ or $ symbol."""
    if abs(n) >= 1e7:
        return f"₹{n/1e7:.2f} Cr"
    elif abs(n) >= 1e5:
        return f"₹{n/1e5:.2f} L"
    else:
        return f"₹{n:,.{decimals}f}"

def fmt_usd(n):
    if abs(n) >= 1e6:
        return f"${n/1e6:.2f}M"
    elif abs(n) >= 1e3:
        return f"${n/1e3:.1f}K"
    else:
        return f"${n:,.0f}"

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
    currency     = st.selectbox("Currency", ["₹ INR (Lakhs)", "$ USD"])
    curr_sym     = "₹" if "INR" in currency else "$"
    is_inr       = "INR" in currency

    curr_income  = st.number_input(f"Annual Income ({curr_sym})", 100000, 100000000, 1500000 if is_inr else 75000, 50000)
    income_growth= st.slider("Income Growth Rate (%)", 0.0, 15.0, 7.0 if is_inr else 3.0, 0.5) / 100
    savings_rate = st.slider("Savings Rate (% of Income)", 1.0, 50.0, 20.0 if is_inr else 15.0, 0.5) / 100
    curr_savings = st.number_input(f"Current Savings ({curr_sym})", 0, 500000000, 500000 if is_inr else 25000, 10000)

    st.markdown("## 📈 Returns & Inflation")
    pre_ret_return  = st.slider("Pre-Retirement Return (%)", 1.0, 20.0, 12.0 if is_inr else 8.0, 0.5) / 100
    post_ret_return = st.slider("Post-Retirement Return (%)", 1.0, 15.0, 7.0 if is_inr else 5.0, 0.5) / 100
    inflation_rate  = st.slider("Inflation Rate (%)", 0.5, 12.0, 6.0 if is_inr else 3.0, 0.5) / 100
    tax_rate        = st.slider("Tax Rate on Withdrawals (%)", 0.0, 40.0, 20.0 if is_inr else 15.0, 1.0) / 100

    st.markdown("## 🏠 Retirement Spending")
    desired_spending = st.number_input(f"Desired Annual Spending Today ({curr_sym})", 
                                        100000, 50000000, 1000000 if is_inr else 50000, 50000)
    replacement_ratio= st.slider("Income Replacement Ratio (%)", 40.0, 100.0, 75.0, 5.0) / 100
    pension_income   = st.number_input(f"Annual Pension / Social Security ({curr_sym})", 
                                        0, 5000000, 120000 if is_inr else 18000, 10000)
    other_income     = st.number_input(f"Other Retirement Income ({curr_sym})", 
                                        0, 5000000, 0, 10000)

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
annual_gap_after_tax = annual_gap / (1 - tax_rate)

# Required corpus (PV of retirement annuity - real return)
required_corpus    = pv_annuity(annual_gap_after_tax, post_real_ret, years_in_ret)

# Projected savings (FV of current savings + FV of growing annuity)
fv_current         = curr_savings * (1 + pre_ret_return) ** years_to_ret
fv_contributions   = fv_growing_annuity(ann_savings, income_growth, pre_ret_return, years_to_ret)
projected_savings  = fv_current + fv_contributions

surplus_shortfall  = projected_savings - required_corpus
funding_ratio      = projected_savings / required_corpus if required_corpus > 0 else 0
safe_wr            = annual_gap / projected_savings if projected_savings > 0 else 0

# Required monthly savings to meet corpus
if pre_real_ret > 0:
    req_monthly_pmt = (required_corpus - fv_current) * pre_real_ret / ((1+pre_real_ret)**years_to_ret - 1) / 12
else:
    req_monthly_pmt = (required_corpus - fv_current) / (years_to_ret * 12)

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
# ─── MAIN TABS ────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard", "📈 Savings Growth", "🏦 Retirement Needs",
    "💸 Withdrawal Plan", "🔬 Sensitivity", "🎲 Monte Carlo", "📚 TVM Basics"
])

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

        # Key metrics summary card
        st.markdown(f"""
        <div style="background:rgba(0,51,102,0.5);border:1px solid rgba(255,215,0,0.2);
            border-radius:12px;padding:18px;font-size:0.8rem;line-height:2;">
        <div style="color:#FFD700;font-family:'Playfair Display';font-size:0.95rem;margin-bottom:8px;">
            📋 Plan Summary
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
            <span style="color:#8892b0;">Annual Savings</span>
            <span style="color:#ADD8E6;text-align:right;">{fmt(ann_savings)}</span>
            <span style="color:#8892b0;">Monthly Savings</span>
            <span style="color:#ADD8E6;text-align:right;">{fmt(monthly_savings)}</span>
            <span style="color:#8892b0;">Spending @ Retirement</span>
            <span style="color:#ADD8E6;text-align:right;">{fmt(spending_at_ret)}</span>
            <span style="color:#8892b0;">Annual Funding Gap</span>
            <span style="color:#ADD8E6;text-align:right;">{fmt(annual_gap_after_tax)}</span>
            <span style="color:#8892b0;">Pre-Ret Real Return</span>
            <span style="color:#ADD8E6;text-align:right;">{pre_real_ret*100:.2f}%</span>
            <span style="color:#8892b0;">Post-Ret Real Return</span>
            <span style="color:#ADD8E6;text-align:right;">{post_real_ret*100:.2f}%</span>
            <span style="color:#8892b0;">Req. Monthly Savings</span>
            <span style="color:{'#28a745' if req_monthly_pmt<=monthly_savings else '#dc3545'};text-align:right;font-weight:600;">
                {fmt(req_monthly_pmt)}
            </span>
            <span style="color:#8892b0;">Current Monthly Savings</span>
            <span style="color:#FFD700;text-align:right;font-weight:600;">{fmt(monthly_savings)}</span>
        </div>
        </div>""", unsafe_allow_html=True)

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
        st.caption("Savings Rate (rows) × Pre-Retirement Return (columns)")
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
        st.caption("Retirement Age (rows) × Inflation Rate (columns)")
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
    st.caption("Adjust inputs to see how TVM formulas power retirement planning")

    tvm1, tvm2, tvm3, tvm4, tvm5 = st.tabs(["FV — Future Value","PV — Present Value","PMT — Payment","NPER — Periods","RATE"])

    with tvm1:
        c1,c2 = st.columns(2)
        with c1:
            pv_in = st.number_input("Present Value (PV)", 1000, 10000000, 100000, 10000, key="fv_pv")
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
            fv_in2 = st.number_input("Future Amount Needed", 100000, 100000000, 10000000, 500000, key="pv_fv")
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
            target_fv = st.number_input("Target Future Value", 100000, 100000000, 10000000, 500000, key="pmt_fv")
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
            mo_sav  = st.number_input("Monthly Savings", 1000, 1000000, 25000 if is_inr else 1000, 1000, key="np_ms")
            curr_sv = st.number_input("Current Savings",  0, 50000000, 500000 if is_inr else 50000, 10000, key="np_cs")
            goal_am = st.number_input("Target Amount",   100000, 500000000, 10000000 if is_inr else 1000000, 100000, key="np_ga")
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
            curr_sv5 = st.number_input("Current Savings",   0, 50000000, 500000 if is_inr else 50000, 10000, key="rt_cs")
            mo_con5  = st.number_input("Monthly Contribution", 1000, 1000000, 25000 if is_inr else 1000, 1000, key="rt_mc")
            target5  = st.number_input("Target Corpus", 100000, 500000000, 20000000 if is_inr else 1500000, 100000, key="rt_tg")
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

# ─── FOOTER ──────────────────────────────────────────────────────────────────
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
