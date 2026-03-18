# 🔥 Agnivāṇī — Nocturnal Biomass-Arbitrage & Smoke-Trajectory Agent

A clean, user-friendly Streamlit dashboard for the Agnivāṇī climate-tech solution targeting stubble burning in the northwestern Indian agricultural belt.

## 📄 Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Problem overview, how it works, tech stack, impact projections |
| 📊 Dashboard | Live field monitor with map, burn alerts, direct alert sending |
| 🌬️ Smoke Trajectory | NeuralGCM wind model, configurable trajectory, AQI forecasting |
| 💰 Biomass Economics | Arbitrage calculator, plant network, PM-Kisan payment flow |
| 📞 Voice Call Log | Bhashini VoicERA transcripts, funnel analytics, AWWER stats |

## 🏗️ Project Structure

```
agnivaani/
├── Home.py                           # Main page — concept & overview
├── pages/
│   ├── 1_📊_Dashboard.py            # Field monitoring dashboard
│   ├── 2_🌬️_Smoke_Trajectory.py     # NeuralGCM wind model
│   ├── 3_💰_Biomass_Economics.py    # Arbitrage engine & calculator
│   └── 4_📞_Voice_Call_Log.py       # Bhashini VoicERA log
├── .streamlit/
│   └── config.toml                   # Dark theme config
├── requirements.txt
└── README.md
```

## 🛰️ Data Sources (Production)

| Component | API / Source | Cost |
|-----------|-------------|------|
| Field monitoring | Google AMED API | Free |
| Fire detection | Copernicus Sentinel-3 SLSTR NRT | Free |
| Wind/smoke model | Google NeuralGCM (open-source) | Free |
| Voice AI | MeitY Bhashini + VoicERA | Free |
| Payment | PM-Kisan DBT API | Free |

> **Note:** This prototype uses simulated data. In production, connect each module to its respective API.
