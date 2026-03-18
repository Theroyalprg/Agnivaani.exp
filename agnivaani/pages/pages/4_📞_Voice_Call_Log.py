import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Voice Call Log — Agnivāṇī", page_icon="📞", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Noto+Sans+Gurmukhi:wght@400;600&display=swap');
*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.section { font-size:1.1rem; font-weight:700; color:#e8eef8;
    border-left:3px solid #2ecc71; padding-left:10px; margin:1.5rem 0 0.8rem 0; }
.stat { background:#111b2e; border:1px solid #1e3352; border-radius:8px; padding:0.9rem; text-align:center; }
.stat-val { font-size:1.7rem; font-weight:700; }
.stat-lbl { font-size:0.68rem; color:#8fa8c8; text-transform:uppercase; letter-spacing:1px; margin-top:3px; }
.punjabi { font-family:'Noto Sans Gurmukhi',sans-serif; color:#2ecc71; font-size:0.9rem; font-weight:600; }
.tech-box { background:#111b2e; border:1px solid #1e3352; border-radius:10px; padding:1rem 1.2rem; }
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
    st.markdown("**📊 Model Stats**")
    st.metric("AWWER Score", "91.3%", "+2.1%")
    st.metric("Punjabi Accuracy", "94.7%", "+0.8%")
    st.metric("Avg Call Duration", "2m 18s", "-12s")
    st.divider()
    st.caption("Model: VoicERA · Bhashini AWWER · Agriculture-tuned")

# ── CALL DATA ─────────────────────────────────────────────────────────────────
CALLS = [
    {
        "id":"C-0041", "type":"fire", "call_type":"Fire Detected (Dynamic)",
        "farmer":"Gurmeet Singh", "village":"Lohian Khas", "district":"Moga",
        "time":"23:33 IST", "duration":"3m 12s", "outcome":"Accepted", "outcome_color":"#2ecc71",
        "sri":87, "offer":"₹3,100/tonne (dynamic buyback)", "stubble":"5.6 t", "revenue":"₹17,360",
        "punjabi":"ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਵੀਰ ਜੀ। ਸਾਡੇ ਸੈਟੇਲਾਈਟ ਨੇ ਤੁਹਾਡੇ ਖੇਤ ਵਿੱਚ ਅੱਗ ਦੇਖੀ ਹੈ।",
        "transcript":[
            ("AGENT",  "Sat Sri Akal, Veer ji. Our Sentinel satellite has detected a small fire on your field in Lohian Khas. It's still small — there's time to act."),
            ("FARMER", "Haan ji... main hi lagayi si thodi. Kehra satellite?"),
            ("AGENT",  "Veer ji, if you douse it now, the Sangrur Bio-CNG plant will take the unburnt 90% at ₹3,100/tonne — that's ₹17,360 for your field, in your PM-Kisan account within 24 hours."),
            ("FARMER", "Paani naal bujhana padega? Truck kado aayega?"),
            ("AGENT",  "Ji. I'm booking the truck for 6:00 AM tomorrow. Please douse with the irrigation channel water. I'm sending the driver's number by SMS now."),
            ("FARMER", "Theek hai veer ji. Bujhaunga."),
        ]
    },
    {
        "id":"C-0039", "type":"preempt", "call_type":"Pre-emptive",
        "farmer":"Balwinder Kaur", "village":"Sahnewal", "district":"Ludhiana",
        "time":"22:15 IST", "duration":"2m 44s", "outcome":"Callback Requested", "outcome_color":"#f5a623",
        "sri":72, "offer":"₹2,400/tonne (base price)", "stubble":"—", "revenue":"—",
        "punjabi":"ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਬੀਬੀ ਜੀ। ਤੁਹਾਡਾ ਖੇਤ ਅੱਜ ਵੱਢਿਆ ਗਿਆ ਹੈ।",
        "transcript":[
            ("AGENT",  "Sat Sri Akal, Bibi ji. Satellite shows your 4.8 ha field in Sahnewal was harvested today. Wind is heading toward Delhi — if burned, smoke arrives in ~8 hours."),
            ("FARMER", "Main jaandi haan. Par mere kol abhi time nahi. Kal gal kariye."),
            ("AGENT",  "Ji zaroor. I'll call at 7:00 AM. The ₹2,400/tonne offer is valid for 48 hours — ₹40,320 for your field."),
            ("FARMER", "Theek hai. Kal subah phone karo."),
        ]
    },
    {
        "id":"C-0038", "type":"fire", "call_type":"Fire Detected (Dynamic)",
        "farmer":"Baljinder Mann", "village":"Khanna", "district":"Ludhiana",
        "time":"23:10 IST", "duration":"1m 55s", "outcome":"Refused", "outcome_color":"#7a8fa8",
        "sri":82, "offer":"₹3,100/tonne (dynamic buyback)", "stubble":"—", "revenue":"—",
        "punjabi":"ਵੀਰ ਜੀ, ਅਸੀਂ ਤੁਹਾਡੇ ਖੇਤ ਵਿੱਚ ਅੱਗ ਦੇਖੀ ਹੈ।",
        "transcript":[
            ("AGENT",  "Veer ji, fire detected on your 7.1 ha field in Khanna. Dynamic buyback is ₹3,100/tonne — over ₹61,000 if you douse it now."),
            ("FARMER", "Yaar, sab laga ditti. Aadha jal gaya. Baaki rakha nahi jaata hune."),
            ("AGENT",  "Even 50% remaining is worth ₹30,000. I can send a truck in 2 hours."),
            ("FARMER", "Nahi yaar. Agli bar shayad. Hune nahi hona."),
            ("AGENT",  "Ji, samajh aata hai. I'm registering your field for early monitoring next season."),
        ]
    },
    {
        "id":"C-0035", "type":"preempt", "call_type":"Pre-emptive",
        "farmer":"Daljeet Sandhu", "village":"Dhuri", "district":"Sangrur",
        "time":"18:30 IST", "duration":"4m 02s", "outcome":"Accepted", "outcome_color":"#2ecc71",
        "sri":55, "offer":"₹2,400/tonne (base price)", "stubble":"12.75 t", "revenue":"₹30,600 (net)",
        "punjabi":"ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਵੀਰ ਜੀ। ਤੁਹਾਡਾ ਖੇਤ ਕੱਲ੍ਹ ਵੱਢਿਆ ਜਾਵੇਗਾ।",
        "transcript":[
            ("AGENT",  "Sat Sri Akal, Veer ji. AMED data shows your 5.1 ha field in Dhuri harvests tomorrow. Residue burned → smoke reaches Delhi."),
            ("FARMER", "Haan, combine aa rahi hai kal. Main soch raha si ki agg laga daan. Koi faida nahi lagda truckon da."),
            ("AGENT",  "Veer ji, we handle the truck. Just say yes. Sangrur Bioenergy buys at ₹2,400/tonne. Your 12.75t = ₹30,600 net to PM-Kisan account."),
            ("FARMER", "Sach mein? PM-Kisan account mein?"),
            ("AGENT",  "Ji bilkul. Truck at 6 AM. Driver's number by SMS."),
            ("FARMER", "Theek hai bhai. Kar lo booking."),
            ("AGENT",  "Booking confirmed! Truck PB-10-AB-3421. Driver: Sukhjinder. Press 1 to call back."),
        ]
    },
    {
        "id":"C-0031", "type":"confirm", "call_type":"Booking Confirmation",
        "farmer":"Manpreet Dhaliwal", "village":"Rampura Phul", "district":"Bathinda",
        "time":"07:15 IST", "duration":"1m 10s", "outcome":"Accepted", "outcome_color":"#2ecc71",
        "sri":0, "offer":"Delivery confirmation", "stubble":"18.25 t delivered", "revenue":"₹43,800 — CREDITED",
        "punjabi":"ਵੀਰ ਜੀ, ਤੁਹਾਡਾ ਭੁਗਤਾਨ ਭੇਜਿਆ ਜਾ ਰਿਹਾ ਹੈ।",
        "transcript":[
            ("AGENT",  "Sat Sri Akal, Veer ji. Your 18.25 tonnes has been received at Sangrur Bioenergy. ₹43,800 is being credited to your PM-Kisan account ending 4782."),
            ("FARMER", "Wah! Itna jaldi! Shukriya bhai."),
            ("AGENT",  "Agle saal bhi aapka khet registered hai. Good season, Veer ji."),
        ]
    },
]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("## 📞 Bhashini VoicERA — Call Log")
st.caption("Autonomous multilingual voice agent · AWWER-optimised Punjabi · Agriculture-weighted models")

# ── STATS ─────────────────────────────────────────────────────────────────────
cols = st.columns(5)
stats = [
    (len(CALLS),                                        "Total Calls Today", "#e8eef8"),
    (sum(1 for c in CALLS if c["outcome"]=="Accepted"), "Accepted",          "#2ecc71"),
    (sum(1 for c in CALLS if c["outcome"]=="Refused"),  "Refused",           "#7a8fa8"),
    ("91.3%",                                           "Punjabi AWWER",     "#f5a623"),
    ("2m 18s",                                          "Avg Duration",      "#8fa8c8"),
]
for col, (val, lbl, color) in zip(cols, stats):
    col.markdown(f'<div class="stat"><div class="stat-val" style="color:{color}">{val}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.divider()

# ── CALLS + ANALYTICS ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="section">📋 Call Transcripts</div>', unsafe_allow_html=True)

    type_icon = {"fire":"🔥","preempt":"🌾","confirm":"✅"}
    type_color = {"fire":"#ff4e1a","preempt":"#f5a623","confirm":"#2ecc71"}

    for call in CALLS:
        tc = type_color.get(call["type"], "#8fa8c8")
        with st.expander(f"📞 {call['id']} — {call['farmer']} ({call['village']}) · {call['time']}"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Type:** <span style='color:{tc}'>{call['call_type']}</span>", unsafe_allow_html=True)
            c2.markdown(f"**Duration:** {call['duration']}")
            c3.markdown(f"**Outcome:** <span style='color:{call['outcome_color']};font-weight:700'>{call['outcome']}</span>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:rgba(7,11,20,0.5);border-radius:8px;padding:10px 14px;
                        margin:8px 0;border-left:3px solid {tc}">
                <div style="font-size:0.68rem;color:#4a6080;margin-bottom:4px">OPENING LINE (Punjabi)</div>
                <div class="punjabi">{call['punjabi']}</div>
                <div style="font-size:0.8rem;color:#8fa8c8;margin-top:6px">
                    <b>Offer:</b> {call['offer']} · <b>SRI:</b> {call['sri']}
                    {f"<br><b>Saved:</b> {call['stubble']} · <b style='color:#2ecc71'>Revenue: {call['revenue']}</b>" if call['outcome']=='Accepted' and call['stubble']!='—' else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Transcript:**")
            for speaker, line in call["transcript"]:
                color = "#f5a623" if speaker == "AGENT" else "#e8eef8"
                label = "🤖 Agent (VoicERA)" if speaker == "AGENT" else "👨‍🌾 Farmer"
                bg    = "rgba(245,166,35,0.05)" if speaker == "AGENT" else "rgba(232,238,248,0.03)"
                bord  = "#f5a62355" if speaker == "AGENT" else "#4a608055"
                st.markdown(f"""
                <div style="margin-bottom:5px;padding:7px 12px;border-radius:6px;
                            background:{bg};border-left:2px solid {bord}">
                    <div style="font-size:0.65rem;color:{color};text-transform:uppercase;
                                letter-spacing:1px;margin-bottom:2px">{label}</div>
                    <div style="font-size:0.83rem;color:{color}">{line}</div>
                </div>""", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section">📊 Analytics</div>', unsafe_allow_html=True)

    # Funnel
    fig_funnel = go.Figure(go.Funnel(
        y=["Fields Harvested","AMED Flagged","Calls Triggered","Calls Answered","Accepted Offer"],
        x=[142,89,52,31,28],
        textinfo="value+percent initial",
        marker_color=["#1e3352","#2a4a72","#f5a623","#d4a843","#2ecc71"],
        textfont=dict(color="#e8eef8")
    ))
    fig_funnel.update_layout(title="Today's Conversion Funnel", paper_bgcolor="#0d1424",
        plot_bgcolor="#0d1424", font_color="#8fa8c8", height=280, margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig_funnel, use_container_width=True)

    # Outcomes by hour
    hours = list(range(17, 24))
    fig_hour = go.Figure()
    fig_hour.add_trace(go.Bar(x=hours, y=[2,3,5,4,6,3,5], name="Accepted", marker_color="#2ecc71"))
    fig_hour.add_trace(go.Bar(x=hours, y=[1,1,2,3,1,2,1], name="Refused",  marker_color="#7a8fa8"))
    fig_hour.add_trace(go.Bar(x=hours, y=[3,2,1,2,2,1,2], name="No Answer",marker_color="#1e3352"))
    fig_hour.update_layout(barmode="stack", title="Call Outcomes by Hour (IST)",
        paper_bgcolor="#0d1424", plot_bgcolor="#0d1424", font_color="#8fa8c8",
        height=230, margin=dict(l=0,r=0,t=40,b=0),
        yaxis=dict(gridcolor="#1e3352"),
        xaxis=dict(title="Hour (IST)",gridcolor="#1e3352",tickvals=hours,ticktext=[f"{h}:00" for h in hours]),
        legend=dict(bgcolor="#111b2e",bordercolor="#1e3352",borderwidth=1))
    st.plotly_chart(fig_hour, use_container_width=True)

    # Tech info
    st.markdown('<div class="section" style="font-size:1rem">🗣️ VoicERA Technology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-box">
        <div style="color:#8fa8c8;font-size:0.82rem;line-height:1.9">
        <b style="color:#2ecc71">Bhashini:</b> India's national AI translation platform by MeitY. Real-time ASR, TTS, NMT across 22 scheduled languages.<br>
        <b style="color:#2ecc71">VoicERA Stack:</b> Whisper-based ASR → LLM reasoning → Indic TTS. 2G/3G compatible for rural networks.<br>
        <b style="color:#2ecc71">AWWER Metric:</b> Agriculture Weighted Word Error Rate. Custom vocabulary for Punjabi crop terms, village names, market prices.<br>
        <b style="color:#2ecc71">Noise robustness:</b> Tested at 15dB+ ambient noise (tractor, combine harvester). Fine-tuned on 2,400+ hours of field audio.
        </div>
    </div>
    """, unsafe_allow_html=True)
