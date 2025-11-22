import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Agricultural Drought Early Warning System - Mekong Delta",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #1a5276;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
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
    .prediction-card {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 2rem 0;
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
        👨‍🔬 <strong>Author:</strong> Nguyen Van Quy<br>
        <strong>Affiliation:</strong> Southern Branch of Joint Vietnam-Russia Tropical Science and Technology Research Center
    </div>
""", unsafe_allow_html=True)

# Header Information Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="info-card">
            <h3 style='color: white; margin: 0;'>📍 Region</h3>
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
            <h3 style='color: white; margin: 0;'>🎯 System</h3>
            <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>Models built with Python and R</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model = joblib.load('models/XGBoost_drought_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    return model, scaler

try:
    model, scaler = load_model()
except:
    st.error("⚠️ Error loading model. Please ensure model files exist in 'models/' folder.")
    st.stop()

# Sidebar - Professional Design
with st.sidebar:
    st.markdown("""
        <div class="sidebar-content">
            <h2 style='color: white; text-align: center;'>🎛️ Control Panel</h2>
            <p style='color: white; text-align: center;'>Adjust parameters for prediction</p>
        </div>
    """, unsafe_allow_html=True)

    # Season selection
    with st.expander("🌦️ **Season Information**", expanded=True):
        season = st.selectbox(
            "Current Season",
            ["Dry Season (Dec-Apr)", "Rainy Season (May-Nov)"],
            help="Mekong Delta seasonal patterns"
        )
        
        st.markdown("**Season Characteristics:**")
        if season == "Dry Season (Dec-Apr)":
            st.markdown("• 🌵 Lower rainfall")
            st.markdown("• ⚠️ Higher drought risk")
            st.markdown("• ❄️ Dec-Feb: Cool dry")
            st.markdown("• 🔥 Mar-Apr: Hot dry")
        else:
            st.markdown("• 🌧️ Higher rainfall") 
            st.markdown("• 🌿 Better vegetation")
            st.markdown("• 🌦️ May-Jul: Early rainy")
            st.markdown("• ⛈️ Aug-Nov: Peak rainy")

    # Vegetation Health
    with st.expander("🌱 **Vegetation Indicators**", expanded=True):
        ndvi = st.slider(
            "NDVI - Vegetation Health",
            min_value=0.20, max_value=0.80, value=0.55, step=0.01,
            help="Normalized Difference Vegetation Index (0.2-0.8)"
        )
        
        vci = st.slider(
            "VCI - Condition Index",
            min_value=0.0, max_value=100.0, value=65.0, step=1.0,
            help="Vegetation Condition Index (0-100%)"
        )
        
        ndvi_3month_avg = st.slider(
            "3-Month Avg NDVI",
            min_value=0.20, max_value=0.80, value=0.52, step=0.01
        )
        
        ndvi_lag1 = st.slider(
            "Previous Month NDVI",
            min_value=0.20, max_value=0.80, value=0.50, step=0.01
        )

    # Precipitation
    with st.expander("🌧️ **Precipitation Data**", expanded=True):
        precip_current = st.number_input(
            "Current Month Rainfall (mm)",
            min_value=0.0, max_value=500.0, value=80.0, step=5.0
        )
        
        precip_3month = st.number_input(
            "3-Month Cumulative (mm)",
            min_value=0.0, max_value=1500.0, value=250.0, step=10.0
        )
        
        precip_6month = st.number_input(
            "6-Month Cumulative (mm)",
            min_value=0.0, max_value=3000.0, value=600.0, step=20.0
        )
        
        precip_anomaly = st.slider(
            "Precipitation Anomaly (%)",
            min_value=-100.0, max_value=150.0, value=10.0, step=5.0
        )

    # Temperature
    with st.expander("🌡️ **Temperature**", expanded=False):
        temp_mean = st.slider(
            "Mean Temperature (°C)",
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
prediction = model.predict(input_data)[0]
prediction_proba = model.predict_proba(input_data)[0]

# 5-Level Balanced Classification System
drought_categories = ['No Drought', 'Light Drought', 'Moderate Drought', 'Severe Drought', 'Extreme Drought']
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
    "💧 Minor stress on vegetation with slightly below normal rainfall", 
    "⚠️ Moderate vegetation stress with significant rainfall deficit",
    "🔥 Severe vegetation stress with prolonged rainfall deficit",
    "🚨 Extreme vegetation stress with critical water shortage conditions"
]

# Main content - Prediction Result
st.markdown('<div class="section-header">🎯 Prediction Result</div>', unsafe_allow_html=True)

predicted_category = drought_categories[prediction]
predicted_gradient = drought_gradients[prediction]
predicted_description = drought_descriptions[prediction]
confidence = prediction_proba[prediction] * 100

# Large prediction display
st.markdown(f"""
    <div style='background: {predicted_gradient}; 
                padding: 4rem 2rem; 
                border-radius: 25px; 
                text-align: center; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                margin: 2rem 0;
                border: 3px solid rgba(255,255,255,0.2);'>
        <h1 style='color: white; margin: 0; font-size: 3.5rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{predicted_category}</h1>
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 15px; margin: 2rem auto; max-width: 300px;'>
            <p style='color: white; font-size: 1.5rem; margin: 0; font-weight: 600;'>Confidence: {confidence:.1f}%</p>
        </div>
        <p style='color: white; font-size: 1.3rem; margin: 1rem 0 0 0; font-weight: 500;'>
            {predicted_description}
        </p>
    </div>
""", unsafe_allow_html=True)

# Probability Distribution - Increased height and y-axis range
st.markdown('<div class="section-header">📊 Probability Distribution</div>', unsafe_allow_html=True)

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
        range=[0, max(prediction_proba * 100) * 1.2]  # Increased y-axis range
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

# Detailed Analysis
st.markdown('<div class="section-header">📈 Detailed Analysis</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("### 🌱 Vegetation Health Analysis")
    
    # Gauge chart for NDVI
    fig_ndvi = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ndvi,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "NDVI - Vegetation Health", 'font': {'size': 20, 'color': '#2c3e50'}},
        delta={'reference': 0.50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0.2, 0.8], 'tickwidth': 2, 'tickfont': {'size': 12}},
            'bar': {'color': "darkblue", 'thickness': 0.3},
            'steps': [
                {'range': [0.2, 0.4], 'color': "#ff6b6b"},
                {'range': [0.4, 0.6], 'color': "#ffe66d"},
                {'range': [0.6, 0.8], 'color': "#51cf66"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.45
            }
        }
    ))
    fig_ndvi.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50"}
    )
    st.plotly_chart(fig_ndvi, use_container_width=True)
    
    # VCI metric
    if vci > 60:
        vci_status = "Healthy ✅"
        vci_color = "#2ecc71"
        icon = "🌿"
    elif vci > 40:
        vci_status = "Moderate ⚠️"
        vci_color = "#f39c12"
        icon = "💧"
    else:
        vci_status = "Stressed 🔴"
        vci_color = "#e74c3c"
        icon = "🔥"
        
    st.markdown(f"""
        <div class="metric-card">
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <p style='color: #7f8c8d; font-size: 14px; margin: 0;'>Vegetation Condition Index</p>
                    <h2 style='color: #2c3e50; margin: 5px 0;'>{vci:.1f}%</h2>
                    <p style='color: {vci_color}; font-weight: bold; margin: 0;'>{icon} {vci_status}</p>
                </div>
                <div style='font-size: 3rem;'>{icon}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("### 🌧️ Precipitation Analysis")
    
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
    
    # Calculate appropriate y-axis range for precipitation chart
    max_precip = max(precip_current, precip_3month, precip_6month)
    y_range_max = max_precip * 1.15  # Add 15% padding
    
    fig_precip.update_layout(
        height=350,  # Reduced height for precipitation chart
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis_title="Precipitation (mm)",
        yaxis=dict(
            title_font=dict(size=16), 
            tickfont=dict(size=12), 
            gridcolor='rgba(0,0,0,0.1)',
            range=[0, y_range_max]  # Dynamic y-axis range
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
        risk_level = "🟢 Low Risk"
        risk_color = "#2ecc71"
        risk_icon = "✅"
    elif risk_score <= 6:
        risk_level = "🟡 Medium Risk" 
        risk_color = "#f39c12"
        risk_icon = "⚠️"
    elif risk_score <= 9:
        risk_level = "🟠 High Risk"
        risk_color = "#e67e22"
        risk_icon = "🔥"
    else:
        risk_level = "🔴 Severe Risk"
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
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🌾 Classification</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• 5-Level Drought System</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• VCI + Precipitation</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Seasonal Analysis</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Multi-Criteria</p>
        </div>
    """, unsafe_allow_html=True)

with col_sys2:
    st.markdown("""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🎯 Features</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• NDVI & VCI Indices</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Cumulative Rainfall</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Temperature Data</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Anomaly Detection</p>
        </div>
    """, unsafe_allow_html=True)

with col_sys3:
    st.markdown("""
        <div class="metric-card">
            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🛠️ Technology</h3>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Streamlit Framework</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• XGBoost Model</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Python & R</p>
            <p style='color: #5d6d7e; margin: 0.5rem 0;'>• Satellite Data</p>
        </div>
    """, unsafe_allow_html=True)

# Footer - Updated with requested changes
st.markdown("""
    <div class="footer">
        <h4 style='color: #2c3e50; margin-bottom: 1rem;'>Agricultural Drought Early Warning System - Mekong Delta</h4>
        <p style='color: #5d6d7e; margin: 0.5rem 0; font-size: 14px;'>
            Built with Streamlit | XGBoost with Accuracy: 0.8750 (87.50%)
        </p>
        <p style='color: #5d6d7e; margin: 0.5rem 0; font-size: 13px;'>
            Data: Google Earth Engine (MODIS, CHIRPS, ERA5) | Region: Mekong Delta, Vietnam | 2025
        </p>
    </div>
""", unsafe_allow_html=True)