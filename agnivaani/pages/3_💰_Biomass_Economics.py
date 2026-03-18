import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Biomass Economics — Agnivāṇī", page_icon="💰", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');
*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.section { font-size:1.1rem; font-weight:700; color:#e8eef8;
    border-left:3px solid #2ecc71; padding-left:10px; margin:1.5rem 0 0.8rem 0; }
.kpi { background:#0d1a0d; border:1px solid #1a5c1a; border-radius:10px; padding:1rem; text-align:center; }
.kpi-val { font-size:1.8rem; font-weight:700; color:#2ecc71; }
.kpi-lbl { font-size:0.68rem; color:#8fa8c8; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }
.plant { background:#111b2e; border:1px solid #1e3352; border-radius:8px; padding:12px 14px; margin-bottom:6px; }
.plant h4 { color:#d4a843; font-size:0.85rem; margin-bottom:4px; }
.plant p  { color:#8fa8c8; font-size:0.78rem; line-height:1.5; margin:0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔥 Agnivāṇī")
    st.divider()
    st.page_link("Home.py",                        label="🏠 Home")
    st.page_link("pages/1_📊_Dashboard.py",        label="📊 Dashboard")
    st.page_link("pages/2_🌬️_Smoke_Trajectory.py", label="🌬️ Smoke Trajectory")
    st.page_link("pages/3_💰_Biomass_Economics.py",label="💰 Biomass Economics")
    st.page_link("pages/4_📞_Voice_Call_Log.py",   label="📞 Voice Call Log")
    st.divider()
    st.markdown("**💰 Calculator**")
    field_area     = st.number_input("Field area (hectares)", 1.0, 20.0, 6.2, 0.1)
    stubble_yield  = st.slider("Stubble yield (t/ha)", 2.0, 6.0, 3.5, 0.1)
    base_price     = st.slider("Bio-CNG price (₹/tonne)", 1500, 4000, 2400, 100)
    dyn_premium    = st.slider("Dynamic premium (%)", 10, 60, 29, 1)
    transport_cost = st.slider("Transport cost (₹/tonne)", 200, 800, 420, 10)
    divert_pct     = st.slider("Residue saved (%)", 50, 100, 90, 5)
    st.divider()
    st.caption("Prices: SATAT scheme · MNRE · Market data")

# ── CALC ─────────────────────────────────────────────────────────────────────
total_stubble = field_area * stubble_yield
saved_stubble = total_stubble * divert_pct / 100
gross_base    = saved_stubble * base_price
gross_dyn     = saved_stubble * base_price * (1 + dyn_premium/100)
transport_tot = saved_stubble * transport_cost
net_base      = gross_base - transport_tot
net_dyn       = gross_dyn  - transport_tot

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("## 💰 Biomass Arbitrage Engine")
st.caption("Making stubble worth MORE unburnt than burnt — delivered in real time to farmers")

# ── KPIs ─────────────────────────────────────────────────────────────────────
cols = st.columns(5)
for col, (val, lbl) in zip(cols, [
    (f"{total_stubble:.1f} t",       "Total stubble"),
    (f"{saved_stubble:.1f} t",       "Biomass recovered"),
    (f"₹{net_base/1000:.1f}K",       "Net income (base)"),
    (f"₹{net_dyn/1000:.1f}K",        "Net income (dynamic)"),
    (f"₹{(net_dyn)/1000:.1f}K",      "vs. Burning (gain)"),
]):
    col.markdown(f'<div class="kpi"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.divider()
left, right = st.columns([1.1, 0.9])

with left:
    st.markdown('<div class="section">📊 Revenue Breakdown</div>', unsafe_allow_html=True)
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative","relative","relative","total","relative","total"],
        x=["Stubble value\n(gross)","Transport\ncost","Collection\nfee","Net income\n(base)","Dynamic\npremium","Net income\n(buyback)"],
        y=[gross_base, -transport_tot, -gross_base*0.03, 0, gross_dyn-gross_base, 0],
        text=[f"₹{gross_base/1000:.1f}K",f"-₹{transport_tot/1000:.1f}K",f"-₹{gross_base*0.03/1000:.1f}K",
              f"₹{net_base/1000:.1f}K",f"+₹{(gross_dyn-gross_base)/1000:.1f}K",f"₹{net_dyn/1000:.1f}K"],
        textposition="outside",
        decreasing=dict(marker_color="#ff4e1a"),
        increasing=dict(marker_color="#2ecc71"),
        totals=dict(marker_color="#f5a623"),
        connector=dict(line=dict(color="#1e3352",width=1.5)),
    ))
    fig_wf.update_layout(paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=320, margin=dict(l=0,r=0,t=20,b=0),
        yaxis=dict(title="₹",gridcolor="#1e3352"), xaxis=dict(gridcolor="#1e3352"))
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown('<div class="section">⚖️ Burn vs. Sell</div>', unsafe_allow_html=True)
    fig_cmp = go.Figure(go.Bar(
        x=["Burn\n(status quo)","Sell base\nprice","Dynamic buyback\n(Agnivāṇī)"],
        y=[0, net_base, net_dyn],
        marker_color=["#4a6080","#f5a623","#2ecc71"],
        text=[f"₹{v/1000:.1f}K" for v in [0, net_base, net_dyn]],
        textposition="outside", textfont=dict(color="#e8eef8", size=13)
    ))
    fig_cmp.update_layout(paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=270, margin=dict(l=0,r=0,t=20,b=0),
        yaxis=dict(title="Farmer income (₹)",gridcolor="#1e3352"), xaxis=dict(gridcolor="#1e3352"))
    st.plotly_chart(fig_cmp, use_container_width=True)

with right:
    st.markdown('<div class="section">🏭 Bio-CNG Plant Network</div>', unsafe_allow_html=True)
    plants = [
        ("Sangrur Bioenergy Pvt. Ltd.", "Sangrur", 200, 2400, 62,  True),
        ("Punjab Agro Industries Corp.","Ludhiana",150, 2350, 38,  True),
        ("Haryana Bio-CNG (HKRN)",      "Karnal",  300, 2500, 120, True),
        ("IFFCO Kisan Bio-Energy",       "Patiala", 250, 2420, 78,  True),
        ("Replus Engi. Services",        "Amritsar",100, 2280, 45,  False),
    ]
    for name, dist, cap, price, km, cert in plants:
        net_p = price - transport_cost
        cert_str = "✅ SATAT Certified" if cert else "⚠️ Non-certified"
        st.markdown(f"""
        <div class="plant">
            <h4>{name}</h4>
            <p>📍 {dist} · {km} km · {cert_str}<br>
            ⚡ Capacity: {cap} TPD<br>
            💵 Price: <b style="color:#2ecc71">₹{price}/t</b> · Net: <b style="color:#d4a843">₹{net_p}/t</b></p>
        </div>""", unsafe_allow_html=True)

    df_p = pd.DataFrame({"name":["Sangrur","Ludhiana","Karnal","Patiala","Amritsar"],
                          "km":[62,38,120,78,45],"price":[2400,2350,2500,2420,2280],"cap":[200,150,300,250,100]})
    fig_sc = go.Figure(go.Scatter(x=df_p.km, y=df_p.price, mode="markers+text", text=df_p.name,
        textposition="top center", textfont=dict(color="#8fa8c8",size=10),
        marker=dict(size=df_p.cap/10, color=df_p.price, colorscale="YlGn", showscale=True,
                    colorbar=dict(title="₹/tonne",thickness=10))))
    fig_sc.update_layout(title="Price vs. Distance from Field", paper_bgcolor="#0d1424", plot_bgcolor="#0d1424",
        font_color="#8fa8c8", height=250, margin=dict(l=0,r=0,t=40,b=0),
        xaxis=dict(title="Distance (km)",gridcolor="#1e3352"), yaxis=dict(title="Price (₹/tonne)",gridcolor="#1e3352"))
    st.plotly_chart(fig_sc, use_container_width=True)

# ── PAYMENT FLOW ──────────────────────────────────────────────────────────────
st.markdown('<div class="section">🏦 PM-Kisan Direct Payment Flow</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    steps = [
        ("Farmer accepts via VoicERA call",          "~0 min",      "#f5a623"),
        ("Nearest Bio-CNG plant confirmed",           "~2 min",      "#f5a623"),
        ("Truck dispatched to field",                 "~30 min",     "#8fa8c8"),
        ("Stubble collected & weighed at plant gate", "~4–8 hours",  "#8fa8c8"),
        ("Payment via PM-Kisan DBT API initiated",   "~24 hours",   "#2ecc71"),
        ("Amount credited to farmer's bank",          "~24–48 hours","#2ecc71"),
    ]
    for i, (step, time_str, color) in enumerate(steps):
        st.markdown(f"""
        <div style="display:flex;gap:12px;align-items:center;margin-bottom:8px">
            <div style="background:{color}22;border:2px solid {color};border-radius:50%;
                        width:28px;height:28px;flex-shrink:0;display:flex;align-items:center;
                        justify-content:center;font-size:0.78rem;font-weight:700;color:{color}">{i+1}</div>
            <div style="flex:1;background:#111b2e;border:1px solid #1e3352;border-radius:8px;padding:8px 12px">
                <div style="font-size:0.83rem;color:#e8eef8">{step}</div>
                <div style="font-size:0.7rem;color:#4a6080;margin-top:2px">⏱ {time_str}</div>
            </div>
        </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("**📈 Punjab-wide Impact at Different Diversion Rates**")
    pct_range = list(range(5, 61, 5))
    total_ha  = 2_900_000
    farmer_income = [p/100 * total_ha * stubble_yield * (base_price-transport_cost)/1e7 for p in pct_range]
    co2_saved_mt  = [p/100 * total_ha * stubble_yield * 1.4/1e6 for p in pct_range]

    fig_scale = go.Figure()
    fig_scale.add_trace(go.Scatter(x=pct_range, y=farmer_income, name="Farmer income (₹ Cr)",
        line=dict(color="#2ecc71",width=2.5), yaxis="y1"))
    fig_scale.add_trace(go.Scatter(x=pct_range, y=co2_saved_mt, name="CO₂ avoided (M t)",
        line=dict(color="#8fa8c8",width=2,dash="dot"), yaxis="y2"))
    fig_scale.update_layout(
        title="Punjab-wide Impact vs. Diversion Rate",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=300, margin=dict(l=0,r=0,t=40,b=0),
        xaxis=dict(title="Diversion Rate (%)",gridcolor="#1e3352",ticksuffix="%"),
        yaxis=dict(title="Farmer Income (₹ Crore)",titlefont=dict(color="#2ecc71"),gridcolor="#1e3352"),
        yaxis2=dict(title="CO₂ Avoided (M t)",overlaying="y",side="right",titlefont=dict(color="#8fa8c8")),
        legend=dict(bgcolor="#111b2e",bordercolor="#1e3352",borderwidth=1)
    )
    st.plotly_chart(fig_scale, use_container_width=True)

    st.markdown("""
    <div style="background:#0d1a0d;border:1px solid #1a5c1a;border-radius:10px;padding:14px">
        <div style="color:#2ecc71;font-weight:700;font-size:0.88rem;margin-bottom:8px">💡 At 30% diversion rate:</div>
        <div style="color:#8fa8c8;font-size:0.82rem;line-height:1.8">
        • Farmer income: <b style="color:#2ecc71">~₹3,800 Crore</b><br>
        • CO₂ avoided: <b style="color:#2ecc71">~5.4 M tonnes</b><br>
        • Delhi AQI reduction: <b style="color:#2ecc71">~45 µg/m³</b><br>
        • Bio-CNG produced: <b style="color:#2ecc71">~12 Lakh MMBTU</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
