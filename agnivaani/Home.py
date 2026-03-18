import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Agnivāṇī — Stubble Burning Agent",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');
*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.hero { padding: 2rem 0 1rem 0; }
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem; color: #f5a623; margin: 0; line-height: 1.1;
}
.hero-sub { font-size: 1rem; color: #8fa8c8; margin: 0.5rem 0 1.5rem 0; }

.kpi { background: #111b2e; border: 1px solid #1e3352; border-radius: 12px; padding: 1.2rem; text-align: center; }
.kpi-val { font-size: 1.8rem; font-weight: 700; }
.kpi-lbl { font-size: 0.72rem; color: #8fa8c8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.section { font-size: 1.1rem; font-weight: 700; color: #e8eef8;
    border-left: 3px solid #f5a623; padding-left: 10px; margin: 1.8rem 0 1rem 0; }

.card { background: #111b2e; border: 1px solid #1e3352; border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem; }
.card-title { font-size: 0.85rem; font-weight: 700; color: #f5a623; margin-bottom: 0.3rem; }
.card-body  { font-size: 0.82rem; color: #8fa8c8; line-height: 1.6; }

.step { display:flex; gap:12px; align-items:flex-start; margin-bottom:1rem; }
.step-num { background:#f5a62322; color:#f5a623; font-weight:700; font-size:0.85rem;
    border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.step-content h4 { color:#e8eef8; font-size:0.88rem; margin:0 0 3px 0; }
.step-content p  { color:#8fa8c8; font-size:0.8rem; margin:0; line-height:1.5; }

.quote { background:#0d1a0d; border:1px solid #1a5c1a; border-left:3px solid #2ecc71;
    border-radius:8px; padding:1rem 1.2rem; font-size:0.85rem; color:#a8d8a8; line-height:1.8; margin:0.8rem 0; }
.quote b { color:#2ecc71; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔥 Agnivāṇī")
    st.divider()
    st.markdown("🏠 [Home](/)")
    st.markdown("📊 [Dashboard](/Dashboard)")
    st.markdown("🌬️ [Smoke_Trajectory](/Smoke_Trajectory)")
    st.markdown("💰 [Biomass_Economics](/Biomass_Economics)")
    st.markdown("📞 [Voice_Call_Log](/Voice_Call_Log)")
    st.divider()

# ── HERO ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🔥 Agnivāṇī</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Nocturnal Biomass-Arbitrage & Smoke-Trajectory Agent · Punjab & Haryana Agricultural Belt</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────
cols = st.columns(5)
kpis = [
    ("35M t",    "Stubble burned per season",    "#f5a623"),
    ("~700",     "Delhi PM2.5 peak (µg/m³)",     "#ff4e1a"),
    ("₹2,400",   "Bio-CNG price per tonne",      "#2ecc71"),
    ("72h",      "NeuralGCM forecast window",    "#8fa8c8"),
    ("Free",     "Cost to farmers",              "#d4a843"),
]
for col, (val, lbl, color) in zip(cols, kpis):
    col.markdown(f'<div class="kpi"><div class="kpi-val" style="color:{color}">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.divider()

# ── THE PROBLEM ──────────────────────────────────────────────────────────────
st.markdown('<div class="section">The Problem</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1, 1])
with col_a:
    st.markdown("""
Every **October–November**, Punjab and Haryana farmers burn rice stubble to clear fields before wheat sowing.
This 2–3 week window causes **60–80% of Delhi's winter PM2.5 spike**.

**Why farmers burn:**
- Manual removal costs ₹5,000–8,000/acre — unaffordable
- No one offers a better deal *in real time*
- Government penalties are resented, not effective

**What burning costs everyone:**
- 17.9 million tonnes CO₂ equivalent per season
- Delhi AQI regularly exceeds 500 (Hazardous)
- Thousands hospitalised with respiratory illness
""")
with col_b:
    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=[55,95,180,160,130,90], name="Without burning",
        line=dict(color="#2ecc71", width=2), fill="tozeroy", fillcolor="rgba(46,204,113,0.1)"))
    fig.add_trace(go.Scatter(x=months, y=[58,210,487,290,175,95], name="With stubble burning",
        line=dict(color="#ff4e1a", width=2.5), fill="tozeroy", fillcolor="rgba(255,78,26,0.12)"))
    fig.update_layout(
        title="Delhi AQI — Seasonal Pattern (PM2.5 µg/m³)",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=260, margin=dict(l=0,r=0,t=40,b=0),
        legend=dict(bgcolor="#111b2e", bordercolor="#1e3352", borderwidth=1),
        yaxis=dict(gridcolor="#1e3352"), xaxis=dict(gridcolor="#1e3352"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section">How Agnivāṇī Works</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    steps = [
        ("1", "Field Intelligence",   "Google AMED API detects recently harvested fields at 10-30m resolution. The agent identifies fields at risk of burning within 48-72 hours."),
        ("2", "Wind & Smoke Forecast","NeuralGCM predicts the 72-hour smoke trajectory for each field. A Smoke Risk Index (SRI) is computed for every GPS coordinate."),
        ("3", "Proactive Call",       "If smoke trajectory hits Delhi or Chandigarh, VoicERA calls the farmer in Punjabi — *before* any burning starts — with a cash offer."),
        ("4", "Nocturnal Detection",  "Sentinel-3 SLSTR scans at night. If a fire is detected, a Dynamic Buy-Back call is triggered within minutes at a premium price."),
        ("5", "Biomass Brokerage",    "The agent books a Bio-CNG collection truck and routes payment to the farmer's PM-Kisan DBT account within 24 hours."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="step">
            <div class="step-num">{num}</div>
            <div class="step-content"><h4>{title}</h4><p>{desc}</p></div>
        </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("**What the farmer hears:**")
    st.markdown("""
    <div class="quote">
        <b>ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਵੀਰ ਜੀ।</b> ("Sat Sri Akal, Veer ji.")<br><br>
        "Our satellite shows your field in [Village] was harvested today.
        If you burn tomorrow, the wind will carry smoke toward Delhi.<br><br>
        A Bio-CNG plant is buying stubble at <b>₹2,400/tonne</b>.
        I can book a truck for 8:00 AM tomorrow — payment to your PM-Kisan account within 24 hours.
        Shall I confirm?"
    </div>
    <div class="quote" style="border-left-color:#f5a623; background:#1a1200; color:#d4b870">
        <b>If fire already detected:</b><br>
        "The fire is small. Douse it now — I'll book the remaining 90% at
        <b>₹3,100/tonne (premium)</b>. Shall I confirm the booking?"
    </div>
    """, unsafe_allow_html=True)

    # Compliance chart
    labels = ['Penalty threats', 'Social pressure', 'Env. appeal', 'Financial offer', 'Real-time offer']
    vals   = [22, 35, 41, 78, 85]
    fig2 = go.Figure(go.Bar(x=vals, y=labels, orientation='h',
        marker_color=["#4a6080","#6a80a0","#8fa8c8","#d4a843","#2ecc71"],
        text=[f"{v}%" for v in vals], textposition='outside',
        textfont=dict(color='#8fa8c8', size=10)))
    fig2.update_layout(
        title="Farmer Compliance by Intervention Type (est.)",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=230, margin=dict(l=0,r=50,t=40,b=0),
        xaxis=dict(range=[0,100], gridcolor="#1e3352", ticksuffix="%"),
        yaxis=dict(gridcolor="#1e3352"),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── TECH STACK ───────────────────────────────────────────────────────────────
st.markdown('<div class="section">Technology Stack (All Free APIs)</div>', unsafe_allow_html=True)
cols = st.columns(4)
tech = [
    ("🛰️", "Google AMED API",     "Field Intelligence",      "10-30m resolution crop monitoring. Tracks Harvest-Ready status, updated every 15 days.",            "#f5a623"),
    ("🌙", "Sentinel-3 SLSTR",    "Night Fire Detection",    "F1 & S7 fire channels scan at night — catches evasion burns with higher sensitivity than MODIS.",     "#ff4e1a"),
    ("🗣️","Bhashini VoicERA",    "Multilingual Voice AI",   "Punjabi/Haryanvi voice agent on India's BHASHINI platform. AWWER-tuned for agricultural vocabulary.", "#2ecc71"),
    ("🌀", "Google NeuralGCM",    "Smoke Trajectory",        "72-hour ML + NWP hybrid model. Computes smoke path for each field GPS coordinate in real time.",      "#8fa8c8"),
]
for col, (icon, name, role, desc, color) in zip(cols, tech):
    col.markdown(f"""
    <div class="card" style="border-top:2px solid {color}">
        <div style="font-size:1.6rem;margin-bottom:8px">{icon}</div>
        <div class="card-title" style="color:{color}">{name}</div>
        <div style="font-size:0.68rem;color:#4a6080;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">{role}</div>
        <div class="card-body">{desc}</div>
    </div>""", unsafe_allow_html=True)

# ── IMPACT ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section">Projected Impact at Scale</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    pct = list(range(0, 101, 10))
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=pct, y=[p*0.179 for p in pct], name="CO₂ Avoided (M tonnes)",
        line=dict(color="#2ecc71", width=2)))
    fig3.add_trace(go.Scatter(x=pct, y=[p*1.52 for p in pct], name="Delhi AQI Reduction",
        line=dict(color="#8fa8c8", width=2), yaxis="y2"))
    fig3.update_layout(
        title="Impact vs. Stubble Diversion Rate",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8", height=280,
        xaxis=dict(title="Fields Diverted (%)", gridcolor="#1e3352", ticksuffix="%"),
        yaxis=dict(title="CO₂ Avoided (M t)", gridcolor="#1e3352"),
        yaxis2=dict(title="AQI Reduction", overlaying="y", side="right"),
        legend=dict(bgcolor="#111b2e", bordercolor="#1e3352", borderwidth=1),
        margin=dict(l=0,r=0,t=40,b=0),
    )
    st.plotly_chart(fig3, use_container_width=True)
with c2:
    districts = ["Ludhiana","Amritsar","Patiala","Sangrur","Moga","Bathinda","Ferozepur"]
    rev_cr    = [a * 2.4 * 0.6 * 2400 / 100 for a in [3.8,2.9,3.1,2.4,1.8,2.2,1.9]]
    fig4 = go.Figure(go.Bar(x=districts, y=rev_cr,
        marker=dict(color=rev_cr, colorscale=[[0,"#1a3a1a"],[0.5,"#2ecc71"],[1,"#f5a623"]]),
        text=[f"₹{v:.0f}Cr" for v in rev_cr], textposition="outside",
        textfont=dict(color="#8fa8c8", size=10)))
    fig4.update_layout(
        title="Potential Farmer Revenue by District (@ 60% diversion)",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8", height=280,
        yaxis=dict(title="Revenue (₹ Crore)", gridcolor="#1e3352"),
        xaxis=dict(gridcolor="#1e3352"), margin=dict(l=0,r=0,t=40,b=0),
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.caption("Agnivāṇī v2.0 · Climate-Tech Solution · Northwestern India Agricultural Belt · Data: ISRO VEDAS · Copernicus SLSTR NRT · Google DeepMind NeuralGCM · MeitY Bhashini")
