# Aadhaar N.E.X.U.S

**National Equity eXecution & Utilization System**

> A data-driven planning and early-warning system that measures digital equity, anticipates Aadhaar demand, and simulates where UIDAI should act first.

## Overview

Aadhaar N.E.X.U.S is an interactive Streamlit dashboard that provides **nationwide visibility** into the Digital Equity Index (DEI) across **36 states/UTs** and **645+ districts**.

🌐 Live Dashboard:
👉 https://aadhaar-nexus.streamlit.app/

## Key Features

- **State to District Drill-down**: Select any state/UT to see district-level performance
- **Real-time KPIs**: View DEI, Access Health, Update Load, and Stability scores
- **Risk Classification**: Automatic categorization into Healthy, Access Stress, Update Burden, Stability Risk
- **Smart Recommendations**: AI-generated suggestions for each district
- **Export Reports**: Download detailed district reports as text files
- **Dark Mode Support**: Full compatibility with Streamlit's dark theme

## Metrics Explained

| Metric | Description | Direction |
|--------|-------------|-----------|
| **DEI** (Digital Equity Index) | Overall composite score | Higher is better |
| **Access Health Score** | Enrollment infrastructure accessibility | Higher is better |
| **Update Load Score** | Biometric/demographic update burden | Lower is better |
| **Stability Score** | Service delivery consistency | Lower is better |

## Coverage

| Zone | States/UTs | Districts |
|------|------------|-----------|
| South | 7 | 148 |
| West | 5 | 115 |
| East | 10 | 188 |
| North | 9 | 188 |
| **Total** | **36** | **645** |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Project Structure

```
uidai_dashboard/
  app.py                    # Main Streamlit application
  requirements.txt          # Python dependencies
  README.md                 # This file
  data/
    district_equity_all_india.csv  # Consolidated DEI data
```

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Styling**: Native Streamlit components (Dark Mode compatible)

## Deployment

This app is ready for deployment on:
- **Streamlit Cloud**: Push to GitHub, connect to Streamlit Cloud
- **Vercel**: See deployment guide in DEPLOY.md
- **Heroku**: Use Procfile with `streamlit run app.py`

## License

Developed for UIDAI Hackathon 2026
