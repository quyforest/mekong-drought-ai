import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Agricultural Drought Early Warning System - Mekong Delta",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling - UPDATED CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a5276;
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-top: 0.5rem;
    }
    .author-info {
        text-align: center;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .info-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #3498db;
        margin-bottom: 1rem;
    }
    .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #dfe6e9 0%, #b2bec3 100%);
        border-radius: 15px;
    }
    .season-dry {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #e67e22;
    }
    .season-rainy {
        background: linear-gradient(135deg, #d1ecf1 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #3498db;
    }
    /* CSS FOR STAT CARDS */
    .season-stat-rainfall {
        background: linear-gradient(135deg, #4FC3F7 0%, #0288D1 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: white;
        border-left: 4px solid #0277BD;
    }
    .season-stat-temperature {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: white;
        border-left: 4px solid #EF6C00;
    }
    .season-stat-humidity {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: white;
        border-left: 4px solid #2E7D32;
    }
    .season-stat-risk-high {
        background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: white;
        border-left: 4px solid #C62828;
    }
    .season-stat-risk-low {
        background: linear-gradient(135deg, #66BB6A 0%, #388E3C 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: white;
        border-left: 4px solid #2E7D32;
    }
    .outlook-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        text-align: center;
    }
    .outlook-mild {
        background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
    }
    .outlook-moderate {
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
    }
    .outlook-severe {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    }
    .current-forecast {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        margin: 2rem 0;
        border: 3px solid rgba(255,255,255,0.2);
    }
    .confidence-badge {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 15px;
        margin: 2rem auto;
        max-width: 300px;
    }
    .risk-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .trend-indicator-up {
        color: #e74c3c;
        font-weight: bold;
    }
    .trend-indicator-down {
        color: #2ecc71;
        font-weight: bold;
    }
    .trend-indicator-stable {
        color: #f39c12;
        font-weight: bold;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
    <div class="main-header">
        🌾 Agricultural Drought Early Warning System
        <div class="sub-header">Mekong Delta Region</div>
    </div>
""", unsafe_allow_html=True)

# Author information
st.markdown("""
    <div class="author-info">
        🎭 <strong>Authors:</strong> Nguyen Van Quy & Dinh Ba Duy<br>
        <strong>Affiliation:</strong> Joint Vietnam-Russia Tropical Science and Technology Research Center
    </div>
""", unsafe_allow_html=True)

# Header Information Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="info-card">
            <h3 style='color: white; margin: 0;'>🗺️ Region</h3>
            <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>Mekong Delta, Vietnam</p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="info-card">
            <h3 style='color: white; margin: 0;'>🛰️ Data Source</h3>
            <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>Satellite-based (2015-2024)</p>
        </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
        <div class="info-card">
            <h3 style='color: white; margin: 0;'>💻 System</h3>
            <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>Python and R Models</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load model with improved error handling
@st.cache_resource
def load_model():
    try:
        if not os.path.exists('models/XGBoost_drought_model.pkl'):
            st.error("❌ Model file not found. Please check the models folder.")
            return None, None
            
        model = joblib.load('models/XGBoost_drought_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        return model, scaler
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None

model, scaler = load_model()

if model is None or scaler is None:
    st.error("🚫 Unable to load required model files. Please check your deployment.")
    st.stop()

# Season data for Mekong Delta - UPDATED WITH STANDARD TERMINOLOGY
SEASON_DATA = {
    "Dry Season (Dec-Apr)": {
        "description": "Characterized by low rainfall, high temperatures, and increased drought vulnerability",
        "characteristics": [
            "🌵 Low rainfall: 100-200 mm (5-10% of annual total)",
            "⚠️ High drought risk: Increased vulnerability to drought conditions",
            "❄️ Dec-Feb: Cool dry season - Milder temperatures (26-30°C)",
            "🔥 Mar-Apr: Hot dry season - High temperatures (30-35°C), extreme dryness",
            "🌊 Saltwater intrusion: Salinity penetrates 15-60km inland",
            "💧 Water scarcity: Critical freshwater shortages in coastal areas",
            "🌾 Agriculture: Winter-Spring crop season (main harvest)"
        ],
        "statistics": {
            "rainfall": "100-200 mm",
            "temperature": "26-35°C",
            "humidity": "70-75%",
            "drought_risk": "High",
            "agriculture": "Winter-Spring crop"
        },
        "color": "season-dry",
        "risk_level": "🟠 High Alert"
    },
    "Rainy Season (May-Nov)": {
        "description": "Features abundant rainfall, flooding, and optimal vegetation growth conditions",
        "characteristics": [
            "🌧️ High rainfall: 1,300-2,000 mm (90-95% of annual total)",
            "🌿 Optimal vegetation: Lush plant growth and green coverage",
            "🌦️ May-Jul: Early rainy season - Beginning of southwest monsoon",
            "⛈️ Aug-Nov: Peak rainy season - Heavy rainfall and flooding",
            "💦 Flooding season: Natural floods bring fertile silt deposits",
            "🎣 Fisheries peak: Ideal conditions for fishing and aquaculture",
            "🌾 Agriculture: Summer-Autumn and Autumn crop seasons"
        ],
        "statistics": {
            "rainfall": "1,300-2,000 mm",
            "temperature": "26-32°C",
            "humidity": "80-85%",
            "drought_risk": "Low",
            "agriculture": "Summer-Autumn crops"
        },
        "color": "season-rainy",
        "risk_level": "🟢 Normal Conditions"
    }
}

# Sidebar - Professional Design
with st.sidebar:
    st.markdown("""
        <div class="sidebar-content">
            <h2 style='color: white; text-align: center;'>🎛️ Control Panel</h2>
            <p style='color: white; text-align: center;'>Adjust parameters for prediction analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Season selection - UPDATED
    with st.expander("🌦️ **Seasonal Information**", expanded=True):
        season = st.selectbox(
            "Current Season",
            list(SEASON_DATA.keys()),
            help="Mekong Delta seasonal patterns and characteristics"
        )
        
        # Display detailed season information
        season_info = SEASON_DATA[season]
        
        # Display risk level
        st.markdown(f"**{season_info['risk_level']}: {season_info['description']}**")
        
        st.markdown("**🔍 Key Characteristics:**")
        for characteristic in season_info['characteristics']:
            st.markdown(f"• {characteristic}")
        
        st.markdown("**📊 Seasonal Statistics:**")
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            # Rainfall
            st.markdown(f"""
                <div class="season-stat-rainfall">
                    <strong>🌧️ Rainfall:</strong><br>
                    <span style='font-size: 1.1rem; font-weight: bold;'>{season_info['statistics']['rainfall']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Temperature
            st.markdown(f"""
                <div class="season-stat-temperature">
                    <strong>🌡️ Temperature:</strong><br>
                    <span style='font-size: 1.1rem; font-weight: bold;'>{season_info['statistics']['temperature']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            # Humidity
            st.markdown(f"""
                <div class="season-stat-humidity">
                    <strong>💧 Humidity:</strong><br>
                    <span style='font-size: 1.1rem; font-weight: bold;'>{season_info['statistics']['humidity']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Drought Risk
            risk_class = "season-stat-risk-high" if season_info['statistics']['drought_risk'] == "High" else "season-stat-risk-low"
            st.markdown(f"""
                <div class="{risk_class}">
                    <strong>⚠️ Drought Risk:</strong><br>
                    <span style='font-size: 1.1rem; font-weight: bold;'>{season_info['statistics']['drought_risk']}</span>
                </div>
            """, unsafe_allow_html=True)

    # Vegetation Health Indicators
    with st.expander("🌱 **Vegetation Health Indicators**", expanded=True):
        ndvi = st.slider(
            "🌿 NDVI - Normalized Difference Vegetation Index",
            min_value=0.20, max_value=0.80, value=0.55, step=0.01,
            help="Vegetation health index ranging from 0.2 (sparse vegetation) to 0.8 (dense vegetation)"
        )
        
        vci = st.slider(
            "📊 VCI - Vegetation Condition Index",
            min_value=0.0, max_value=100.0, value=65.0, step=1.0,
            help="Vegetation condition relative to historical minimum and maximum (0-100%)"
        )
        
        ndvi_3month_avg = st.slider(
            "📈 3-Month Average NDVI",
            min_value=0.20, max_value=0.80, value=0.52, step=0.01
        )
        
        ndvi_lag1 = st.slider(
            "🕐 Previous Month NDVI",
            min_value=0.20, max_value=0.80, value=0.50, step=0.01
        )

    # Precipitation Data
    with st.expander("🌧️ **Precipitation Data**", expanded=True):
        precip_current = st.number_input(
            "💧 Current Month Rainfall (mm)",
            min_value=0.0, max_value=500.0, value=80.0, step=5.0
        )
        
        precip_3month = st.number_input(
            "📅 3-Month Cumulative Rainfall (mm)",
            min_value=0.0, max_value=1500.0, value=250.0, step=10.0
        )
        
        precip_6month = st.number_input(
            "🗓️ 6-Month Cumulative Rainfall (mm)",
            min_value=0.0, max_value=3000.0, value=600.0, step=20.0
        )
        
        precip_anomaly = st.slider(
            "📊 Precipitation Anomaly (%)",
            min_value=-100.0, max_value=150.0, value=10.0, step=5.0,
            help="Deviation from long-term average precipitation"
        )

    # Temperature Data
    with st.expander("🌡️ **Temperature Data**", expanded=False):
        temp_mean = st.slider(
            "🌡️ Mean Temperature (°C)",
            min_value=20.0, max_value=35.0, value=28.0, step=0.5
        )

# Calculate derived features
precip_3month_avg = precip_3month / 3
precip_lag1 = precip_current * 0.9  # Simplified assumption

# Prepare input for prediction
input_data = pd.DataFrame({
    'ndvi': [ndvi],
    'precipitation_mm': [precip_current],
    'temp_mean_c': [temp_mean],
    'precip_3month': [precip_3month],
    'precip_6month': [precip_6month],
    'ndvi_3month_avg': [ndvi_3month_avg],
    'precip_3month_avg': [precip_3month_avg],
    'vci': [vci],
    'precip_anomaly': [precip_anomaly],
    'precip_lag1': [precip_lag1],
    'ndvi_lag1': [ndvi_lag1]
})

# Make prediction
try:
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]
except Exception as e:
    st.error(f"❌ Prediction error: {str(e)}")
    st.stop()

# 5-Level Drought Classification System - STANDARD TERMINOLOGY
drought_categories = ['No Drought', 'Mild Drought', 'Moderate Drought', 'Severe Drought', 'Extreme Drought']
drought_colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#8b0000']
drought_gradients = [
    'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
    'linear-gradient(135deg, #f1c40f 0%, #f39c12 100%)',
    'linear-gradient(135deg, #e67e22 0%, #d35400 100%)',
    'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
    'linear-gradient(135deg, #8b0000 0%, #600000 100%)'
]
drought_descriptions = [
    "🌿 Normal vegetation conditions with adequate rainfall patterns",
    "💧 Minor vegetation stress with slightly below normal rainfall", 
    "⚠️ Moderate vegetation stress with significant rainfall deficit",
    "🔥 Severe vegetation stress with prolonged rainfall deficit",
    "🚨 Extreme vegetation stress with critical water shortage conditions"
]

# Main content - Current Forecast Result
st.markdown('<div class="section-header">🎯 Current Drought Forecast</div>', unsafe_allow_html=True)

predicted_category = drought_categories[prediction]
predicted_gradient = drought_gradients[prediction]
predicted_description = drought_descriptions[prediction]
confidence = prediction_proba[prediction] * 100

# Large forecast display
st.markdown(f"""
    <div class="current-forecast" style='background: {predicted_gradient}'>
        <h1 style='color: white; margin: 0; font-size: 3.5rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{predicted_category}</h1>
        <div class="confidence-badge">
            <p style='color: white; font-size: 1.5rem; margin: 0; font-weight: 600;'>Model Confidence: {confidence:.1f}%</p>
        </div>
        <p style='color: white; font-size: 1.3rem; margin: 1rem 0 0 0; font-weight: 500;'>
            {predicted_description}
        </p>
    </div>
""", unsafe_allow_html=True)

# SHORT-TERM OUTLOOK SECTION - UPDATED
st.markdown('<div class="section-header">🔮 Short-term Outlook (Next 30 Days)</div>', unsafe_allow_html=True)

def predict_short_term_outlook(current_prediction, ndvi_trend, precip_trend, vci_trend, season):
    """
    Forecast drought conditions for next month based on current trends
    """
    # Trend scoring
    trend_score = 0
    
    # NDVI trend analysis
    if ndvi_trend < -0.05:  # Sharp decrease
        trend_score += 2
    elif ndvi_trend < -0.02:  # Slight decrease
        trend_score += 1
    elif ndvi_trend > 0.05:  # Sharp increase
        trend_score -= 2
    elif ndvi_trend > 0.02:  # Slight increase
        trend_score -= 1
    
    # Precipitation trend analysis
    if precip_trend < -20:  # Sharp decrease
        trend_score += 2
    elif precip_trend < -10:  # Slight decrease
        trend_score += 1
    elif precip_trend > 20:  # Sharp increase
        trend_score -= 2
    elif precip_trend > 10:  # Slight increase
        trend_score -= 1
    
    # VCI trend analysis
    if vci_trend < -10:  # Sharp decrease
        trend_score += 2
    elif vci_trend < -5:  # Slight decrease
        trend_score += 1
    elif vci_trend > 10:  # Sharp increase
        trend_score -= 2
    elif vci_trend > 5:  # Slight increase
        trend_score -= 1
    
    # Seasonal adjustment
    if season == "Dry Season (Dec-Apr)":
        trend_score += 1
    
    # Outlook classification
    if trend_score >= 3:
        outlook = "worsening"
    elif trend_score >= 1:
        outlook = "slightly_worsening"
    elif trend_score <= -3:
        outlook = "improving"
    elif trend_score <= -1:
        outlook = "slightly_improving"
    else:
        outlook = "stable"
    
    return outlook, trend_score

# Calculate trends
ndvi_trend = ndvi - ndvi_lag1
precip_trend = precip_anomaly
vci_trend = vci - 60

# Generate short-term forecast
outlook, trend_score = predict_short_term_outlook(
    prediction, ndvi_trend, precip_trend, vci_trend, season
)

# Display outlook results
col_out1, col_out2 = st.columns([2, 1])

with col_out1:
    outlook_config = {
        "worsening": {
            "class": "outlook-severe",
            "icon": "📈",
            "level": "Deteriorating",
            "message": "Conditions expected to worsen significantly"
        },
        "slightly_worsening": {
            "class": "outlook-moderate",
            "icon": "↗️", 
            "level": "Slightly Deteriorating",
            "message": "Conditions may slightly worsen"
        },
        "improving": {
            "class": "outlook-mild",
            "icon": "📉",
            "level": "Improving", 
            "message": "Conditions expected to improve"
        },
        "slightly_improving": {
            "class": "outlook-mild",
            "icon": "↘️",
            "level": "Slightly Improving",
            "message": "Conditions may slightly improve"
        },
        "stable": {
            "class": "outlook-card",
            "icon": "➡️",
            "level": "Stable",
            "message": "Conditions expected to remain stable"
        }
    }
    
    outlook_info = outlook_config[outlook]
    
    st.markdown(f"""
        <div class="outlook-card {outlook_info['class']}">
            <h2 style='color: white; margin: 0; font-size: 2.5rem;'>{outlook_info['icon']} {outlook_info['level']}</h2>
            <p style='color: white; font-size: 1.2rem; margin: 1rem 0;'>{outlook_info['message']}</p>
            <p style='color: white; font-size: 1rem; margin: 0.5rem 0 0 0; opacity: 0.9;'>
                Based on current vegetation trends and precipitation patterns
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_out2:
    # Trend indicators with proper formatting
    trend_ndvi = "↘️ Decreasing" if ndvi_trend < 0 else "↗️ Increasing" if ndvi_trend > 0 else "➡️ Stable"
    trend_precip = "↘️ Below normal" if precip_trend < 0 else "↗️ Above normal" if precip_trend > 0 else "➡️ Normal"
    trend_vci = "↘️ Decreasing" if vci_trend < 0 else "↗️ Increasing" if vci_trend > 0 else "➡️ Stable"
    
    st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>📈 Trend Indicators</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• NDVI Trend: {trend_ndvi}</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Precipitation: {trend_precip}</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• VCI Trend: {trend_vci}</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Trend Score: {trend_score}</p>
        </div>
    """, unsafe_allow_html=True)

# Recommendations based on outlook
st.markdown("#### 💡 Management Recommendations")

if outlook in ["worsening", "slightly_worsening"]:
    st.markdown("""
        <div class="recommendation-box">
            <h4 style='color: #e74c3c; margin-bottom: 1rem;'>⚠️ Preparedness Actions Recommended:</h4>
            <ul style='color: #5d6d7e;'>
                <li>Increase monitoring frequency of water resources</li>
                <li>Implement water conservation measures in agriculture</li>
                <li>Prepare for potential irrigation adjustments</li>
                <li>Coordinate with local water management authorities</li>
                <li>Review drought contingency plans</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
elif outlook in ["improving", "slightly_improving"]:
    st.markdown("""
        <div class="recommendation-box">
            <h4 style='color: #27ae60; margin-bottom: 1rem;'>✅ Favorable Outlook:</h4>
            <ul style='color: #5d6d7e;'>
                <li>Current water management practices appear adequate</li>
                <li>Continue regular monitoring schedule</li>
                <li>Consider opportunities for agricultural expansion</li>
                <li>Maintain water storage for dry periods</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="recommendation-box">
            <h4 style='color: #f39c12; margin-bottom: 1rem;'>🔍 Monitoring Recommended:</h4>
            <ul style='color: #5d6d7e;'>
                <li>Maintain current monitoring frequency</li>
                <li>Watch for sudden changes in conditions</li>
                <li>Continue standard agricultural practices</li>
                <li>Prepare for seasonal transitions</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Probability Distribution
st.markdown('<div class="section-header">📊 Drought Category Probability Distribution</div>', unsafe_allow_html=True)

fig_proba = go.Figure()
for i, (category, prob) in enumerate(zip(drought_categories, prediction_proba)):
    fig_proba.add_trace(go.Bar(
        x=[category],
        y=[prob * 100],
        marker_color=drought_colors[i],
        text=[f'{prob*100:.1f}%'],
        textposition='outside',
        textfont=dict(size=16, color='black', family='Arial Black'),
        hovertemplate=f'<b>{category}</b><br>Probability: {prob*100:.1f}%<extra></extra>'
    ))

fig_proba.update_layout(
    height=500,
    margin=dict(l=50, r=50, t=80, b=80),
    yaxis_title="Probability (%)",
    yaxis=dict(
        title_font=dict(size=18, color='#2c3e50'), 
        tickfont=dict(size=14), 
        gridcolor='rgba(0,0,0,0.1)',
        range=[0, max(prediction_proba * 100) * 1.2]
    ),
    xaxis=dict(tickfont=dict(size=12), tickangle=45),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title=dict(
        text='Drought Category Probability Distribution',
        font=dict(size=20, color='#2c3e50'),
        x=0.5
    )
)
st.plotly_chart(fig_proba, use_container_width=True)

# Detailed Analysis Sections
st.markdown('<div class="section-header">📈 Detailed Analysis</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("### 🌱 Vegetation Health Analysis")
    
    # NDVI Status Assessment
    if ndvi >= 0.6:
        ndvi_status = "Excellent 🌿"
        ndvi_color = "#2ecc71"
        ndvi_icon = "✅"
    elif ndvi >= 0.45:
        ndvi_status = "Good 💧"
        ndvi_color = "#f1c40f"
        ndvi_icon = "⚠️"
    else:
        ndvi_status = "Poor 🔥"
        ndvi_color = "#e74c3c"
        ndvi_icon = "❌"
    
    # VCI Status Assessment
    if vci > 60:
        vci_status = "Healthy 🌿"
        vci_color = "#2ecc71"
        vci_icon = "✅"
    elif vci > 40:
        vci_status = "Moderate 💧"
        vci_color = "#f39c12"
        vci_icon = "⚠️"
    else:
        vci_status = "Stressed 🔥"
        vci_color = "#e74c3c"
        vci_icon = "❌"
    
    # Vegetation metrics
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown(f"""
            <div class="metric-card">
                <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>NDVI Status</h3>
                <p style='color: {ndvi_color}; font-size: 1.2rem; font-weight: bold; margin: 0;'>{ndvi_icon} {ndvi_status}</p>
                <p style='color: #7f8c8d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Value: {ndvi:.3f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_a2:
        ndvi_percentage = ((ndvi - 0.2) / (0.8 - 0.2)) * 100
        st.markdown(f"""
            <div class="metric-card">
                <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>Health Level</h3>
                <p style='color: #2c3e50; font-size: 1.2rem; font-weight: bold; margin: 0;'>{ndvi_percentage:.1f}%</p>
                <p style='color: #7f8c8d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Normalized scale</p>
            </div>
        """, unsafe_allow_html=True)
    
    # VCI metric
    st.markdown(f"""
        <div class="metric-card">
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <p style='color: #7f8c8d; font-size: 14px; margin: 0;'>Vegetation Condition Index</p>
                    <h2 style='color: #2c3e50; margin: 5px 0;'>{vci:.1f}%</h2>
                    <p style='color: {vci_color}; font-weight: bold; margin: 0;'>{vci_icon} {vci_status}</p>
                </div>
                <div style='font-size: 3rem;'>{vci_icon}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("### ⛈️ Precipitation Analysis")
    
    # Precipitation chart
    precip_data = pd.DataFrame({
        'Period': ['Current Month', '3-Month', '6-Month'],
        'Precipitation (mm)': [precip_current, precip_3month, precip_6month],
        'Color': ['#3498db', '#2980b9', '#21618c']
    })
    
    fig_precip = go.Figure(data=[
        go.Bar(
            x=precip_data['Period'],
            y=precip_data['Precipitation (mm)'],
            marker_color=precip_data['Color'],
            text=precip_data['Precipitation (mm)'],
            texttemplate='%{text:.0f} mm',
            textposition='outside',
            textfont=dict(size=14, color='black', family='Arial Black'),
            marker_line_color='rgba(0,0,0,0.3)',
            marker_line_width=1.5
        )
    ])
    
    max_precip = max(precip_current, precip_3month, precip_6month)
    y_range_max = max_precip * 1.15
    
    fig_precip.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis_title="Precipitation (mm)",
        yaxis=dict(
            title_font=dict(size=16), 
            tickfont=dict(size=12), 
            gridcolor='rgba(0,0,0,0.1)',
            range=[0, y_range_max]
        ),
        xaxis=dict(tickfont=dict(size=12)),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_precip, use_container_width=True)
    
    # Risk assessment
    risk_score = 0
    
    # VCI-based risk
    if vci <= 15:
        risk_score += 4
    elif vci <= 30:
        risk_score += 3
    elif vci <= 45:
        risk_score += 2
    elif vci <= 60:
        risk_score += 1
    
    # Precipitation-based risk
    if precip_current < 10:
        risk_score += 4
    elif precip_current < 20:
        risk_score += 3
    elif precip_current < 35:
        risk_score += 2
    elif precip_current < 50:
        risk_score += 1
        
    if precip_3month < 30:
        risk_score += 4
    elif precip_3month < 50:
        risk_score += 3
    elif precip_3month < 80:
        risk_score += 2
    elif precip_3month < 120:
        risk_score += 1
    
    # NDVI-based risk
    if ndvi < 0.35:
        risk_score += 3
    elif ndvi < 0.45:
        risk_score += 2
    elif ndvi < 0.55:
        risk_score += 1
    
    # Determine risk level
    if risk_score <= 3:
        risk_level = "Low Risk"
        risk_color = "#2ecc71"
        risk_icon = "✅"
    elif risk_score <= 6:
        risk_level = "Medium Risk" 
        risk_color = "#f39c12"
        risk_icon = "🔴"
    elif risk_score <= 9:
        risk_level = "High Risk"
        risk_color = "#e67e22"
        risk_icon = "☀️"
    else:
        risk_level = "Severe Risk"
        risk_color = "#e74c3c"
        risk_icon = "🚨"
    
    st.markdown(f"""
        <div class="metric-card">
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <p style='color: #7f8c8d; font-size: 14px; margin: 0;'>Overall Risk Assessment</p>
                    <h2 style='color: #2c3e50; margin: 5px 0;'>{risk_icon} {risk_level}</h2>
                    <p style='color: {risk_color}; font-weight: bold; margin: 0;'>Risk Score: {risk_score}/15</p>
                </div>
                <div style='font-size: 3rem;'>{risk_icon}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# System Information
st.markdown('<div class="section-header">ℹ️ System Overview</div>', unsafe_allow_html=True)

col_sys1, col_sys2, col_sys3 = st.columns(3)

with col_sys1:
    st.markdown("""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>💾 Classification System</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• 5-Level Drought Classification</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• VCI + Precipitation Analysis</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Seasonal Pattern Recognition</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Multi-Criteria Assessment</p>
        </div>
    """, unsafe_allow_html=True)

with col_sys2:
    st.markdown("""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🎯 Monitoring Features</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• NDVI & VCI Vegetation Indices</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Cumulative Rainfall Analysis</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Temperature Monitoring</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Anomaly Detection System</p>
        </div>
    """, unsafe_allow_html=True)

with col_sys3:
    st.markdown("""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🛠️ Technology Stack</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Streamlit Web Framework</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• XGBoost Machine Learning</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Python & R Integration</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Satellite Data Processing</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <h4 style='color: #2c3e50; margin-bottom: 1rem;'>Agricultural Drought Early Warning System - Mekong Delta</h4>
        <p style='color: #5d6d7e; margin: 0.5rem 0; font-size: 14px;'>
            Built with Streamlit | XGBoost Model Accuracy: 0.8750 (87.50%)
        </p>
        <p style='color: #5d6d7e; margin: 0.5rem 0; font-size: 13px;'>
            Data Sources: Google Earth Engine (MODIS, CHIRPS, ERA5) | Region: Mekong Delta, Vietnam | November 2024
        </p>
    </div>
""", unsafe_allow_html=True)