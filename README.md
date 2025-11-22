# 🌾 Agricultural Drought Early Warning System - Mekong Delta

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A cutting-edge AI-powered platform for real-time agricultural drought monitoring and early warning in the Mekong Delta region, leveraging satellite remote sensing and machine learning technologies.

## 🎯 Revolutionizing Drought Monitoring

In the heart of Vietnam's rice basket, where climate change poses significant threats to food security, our system stands as a technological shield. By harnessing the power of satellite data and artificial intelligence, we deliver precise, real-time drought predictions that empower farmers and policymakers with actionable insights.

### 🚀 Breakthrough Capabilities

- 🌐 Multi-Source Satellite Fusion: Integrates MODIS, CHIRPS, and ERA5 data streams for comprehensive environmental monitoring
- 🧠 Advanced AI Ensemble: XGBoost model achieving 87.5% prediction accuracy in multi-class drought classification
- ⚡ Real-Time Intelligence: Live dashboard processing current vegetation health and precipitation patterns
- 🎯 5-Level Precision Classification: Sophisticated balanced system distinguishing No Drought, Light, Moderate, Severe, and Extreme drought conditions
- 📊 Interactive Analytics: Dynamic visualizations revealing hidden patterns in environmental data

## 📊 Data Ecosystem

Orbital Intelligence Network:
- 🛰️ MODIS Terra/Aqua: High-resolution vegetation indices (NDVI) tracking crop health
- 🌧️ CHIRPS: Climate Hazards Group InfraRed Precipitation for rainfall monitoring
- 🌡️ ERA5: European Centre atmospheric reanalysis for temperature profiling

Coverage: 120 months of continuous Earth observation (2015-2024)  
Region: Mekong Delta, Vietnam - Critical agricultural zone  
Feature Engineering: 19 advanced metrics including temporal lags, rolling aggregates, and anomaly detection

## 🚀 Quick Deployment

### System Requirements
```bash
Python 3.8+ | 4GB RAM | Stable internet connection
```

### Instant Setup
```bash
# Clone the intelligence platform
git clone https://github.com/quyforest/mekong-drought-ai.git
cd mekong-drought-ai

# Install AI dependencies
pip install -r requirements.txt

# Launch the command center
streamlit run app.py
```

Access your personal drought monitoring dashboard at `http://localhost:8501`

## 🏗️ Architectural Excellence

```
mekong-drought-ai/
├── app.py                          # AI Command Center
├── models/
│   ├── xgboost_drought_model.pkl   # Trained Intelligence Core
│   └── feature_scaler.pkl          # Data Normalization Engine
├── requirements.txt                # Technology Stack
└── README.md                       # System Documentation
```

## 🧠 Intelligent Methodology

### 1. Satellite Data Acquisition
- Automated pipeline harvesting 10+ years of Earth observation data
- Multi-spectral analysis of vegetation stress indicators
- Continuous monitoring of hydro-meteorological variables

### 2. Feature Intelligence
- VCI Computation: Vegetation Condition Index for stress quantification
- Temporal Dynamics: Rolling precipitation aggregates (3,6-month windows)
- Anomaly Detection: Statistical deviation from historical baselines
- Lag Correlation: Time-delayed impact analysis of environmental factors

### 3. Machine Learning Excellence

| Model | Accuracy | Precision | Recall | F1-Score | Macro-F1 |
|-------|----------|-----------|--------|----------|----------|
| Logistic Regression | 66.67% | 66.37% | 66.67% | 65.94% | 62.97% |
| Random Forest | 83.33% | 85.04% | 83.33% | 83.30% | 81.16% |
| XGBoost | 87.50% | 89.35% | 87.50% | 87.37% | 87.94% |

### 4. Balanced Classification Framework
Our sophisticated 5-tier system combines vegetation health (VCI) with precipitation metrics:

```python
# Intelligent Decision Matrix
- 🟢 No Drought: VCI > 60 (Optimal conditions)
- 🟡 Light Drought: VCI ≤ 60 + precipitation deficit
- 🟠 Moderate Drought: VCI ≤ 45 + significant dry spell  
- 🔴 Severe Drought: VCI ≤ 30 + prolonged water shortage
- 🚨 Extreme Drought: VCI ≤ 15 + critical conditions
```

### 5. Operational Deployment
- Real-time prediction engine processing current satellite feeds
- Seasonal adaptation for Mekong Delta's unique climate patterns
- Interactive visualization suite for stakeholder engagement

## 📈 Performance Excellence

### 🏆 Model Superiority
- XGBoost Dominance: 87.5% accuracy in complex multi-class environment
- Seasonal Intelligence: Adaptive algorithms for dry (Dec-Apr) and rainy (May-Nov) seasons
- Feature Insight: VCI and precipitation metrics as primary predictors

### 🎯 Predictive Intelligence
Top Feature Contributions:
1. VCI (26.4%) - Vegetation stress primary indicator
2. NDVI (18.1%) - Biomass and crop health monitoring
3. 6-Month Precipitation (13.3%) - Long-term water availability
4. 3-Month Metrics (19.3%) - Medium-term drought progression

## 🖥️ Dashboard Experience

### Command Center Interface
- Live Risk Assessment: Real-time drought probability calculations
- Seasonal Analytics: Mekong Delta-specific climate pattern integration
- Multi-dimensional Scoring: Combined vegetation and precipitation risk indices
- Probability Distributions: Visual uncertainty quantification

### Advanced Intelligence Features
- Vegetation Health Monitoring: NDVI/VCI dual-index analysis
- Precipitation Intelligence: Cumulative rainfall pattern recognition
- Thermal Impact Assessment: Temperature stress evaluation
- Historical Context: Decadal trend analysis and anomaly detection

## 🔬 Research Impact

### Addressing Critical Challenges
- 🌾 Food Security: Early warning for rice production threats
- 💧 Water Management: Optimized irrigation and reservoir planning
- 🌡️ Climate Adaptation: Resilience strategies for changing patterns
- 📊 Policy Support: Data-driven agricultural decision making
- 🔬 Scientific Advancement: Methodological innovations in remote sensing

## 🛠️ Technology Stack

- Python 3.13: Core computational engine
- Google Earth Engine: Planetary-scale data access
- XGBoost: Championship-winning gradient boosting
- Scikit-learn: Machine learning foundation
- Plotly: Interactive scientific visualization
- Streamlit: Rapid deployment framework
- Pandas/NumPy: High-performance data processing

## 👨‍🔬 Research Leadership

Nguyen Van Quy  
Southern Branch of Joint Vietnam-Russia Tropical Science and Technology Research Center

🔬 Research Focus: Ecology, climate change impacts, and sustainable agricultural technologies in tropical delta regions.

## 📜 License

This transformative technology is available under the MIT License - fostering innovation while protecting intellectual contributions.

## 🙏 Collaborative Acknowledgments

- Google Earth Engine for democratizing satellite data access
- Climate Hazards Group for precipitation intelligence
- European Centre for atmospheric reanalysis excellence
- NASA MODIS for vegetation monitoring capabilities
- Research Institution for academic support and resources

---

⭐ Support Agricultural Innovation - Your stars fuel our mission to protect food security through advanced technology!

Engineering a climate-resilient future for the Mekong Delta 🌱