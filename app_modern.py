#!/usr/bin/env python3
# Saathi - AI Crop Advisor - Modern UI Version

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Saathi - AI Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafb 0%, #e8f5e8 100%);
    }
    
    /* Global text color fixes for readability */
    body {
        color: #2C3E50 !important;
    }
    
    .stMarkdown {
        color: #2C3E50 !important;
    }
    
    .stText {
        color: #2C3E50 !important;
    }
    
    /* Ensure all paragraph text is readable */
    p {
        color: #2C3E50 !important;
    }
    
    /* Ensure all div text is readable */
    div {
        color: #2C3E50 !important;
    }
    
    /* Override any light text in cards */
    .card p, .card div, .card span {
        color: #2C3E50 !important;
    }
    
    /* Header Styles */
    .hero-header {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 50%, #1F6B3F 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 139, 87, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-30px, -30px) rotate(180deg); }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        opacity: 0.95;
    }
    
    .hero-description {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Card Styles */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .card-header {
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Result Card Styles */
    .result-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .result-prediction {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .result-confidence {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        opacity: 0.95;
    }
    
    .result-reasons {
        text-align: left;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .result-reasons h4 {
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .result-reasons ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .result-reasons li {
        margin-bottom: 0.5rem;
        opacity: 0.95;
    }
    
    /* Input Section Styles */
    .input-section {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 2rem;
    }
    
    .input-group {
        margin-bottom: 2rem;
    }
    
    .input-group-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Status Card Styles */
    .status-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f9f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(46, 139, 87, 0.2);
        margin-bottom: 1rem;
    }
    
    .status-title {
        color: #2E8B57;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .status-info {
        color: #4B5563;
        font-size: 0.9rem;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Tips Card */
    .tips-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #2E8B57;
        margin-bottom: 2rem;
    }
    
    .tips-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tips-content {
        color: #2C3E50;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.4);
    }
    
    /* Selectbox Styles */
    .stSelectbox > div > div > select {
        background-color: #2E8B57;
        color: #F9FAFB;
        font-weight: 600;
        border-radius: 8px;
        border: 2px solid #2E8B57;
        padding: 0.75rem;
    }
    
    .stSelectbox > div > div > select option {
        background-color: #2E8B57;
        color: #F9FAFB;
        font-weight: 500;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #27AE60;
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
    }
    
    /* Slider Styles */
    .stSlider {
        margin-bottom: 1.5rem;
    }
    
    .stSlider > div > div > div > div {
        background-color: #2E8B57;
    }
    
    /* Footer Styles */
    .footer {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-top: 3rem;
    }
    
    .footer-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtitle {
        color: #4B5563;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .footer-author {
        color: #6B7280;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .result-prediction {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">🌾 Saathi - AI Crop Advisor</h1>
    <h2 class="hero-subtitle">AI-Powered Smart Farming Recommendations for Indian Agriculture</h2>
    <p class="hero-description">Helping farmers choose suitable crops using soil and weather data.</p>
</div>
""", unsafe_allow_html=True)

# Load specialized models
@st.cache_resource
def load_models():
    """Load the specialized crop and fruit models"""
    try:
        # Load crop model
        crop_model_path = "models/crop_model_clean.pkl"
        crop_features_path = "models/crop_features_clean.pkl"
        
        if os.path.exists(crop_model_path):
            with open(crop_model_path, 'rb') as file:
                crop_model = pickle.load(file)
            
            with open(crop_features_path, 'rb') as file:
                crop_features = pickle.load(file)
        else:
            crop_model, crop_features = None, None
        
        # Load fruit model
        fruit_model_path = "models/fruit_model_clean.pkl"
        fruit_features_path = "models/fruit_features_clean.pkl"
        
        if os.path.exists(fruit_model_path):
            with open(fruit_model_path, 'rb') as file:
                fruit_model = pickle.load(file)
            
            with open(fruit_features_path, 'rb') as file:
                fruit_features = pickle.load(file)
        else:
            fruit_model, fruit_features = None, None
            
        return crop_model, crop_features, fruit_model, fruit_features
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None, None, None

# Load models
crop_model, crop_features, fruit_model, fruit_features = load_models()

# Main Content
if crop_model is None or fruit_model is None:
    st.markdown("""
    <div class="card">
        <div class="card-header">⚠️ Model Loading Error</div>
        <p>AI models not found. Please ensure model files are in the 'models/' directory.</p>
        <p>Required files:</p>
        <ul>
            <li>crop_model_clean.pkl</li>
            <li>crop_features_clean.pkl</li>
            <li>fruit_model_clean.pkl</li>
            <li>fruit_features_clean.pkl</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    # Model Status Cards
    st.markdown('<div class="card-header">🤖 Model Status</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="status-card">
            <div class="status-title">🌾 Crop Recommendation Model</div>
            <div class="status-info">
                • Model loaded successfully<br>
                • Supports {} crop types<br>
                • High accuracy ML model<br>
                • Ready for predictions
            </div>
        </div>
        """.format(len(crop_model.classes_)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="status-card">
            <div class="status-title">🍎 Fruit Recommendation Model</div>
            <div class="status-info">
                • Model loaded successfully<br>
                • Supports {} fruit types<br>
                • High accuracy ML model<br>
                • Ready for predictions
            </div>
        </div>
        """.format(len(fruit_model.classes_)), unsafe_allow_html=True)
    
    # Category Selection
    st.markdown('<div class="card-header">🎯 Select Recommendation Type</div>', unsafe_allow_html=True)
    
    category = st.selectbox(
        "Choose what you'd like recommendations for:",
        ["🌾 Agricultural Crops", "🍎 Fruits"],
        help="Select between crop or fruit recommendations"
    )
    
    if category == "🌾 Agricultural Crops":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown('<div class="input-group-title">🌍 Soil Nutrients</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 90, help="Nitrogen content in soil (kg/ha)")
            phosphorus = st.slider("Phosphorus (P)", 0, 200, 42, help="Phosphorus content in soil (kg/ha)")
            potassium = st.slider("Potassium (K)", 0, 200, 43, help="Potassium content in soil (kg/ha)")
            ph = st.slider("pH Level", 0.0, 14.0, 6.5, 0.1, help="Soil pH level")
        
        with col2:
            st.markdown('<div class="input-group-title">🌤️ Weather Conditions</div>', unsafe_allow_html=True)
            temperature = st.slider("Temperature (°C)", 0.0, 50.0, 20.8, 0.1, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 82, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 202.9, 0.1, help="Annual rainfall")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction Button
        if st.button("🔮 Get Crop Recommendation", type="primary"):
            # Create input array in correct order
            input_dict = {
                'N': nitrogen,
                'P': phosphorus, 
                'K': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            
            # Create input DataFrame with exact training column names
            input_df = pd.DataFrame([[input_dict[feature] for feature in crop_features]], 
                                  columns=crop_features)
            
            # Make prediction
            try:
                prediction = crop_model.predict(input_df)[0]
                confidence = crop_model.predict_proba(input_df).max() * 100
                
                # Generate reasons based on input values
                reasons = []
                if rainfall > 150:
                    reasons.append("Suitable rainfall levels")
                if humidity > 70:
                    reasons.append("Good humidity conditions")
                if 6.0 <= ph <= 7.5:
                    reasons.append("Ideal soil pH range")
                if temperature >= 20 and temperature <= 30:
                    reasons.append("Optimal temperature range")
                if nitrogen >= 80:
                    reasons.append("Adequate nitrogen content")
                
                if not reasons:
                    reasons = "Conditions suitable for crop growth"
                
                # Display result
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Recommended Crop</div>
                    <div class="result-prediction">{prediction.upper()}</div>
                    <div class="result-confidence">Confidence: {confidence:.2f}%</div>
                    <div class="result-reasons">
                        <h4>Why Recommended:</h4>
                        <ul>
                            <li>{reasons if isinstance(reasons, str) else reasons[0]}</li>
                            {"<li>" + "</li><li>".join(reasons[1:]) + "</li>" if isinstance(reasons, list) and len(reasons) > 1 else ""}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">📊 Input Parameters Analysis</div>', unsafe_allow_html=True)
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=[nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3],
                    theta=['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
                    fill='toself',
                    name='Input Parameters',
                    line_color='#2E8B57',
                    fillcolor='rgba(46, 139, 87, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3) * 1.1],
                            tickcolor="#E5E7EB",
                            gridcolor="#374151"
                        ),
                        angularaxis=dict(
                            tickcolor="#E5E7EB",
                            gridcolor="#374151"
                        )
                    ),
                    title="Parameter Visualization",
                    font=dict(color="#F9FAFB"),
                    showlegend=False,
                    paper_bgcolor="#0B1220",
                    plot_bgcolor="#0B1220"
                )
                
                st.plotly_chart(fig, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Farming Tips
                tips = {
                    'rice': "🌾 Rice needs high rainfall (200-300mm) and warm temperatures (20-30°C). Ideal for regions with good water availability.",
                    'maize': "🌽 Maize is drought-tolerant and grows well in moderate rainfall (150-300mm). Requires well-drained soil.",
                    'wheat': "🌾 Wheat prefers cool temperatures (15-20°C) and moderate rainfall (100-200mm). Best for winter cultivation.",
                    'cotton': "🌿 Cotton needs warm climate (25-30°C) and moderate rainfall (150-200mm). Requires long growing season.",
                    'jute': "🌿 Jute thrives in warm, humid conditions (25-35°C) with high rainfall (200-300mm).",
                    'coffee': "☕ Coffee grows best in tropical highlands (18-22°C) with moderate rainfall (150-200mm).",
                    'blackgram': "🌾 Black gram (urad) grows well in warm climates with moderate rainfall (150-200mm).",
                    'chickpea': "🌾 Chickpea prefers cool, dry conditions with moderate rainfall (100-200mm).",
                    'kidneybeans': "🌾 Kidney beans need warm temperatures (20-25°C) and moderate rainfall (100-150mm).",
                    'lentil': "🌾 Lentil grows best in cool temperatures (15-20°C) with low to moderate rainfall (100-200mm).",
                    'mothbeans': "🌾 Moth beans are drought-tolerant and grow well in arid conditions.",
                    'mungbean': "🌾 Mung beans prefer warm temperatures (25-30°C) with moderate rainfall (150-200mm).",
                    'pigeonpeas': "🌾 Pigeon peas (tur) grow well in warm climates with moderate rainfall (150-250mm)."
                }
                
                st.markdown('<div class="tips-card">', unsafe_allow_html=True)
                st.markdown('<div class="tips-title">🌱 Farming Tips</div>', unsafe_allow_html=True)
                
                if prediction.lower() in tips:
                    st.markdown(f'<div class="tips-content">{tips[prediction.lower()]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="tips-content">Consult local agricultural experts for specific growing guidelines.</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error making prediction: {str(e)}")
    
    elif category == "🍎 Fruits":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown('<div class="input-group-title">🌍 Soil Nutrients</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 95, help="Nitrogen content in soil (kg/ha)")
            phosphorus = st.slider("Phosphorus (P)", 0, 200, 75, help="Phosphorus content in soil (kg/ha)")
            potassium = st.slider("Potassium (K)", 0, 200, 85, help="Potassium content in soil (kg/ha)")
            ph = st.slider("pH Level", 0.0, 14.0, 7.8, 0.1, help="Soil pH level")
        
        with col2:
            st.markdown('<div class="input-group-title">🌤️ Weather Conditions</div>', unsafe_allow_html=True)
            temperature = st.slider("Temperature (°C)", 0.0, 50.0, 35.0, 0.1, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 95, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 250.0, 0.1, help="Annual rainfall")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction Button
        if st.button("🔮 Get Fruit Recommendation", type="primary"):
            # Create input array in correct order
            input_dict = {
                'N': nitrogen,
                'P': phosphorus, 
                'K': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            
            # Create input DataFrame with exact training column names
            input_df = pd.DataFrame([[input_dict[feature] for feature in fruit_features]], 
                                  columns=fruit_features)
            
            # Make prediction
            try:
                prediction = fruit_model.predict(input_df)[0]
                confidence = fruit_model.predict_proba(input_df).max() * 100
                
                # Generate reasons based on input values
                reasons = []
                if temperature >= 25:
                    reasons.append("Warm tropical climate")
                if humidity >= 80:
                    reasons.append("High humidity conditions")
                if rainfall >= 200:
                    reasons.append("Abundant rainfall")
                if 6.5 <= ph <= 8.0:
                    reasons.append("Suitable soil pH")
                if nitrogen >= 80:
                    reasons.append("Rich soil nutrients")
                
                if not reasons:
                    reasons = "Conditions suitable for fruit cultivation"
                
                # Display result
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Recommended Fruit</div>
                    <div class="result-prediction">{prediction.upper()}</div>
                    <div class="result-confidence">Confidence: {confidence:.2f}%</div>
                    <div class="result-reasons">
                        <h4>Why Recommended:</h4>
                        <ul>
                            <li>{reasons if isinstance(reasons, str) else reasons[0]}</li>
                            {"<li>" + "</li><li>".join(reasons[1:]) + "</li>" if isinstance(reasons, list) and len(reasons) > 1 else ""}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">📊 Input Parameters Analysis</div>', unsafe_allow_html=True)
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=[nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3],
                    theta=['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
                    fill='toself',
                    name='Input Parameters',
                    line_color='#2E8B57',
                    fillcolor='rgba(46, 139, 87, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3) * 1.1],
                            tickcolor="#E5E7EB",
                            gridcolor="#374151"
                        ),
                        angularaxis=dict(
                            tickcolor="#E5E7EB",
                            gridcolor="#374151"
                        )
                    ),
                    title="Parameter Visualization",
                    font=dict(color="#F9FAFB"),
                    showlegend=False,
                    paper_bgcolor="#0B1220",
                    plot_bgcolor="#0B1220"
                )
                
                st.plotly_chart(fig, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Fruit Growing Tips
                tips = {
                    'papaya': "🍎 Papaya thrives in tropical climates (25-35°C) with high rainfall (200-300mm). Requires well-drained soil.",
                    'mango': "🥭 Mango needs warm temperatures (25-30°C) and moderate rainfall (150-250mm). Best for tropical regions.",
                    'banana': "🍌 Banana requires high humidity (80-90%) and warm temperatures (25-30°C) with abundant rainfall.",
                    'coconut': "🥥 Coconut grows in tropical coastal areas with high temperatures (27-32°C) and high rainfall.",
                    'pomegranate': "🍎 Pomegranate prefers semi-arid conditions with hot summers and cool winters.",
                    'grapes': "🍇 Grapes need moderate temperatures (15-25°C) and well-drained soil with moderate rainfall.",
                    'watermelon': "🍉 Watermelon requires warm temperatures (25-30°C) and high rainfall (200-300mm).",
                    'muskmelon': "🍈 Muskmelon grows well in warm temperatures (25-30°C) with moderate rainfall (150-200mm).",
                    'apple': "🍎 Apple grows best in temperate climates (15-20°C) with moderate rainfall (100-200mm).",
                    'orange': "🍊 Orange thrives in subtropical climates (20-30°C) with moderate rainfall (100-200mm)."
                }
                
                st.markdown('<div class="tips-card">', unsafe_allow_html=True)
                st.markdown('<div class="tips-title">🍎 Growing Tips</div>', unsafe_allow_html=True)
                
                if prediction.lower() in tips:
                    st.markdown(f'<div class="tips-content">{tips[prediction.lower()]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="tips-content">Consult horticulture experts for specific growing guidelines.</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error making prediction: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-title">🌾 Saathi - AI Crop Advisor</div>
    <div class="footer-subtitle">Built for TE IT DS Project</div>
    <div class="footer-author">Empowering Indian Farmers with Technology</div>
</div>
""", unsafe_allow_html=True)
