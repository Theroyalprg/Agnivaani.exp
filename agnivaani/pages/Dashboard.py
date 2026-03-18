import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Dashboard — Agnivāṇī", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');
*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.kpi { background: #111b2e; border: 1px solid #1e3352; border-radius: 10px; padding: 1rem; text-align: center; }
.kpi-val { font-size: 1.8rem; font-weight: 700; }
.kpi-lbl { font-size: 0.68rem; color: #8fa8c8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.section { font-size: 1.1rem; font-weight: 700; color: #e8eef8;
    border-left: 3px solid #f5a623; padding-left: 10px; margin: 1.5rem 0 0.8rem 0; }

.field-row { border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; border-left: 3px solid; }

.alert-box { background:rgba(46,204,113,0.08); border:1px solid #2ecc71;
    border-radius:8px; padding:10px 14px; margin-bottom:6px; font-size:0.83rem; color:#2ecc71; }

.msg-preview { background:#0a1a0a; border:1px solid #1a5c1a; border-radius:10px;
    padding:14px 16px; font-size:0.83rem; color:#a8d8a8; line-height:1.9; font-family:monospace; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔥 Agnivāṇī")
    st.divider()
    st.markdown("🏠 [Home](/)")
    st.markdown("📊 [Dashboard](/Dashboard)")
    st.markdown("🌬️ [Smoke Trajectory](/Smoke_Trajectory)")
    st.markdown("💰 [Biomass Economics](/Biomass_Economics)")
    st.markdown("📞 [Voice Call Log](/Voice_Call_Log)")
    st.divider()
    st.markdown("**⚙️ Controls**")
    auto_refresh = st.toggle("Auto-refresh (10s)", value=False)
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()
    st.divider()
    st.caption("Live Data: Sentinel-3 SLSTR NRT · Google AMED API")
# ── FIELD DATA ────────────────────────────────────────────────────────────────
FIELDS = [
    {"id":"F001","farmer":"Gurmeet Singh",    "village":"Lohian Khas",  "district":"Moga",           "area_ha":6.2, "status":"BURNING",   "sri":87, "lat":30.82,"lon":75.17,"phone":"+919876543210"},
    {"id":"F002","farmer":"Balwinder Kaur",   "village":"Sahnewal",     "district":"Ludhiana",       "area_ha":4.8, "status":"HARVESTED", "sri":72, "lat":30.90,"lon":75.83,"phone":"+919876543211"},
    {"id":"F003","farmer":"Sukhdev Rana",     "village":"Rajpura",      "district":"Patiala",        "area_ha":3.1, "status":"HARVESTED", "sri":58, "lat":30.48,"lon":76.59,"phone":"+919876543212"},
    {"id":"F004","farmer":"Harpreet Gill",    "village":"Tarn Taran",   "district":"Amritsar",       "area_ha":8.4, "status":"MONITORING","sri":43, "lat":31.45,"lon":74.93,"phone":"+919876543213"},
    {"id":"F005","farmer":"Ranjit Kumar",     "village":"Sirhind",      "district":"Fatehgarh Sahib","area_ha":2.7, "status":"BURNING",   "sri":79, "lat":30.64,"lon":76.38,"phone":"+919876543214"},
    {"id":"F006","farmer":"Daljeet Sandhu",   "village":"Dhuri",        "district":"Sangrur",        "area_ha":5.1, "status":"BOOKED",    "sri":0,  "lat":30.05,"lon":75.87,"phone":"+919876543215"},
    {"id":"F007","farmer":"Manpreet Dhaliwal","village":"Rampura Phul", "district":"Bathinda",       "area_ha":7.3, "status":"DELIVERED", "sri":0,  "lat":30.27,"lon":75.22,"phone":"+919876543216"},
    {"id":"F008","farmer":"Jagtar Singh",     "village":"Zira",         "district":"Ferozepur",      "area_ha":4.0, "status":"HARVESTED", "sri":61, "lat":30.96,"lon":74.99,"phone":"+919876543217"},
    {"id":"F009","farmer":"Kirpal Brar",      "village":"Phagwara",     "district":"Kapurthala",     "area_ha":6.6, "status":"MONITORING","sri":38, "lat":31.22,"lon":75.77,"phone":"+919876543218"},
    {"id":"F010","farmer":"Amarjit Dhillon",  "village":"Barnala",      "district":"Sangrur",        "area_ha":5.5, "status":"HARVESTED", "sri":65, "lat":30.38,"lon":75.54,"phone":"+919876543219"},
    {"id":"F011","farmer":"Surjit Kaur",      "village":"Malerkotla",   "district":"Sangrur",        "area_ha":3.8, "status":"BOOKED",    "sri":0,  "lat":30.53,"lon":75.88,"phone":"+919876543220"},
    {"id":"F012","farmer":"Baljinder Mann",   "village":"Khanna",       "district":"Ludhiana",       "area_ha":7.1, "status":"BURNING",   "sri":82, "lat":30.71,"lon":76.22,"phone":"+919876543221"},
]
df = pd.DataFrame(FIELDS)

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("## 📊 Live Field Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %H:%M:%S IST')}")

# ── KPIs ─────────────────────────────────────────────────────────────────────
cols = st.columns(6)
kpis = [
    (len(df),                                              "Fields Monitored", "#e8eef8"),
    (len(df[df.status=="BURNING"]),                        "Active Burns",     "#ff4e1a"),
    (len(df[df.status=="HARVESTED"]),                      "Harvested",        "#f5a623"),
    (len(df[df.status=="BOOKED"]),                         "Trucks Booked",    "#2ecc71"),
    (len(df[df.status=="DELIVERED"]),                      "Delivered",        "#d4a843"),
    (f"₹{sum(r.area_ha*2.5*2400 for _,r in df[df.status.isin(['BOOKED','DELIVERED'])].iterrows())/100000:.1f}L",
                                                           "Revenue Generated","#2ecc71"),
]
for col, (val, lbl, color) in zip(cols, kpis):
    col.markdown(f'<div class="kpi"><div class="kpi-val" style="color:{color}">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.divider()

# ── MAP + ALERTS ─────────────────────────────────────────────────────────────
left, right = st.columns([1.5, 1])

with left:
    st.markdown('<div class="section">🗺️ Field Map</div>', unsafe_allow_html=True)
    status_color = {"BURNING":"#ff4e1a","HARVESTED":"#f5a623","MONITORING":"#7a8fa8","BOOKED":"#2ecc71","DELIVERED":"#1a7a42"}
    status_icon  = {"BURNING":"🔥","HARVESTED":"🌾","MONITORING":"🛰️","BOOKED":"🚛","DELIVERED":"✅"}

    fig = go.Figure()
    for status in df.status.unique():
        sub = df[df.status == status]
        fig.add_trace(go.Scattermapbox(
            lat=sub.lat, lon=sub.lon, mode="markers+text",
            marker=dict(size=12 if status=="BURNING" else 9, color=status_color[status]),
            text=[f"{status_icon[status]} {r.farmer}" for _,r in sub.iterrows()],
            textposition="top right", textfont=dict(color=status_color[status], size=10),
            name=f"{status_icon[status]} {status}",
            hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
            customdata=[f"{r.village}, {r.district} | {r.area_ha}ha | SRI:{r.sri}" for _,r in sub.iterrows()]
        ))
    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=30.6, lon=75.7), zoom=6.8),
        paper_bgcolor="#0d1424", font_color="#8fa8c8",
        height=460, margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(bgcolor="#111b2e", bordercolor="#1e3352", borderwidth=1, orientation="h", y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown('<div class="section">🚨 Critical Fields — Action Required</div>', unsafe_allow_html=True)

    critical = df[df.status.isin(["BURNING","HARVESTED"])].sort_values("sri", ascending=False)

    for _, f in critical.iterrows():
        color = "#ff4e1a" if f.status == "BURNING" else "#f5a623"
        icon  = "🔥" if f.status == "BURNING" else "🌾"
        stubble = round(f.area_ha * 3.5 * 0.9, 1)
        revenue = int(stubble * (3100 if f.status=="BURNING" else 2400) - stubble * 420)
        already_sent = any(log["field_id"] == f["id"] for log in st.session_state.alert_log)

        with st.expander(f"{icon} {f['farmer']} — {f['village']}, {f['district']} (SRI {f['sri']})"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Status", f.status)
            c2.metric("Area", f"{f['area_ha']} ha")
            c3.metric("Est. Revenue", f"₹{revenue:,}")

            # WhatsApp message preview
            price = 3100 if f.status == "BURNING" else 2400
            msg = f"""🔥 *Agnivāṇī Alert*

Sat Sri Akal *{f['farmer']}* ji.

{"Sentinel satellite has detected a fire on your field." if f.status=="BURNING" else "Your field was recently harvested."}
📍 {f['village']}, {f['district']}
📊 Smoke Risk Index: *{f['sri']}/100*

💰 *Offer:* ₹{price}/tonne ({'dynamic buyback' if f.status=='BURNING' else 'base price'})
🌾 Your {stubble}t stubble = *₹{revenue:,}* (net)
💳 Payment to PM-Kisan account within 24h

Reply YES to book truck for 6 AM tomorrow.
— Agnivāṇī Agent"""

            st.code(msg, language=None)

            if already_sent:
                st.success("✅ Alert already sent this session")
            else:
                if st.button(f"📱 Send WhatsApp Alert to {f['farmer']}", key=f"btn_{f['id']}", type="primary", use_container_width=True):
                    # Log the alert (in production this would call Bhashini/WhatsApp API)
                    st.session_state.alert_log.append({
                        "field_id": f["id"], "farmer": f["farmer"],
                        "village": f["village"], "sri": f["sri"],
                        "revenue": revenue, "time": datetime.now().strftime("%H:%M:%S"),
                        "phone": f["phone"]
                    })
                    st.success(f"✅ Alert queued for {f['farmer']} ({f['phone']})")
                    st.info("ℹ️ In production: Bhashini VoicERA call + WhatsApp message triggered via API")
                    st.rerun()

    st.divider()

    # Bulk send
    unsent = [f for _,f in critical.iterrows() if not any(l["field_id"]==f["id"] for l in st.session_state.alert_log)]
    if unsent:
        if st.button(f"🚨 Send All {len(unsent)} Alerts Now", type="primary", use_container_width=True):
            for f in unsent:
                stubble = round(f.area_ha * 3.5 * 0.9, 1)
                revenue = int(stubble * (3100 if f.status=="BURNING" else 2400) - stubble * 420)
                st.session_state.alert_log.append({
                    "field_id": f["id"], "farmer": f["farmer"],
                    "village": f["village"], "sri": f["sri"],
                    "revenue": revenue, "time": datetime.now().strftime("%H:%M:%S"),
                    "phone": f["phone"]
                })
            st.success(f"✅ {len(unsent)} alerts queued!")
            st.rerun()

    # Alert log
    if st.session_state.alert_log:
        st.markdown('<div class="section" style="font-size:1rem">📋 Alert Log</div>', unsafe_allow_html=True)
        for log in reversed(st.session_state.alert_log):
            st.markdown(f"""
            <div class="alert-box">
                ✅ <b>{log['farmer']}</b> · {log['village']} · SRI {log['sri']}<br>
                <span style="font-size:0.72rem;opacity:0.7">{log['phone']} · Est. ₹{log['revenue']:,} · {log['time']}</span>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️ Clear Log", use_container_width=True):
            st.session_state.alert_log = []
            st.rerun()

# ── BOTTOM: FIELD TABLE + TIMESERIES ─────────────────────────────────────────
st.divider()
left_b, right_b = st.columns([0.55, 1.45])

with left_b:
    st.markdown('<div class="section">📋 All Fields</div>', unsafe_allow_html=True)
    sc = {"BURNING":("#ff4e1a","rgba(255,78,26,0.1)"), "HARVESTED":("#f5a623","rgba(245,166,35,0.08)"),
          "MONITORING":("#7a8fa8","rgba(122,143,168,0.06)"), "BOOKED":("#2ecc71","rgba(46,204,113,0.08)"),
          "DELIVERED":("#1a7a42","rgba(26,122,66,0.08)")}
    icons = {"BURNING":"🔥","HARVESTED":"🌾","MONITORING":"🛰️","BOOKED":"🚛","DELIVERED":"✅"}
    for _, row in df.iterrows():
        c, bg = sc[row["status"]]
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {c}33;border-radius:8px;
                    padding:8px 12px;margin-bottom:5px;border-left:3px solid {c}">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:0.82rem;font-weight:700;color:#e8eef8">{row['farmer']}</span>
                <span style="background:{c}22;color:{c};font-size:0.62rem;font-weight:700;
                             padding:2px 8px;border-radius:8px">{icons[row['status']]} {row['status']}</span>
            </div>
            <div style="font-size:0.72rem;color:#8fa8c8;margin-top:2px">
                {row['village']}, {row['district']} · {row['area_ha']}ha · SRI: {row['sri']}
            </div>
        </div>""", unsafe_allow_html=True)

with right_b:
    st.markdown('<div class="section">📈 Fire Detections — Last 24 Hours</div>', unsafe_allow_html=True)
    hours_ts = [(datetime.now() - timedelta(hours=23-i)) for i in range(24)]
    np.random.seed(42)
    detections = np.clip(np.random.poisson(3,24) + np.array([0]*12+[2,4,6,5,4,3,2,1,1,1,1,0]), 0, 15)
    aqi_vals   = 180 + np.cumsum(np.random.randn(24)*5) + detections*8
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=hours_ts, y=detections, name="Fire Detections",
        line=dict(color="#ff4e1a", width=2.5), fill="tozeroy", fillcolor="rgba(255,78,26,0.1)", yaxis="y1"))
    fig_ts.add_trace(go.Scatter(x=hours_ts, y=aqi_vals, name="Delhi AQI (est.)",
        line=dict(color="#8fa8c8", width=1.5, dash="dot"), yaxis="y2"))
    fig_ts.add_hline(y=4, line_dash="dash", line_color="#f5a623", opacity=0.5,
        annotation_text="Alert threshold", annotation_font=dict(color="#f5a623", size=10))
    fig_ts.update_layout(
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=320, margin=dict(l=0,r=0,t=10,b=0),
        yaxis=dict(title="Fire Count", gridcolor="#1e3352"),
        yaxis2=dict(title="AQI", overlaying="y", side="right"),
        legend=dict(bgcolor="#111b2e", bordercolor="#1e3352", borderwidth=1, orientation="h", y=1.02),
        xaxis=dict(gridcolor="#1e3352"),
    )
    st.plotly_chart(fig_ts, use_container_width=True)

if auto_refresh:
    time.sleep(10)
    st.rerun()
