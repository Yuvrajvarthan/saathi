#!/usr/bin/env python3
# Saathi - AI Crop Advisor - Final Polished Version

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

# Premium CSS Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: #F8FAF7;
    }
    
    /* Typography */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2C3E50;
    }
    
    /* Hero Section */
    .hero-card {
        background: linear-gradient(135deg, #2E8B57 0%, #27AE60 50%, #229954 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(46, 139, 87, 0.15);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.95);
    }
    
    .hero-description {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Card Styles */
    .premium-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
    }
    
    .card-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Model Status Cards */
    .model-status-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid #2E8B57;
        box-shadow: 0 2px 12px rgba(46, 139, 87, 0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .model-status-title {
        color: #2E8B57;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .model-status-item {
        color: #555;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    /* Category Selector */
    .category-selector {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .category-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input Section */
    .input-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .input-section-title {
        color: #2E8B57;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #2E8B57 0%, #27AE60 100%);
        color: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(46, 139, 87, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .result-label {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .result-prediction {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-confidence {
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        opacity: 0.95;
    }
    
    .result-reasons {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1rem;
        text-align: left;
    }
    
    .result-reasons-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .result-reasons-list {
        margin: 0;
        padding-left: 1.2rem;
        font-size: 0.9rem;
        opacity: 0.95;
    }
    
    .result-reasons-list li {
        margin-bottom: 0.3rem;
    }
    
    /* Chart Section */
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Tips Section */
    .tips-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #2E8B57;
        margin-bottom: 1.5rem;
    }
    
    .tips-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tips-content {
        color: #555;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Footer */
    .footer {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin-top: 2rem;
    }
    
    .footer-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtitle {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .footer-author {
        color: #888;
        font-size: 0.85rem;
        font-style: italic;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #27AE60 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(46, 139, 87, 0.2);
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.3);
    }
    
    /* Selectbox Styles */
    .stSelectbox > div > div > select {
        background-color: white;
        color: #2C3E50;
        font-weight: 500;
        border: 2px solid #2E8B57;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Slider Styles */
    .stSlider {
        margin-bottom: 1rem;
    }
    
    .stSlider > div > div > div > div {
        background-color: #2E8B57;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #27AE60;
    }
    
    /* Error Message */
    .error-card {
        background: #FFF5F5;
        border: 2px solid #E53E3E;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .error-title {
        color: #E53E3E;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .result-prediction {
            font-size: 2rem;
        }
        
        .premium-card {
            padding: 1rem;
        }
        
        .model-status-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">Saathi - AI Crop Advisor</h1>
    <h2 class="hero-subtitle">AI-Powered Smart Farming Recommendations for Indian Agriculture</h2>
    <p class="hero-description">Helping farmers choose suitable crops using soil and weather data.</p>
</div>
""", unsafe_allow_html=True)

# Load specialized models (BACKEND UNTOUCHED)
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

# Load models (BACKEND UNTOUCHED)
crop_model, crop_features, fruit_model, fruit_features = load_models()

# Main Content
if crop_model is None or fruit_model is None:
    st.markdown("""
    <div class="error-card">
        <div class="error-title">⚠️ Model Loading Error</div>
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
    # Model Status Section
    st.markdown('<div class="card-title">🤖 Model Status</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="model-status-card">
            <div class="model-status-title">🌾 Crop Recommendation Model</div>
            <div class="model-status-item">✔ Model loaded successfully</div>
            <div class="model-status-item">✔ Supported types: {len(crop_model.classes_)} crops</div>
            <div class="model-status-item">✔ High accuracy ML model</div>
            <div class="model-status-item">✔ Ready for predictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="model-status-card">
            <div class="model-status-title">🍎 Fruit Recommendation Model</div>
            <div class="model-status-item">✔ Model loaded successfully</div>
            <div class="model-status-item">✔ Supported types: {len(fruit_model.classes_)} fruits</div>
            <div class="model-status-item">✔ High accuracy ML model</div>
            <div class="model-status-item">✔ Ready for predictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Category Selection
    st.markdown('<div class="category-selector">', unsafe_allow_html=True)
    st.markdown('<div class="category-title">🎯 Select Recommendation Type</div>', unsafe_allow_html=True)
    
    category = st.selectbox(
        "Choose recommendation type:",
        ["Agricultural Crops", "Fruits"],
        help="Select between crop or fruit recommendations"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if category == "Agricultural Crops":
        # Input Section - Two Cards Side by Side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-section-title">🌍 Soil Nutrients</div>', unsafe_allow_html=True)
            
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 90, help="Nitrogen content in soil (kg/ha)")
            phosphorus = st.slider("Phosphorus (P)", 0, 200, 42, help="Phosphorus content in soil (kg/ha)")
            potassium = st.slider("Potassium (K)", 0, 200, 43, help="Potassium content in soil (kg/ha)")
            ph = st.slider("pH Level", 0.0, 14.0, 6.5, 0.1, help="Soil pH level")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-section-title">☀ Weather Conditions</div>', unsafe_allow_html=True)
            
            temperature = st.slider("Temperature (°C)", 0.0, 50.0, 20.8, 0.1, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 82, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 202.9, 0.1, help="Annual rainfall")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction Button
        if st.button("🔮 Get Crop Recommendation", type="primary"):
            # Create input array in correct order (BACKEND UNTOUCHED)
            input_dict = {
                'N': nitrogen,
                'P': phosphorus, 
                'K': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            
            # Create input array in training feature order (BACKEND UNTOUCHED)
            input_data = np.array([[input_dict[feature] for feature in crop_features]])
            
            # Make prediction (BACKEND UNTOUCHED)
            try:
                prediction = crop_model.predict(input_data)[0]
                confidence = crop_model.predict_proba(input_data).max() * 100
                
                # Generate reasons based on input values
                reasons = []
                if rainfall > 150:
                    reasons.append("Suitable rainfall")
                if humidity > 70:
                    reasons.append("Good humidity")
                if 6.0 <= ph <= 7.5:
                    reasons.append("Ideal pH")
                if temperature >= 20 and temperature <= 30:
                    reasons.append("Suitable temperature")
                if nitrogen >= 80:
                    reasons.append("Adequate nitrogen")
                
                if not reasons:
                    reasons = ["Suitable conditions for crop growth"]
                
                # Display Result (COMPACT PREMIUM CARD)
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Recommended Crop</div>
                    <div class="result-prediction">{prediction.upper()}</div>
                    <div class="result-confidence">Confidence: {confidence:.2f}%</div>
                    <div class="result-reasons">
                        <div class="result-reasons-title">Why Recommended:</div>
                        <ul class="result-reasons-list">
                            {"<li>" + "</li><li>".join(reasons[:4]) + "</li>"}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Chart Section - Horizontal Bar Chart
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">📊 Input Parameters Analysis</div>', unsafe_allow_html=True)
                
                # Create horizontal bar chart
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=[nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3],
                    y=['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
                    orientation='h',
                    marker_color='#2E8B57',
                    name='Input Values'
                ))
                
                fig.update_layout(
                    title="Parameter Values",
                    xaxis_title="Value",
                    yaxis_title="Parameters",
                    font=dict(color="#2C3E50"),
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Farming Tips
                tips = {
                    'rice': "🌾 Rice grows best in high rainfall and warm climates. Ensure good irrigation and soil fertility.",
                    'maize': "🌽 Maize is drought-tolerant and grows well in moderate rainfall. Requires well-drained soil.",
                    'wheat': "🌾 Wheat prefers cool temperatures and moderate rainfall. Best for winter cultivation.",
                    'cotton': "🌿 Cotton needs warm climate and moderate rainfall. Requires long growing season.",
                    'jute': "🌿 Jute thrives in warm, humid conditions with high rainfall.",
                    'coffee': "☕ Coffee grows best in tropical highlands with moderate rainfall.",
                    'blackgram': "🌾 Black gram grows well in warm climates with moderate rainfall.",
                    'chickpea': "🌾 Chickpea prefers cool, dry conditions with moderate rainfall.",
                    'kidneybeans': "🌾 Kidney beans need warm temperatures and moderate rainfall.",
                    'lentil': "🌾 Lentil grows best in cool temperatures with low to moderate rainfall.",
                    'mothbeans': "🌾 Moth beans are drought-tolerant and grow well in arid conditions.",
                    'mungbean': "🌾 Mung beans prefer warm temperatures with moderate rainfall.",
                    'pigeonpeas': "🌾 Pigeon peas grow well in warm climates with moderate rainfall."
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
    
    elif category == "Fruits":
        # Input Section - Two Cards Side by Side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-section-title">🌍 Soil Nutrients</div>', unsafe_allow_html=True)
            
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 95, help="Nitrogen content in soil (kg/ha)")
            phosphorus = st.slider("Phosphorus (P)", 0, 200, 75, help="Phosphorus content in soil (kg/ha)")
            potassium = st.slider("Potassium (K)", 0, 200, 85, help="Potassium content in soil (kg/ha)")
            ph = st.slider("pH Level", 0.0, 14.0, 7.8, 0.1, help="Soil pH level")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-section-title">☀ Weather Conditions</div>', unsafe_allow_html=True)
            
            temperature = st.slider("Temperature (°C)", 0.0, 50.0, 35.0, 0.1, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 95, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 250.0, 0.1, help="Annual rainfall")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction Button
        if st.button("🔮 Get Fruit Recommendation", type="primary"):
            # Create input array in correct order (BACKEND UNTOUCHED)
            input_dict = {
                'N': nitrogen,
                'P': phosphorus, 
                'K': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            
            # Create input array in training feature order (BACKEND UNTOUCHED)
            input_data = np.array([[input_dict[feature] for feature in fruit_features]])
            
            # Make prediction (BACKEND UNTOUCHED)
            try:
                prediction = fruit_model.predict(input_data)[0]
                confidence = fruit_model.predict_proba(input_data).max() * 100
                
                # Generate reasons based on input values
                reasons = []
                if temperature >= 25:
                    reasons.append("Warm tropical climate")
                if humidity >= 80:
                    reasons.append("High humidity")
                if rainfall >= 200:
                    reasons.append("Abundant rainfall")
                if 6.5 <= ph <= 8.0:
                    reasons.append("Suitable soil pH")
                if nitrogen >= 80:
                    reasons.append("Rich soil nutrients")
                
                if not reasons:
                    reasons = ["Suitable conditions for fruit cultivation"]
                
                # Display Result (COMPACT PREMIUM CARD)
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Recommended Fruit</div>
                    <div class="result-prediction">{prediction.upper()}</div>
                    <div class="result-confidence">Confidence: {confidence:.2f}%</div>
                    <div class="result-reasons">
                        <div class="result-reasons-title">Why Recommended:</div>
                        <ul class="result-reasons-list">
                            {"<li>" + "</li><li>".join(reasons[:4]) + "</li>"}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Chart Section - Horizontal Bar Chart
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">📊 Input Parameters Analysis</div>', unsafe_allow_html=True)
                
                # Create horizontal bar chart
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=[nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3],
                    y=['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
                    orientation='h',
                    marker_color='#2E8B57',
                    name='Input Values'
                ))
                
                fig.update_layout(
                    title="Parameter Values",
                    xaxis_title="Value",
                    yaxis_title="Parameters",
                    font=dict(color="#2C3E50"),
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Fruit Growing Tips
                tips = {
                    'papaya': "🍎 Papaya thrives in tropical climates with high rainfall. Requires well-drained soil.",
                    'mango': "🥭 Mango needs warm temperatures and moderate rainfall. Best for tropical regions.",
                    'banana': "🍌 Banana requires high humidity and warm temperatures with abundant rainfall.",
                    'coconut': "🥥 Coconut grows in tropical coastal areas with high temperatures and rainfall.",
                    'pomegranate': "🍎 Pomegranate prefers semi-arid conditions with hot summers and cool winters.",
                    'grapes': "🍇 Grapes need moderate temperatures and well-drained soil with moderate rainfall.",
                    'watermelon': "🍉 Watermelon requires warm temperatures and high rainfall.",
                    'muskmelon': "🍈 Muskmelon grows well in warm temperatures with moderate rainfall.",
                    'apple': "🍎 Apple grows best in temperate climates with moderate rainfall.",
                    'orange': "🍊 Orange thrives in subtropical climates with moderate rainfall."
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
    <div class="footer-subtitle">Built for BE IT Mini Project</div>
    <div class="footer-author">Empowering Indian Farmers with Technology</div>
</div>
""", unsafe_allow_html=True)
