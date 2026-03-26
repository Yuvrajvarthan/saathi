# 🌾 Saathi - AI Crop Advisor for Indian Farmers
# Complete Streamlit Application with Crop Recommendation and Disease Detection

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
from PIL import Image
# Try to import deep learning libraries, but handle DLL errors gracefully
PYTORCH_AVAILABLE = False
TENSORFLOW_AVAILABLE = False

try:
    import torch
    import torchvision.transforms as transforms
    from PIL import Image as PILImage
    PYTORCH_AVAILABLE = True
    print("PyTorch loaded successfully!")
except (ImportError, OSError) as e:
    if "DLL" in str(e):
        print("PyTorch DLL error - framework disabled")
    else:
        print("PyTorch not available")

try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing import image
    TENSORFLOW_AVAILABLE = True
    print("TensorFlow loaded successfully!")
except ImportError:
    print("TensorFlow not available")

if not PYTORCH_AVAILABLE and not TENSORFLOW_AVAILABLE:
    print("Running without deep learning framework - Crop recommendation only")
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Saathi - AI Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🌾 Saathi - AI Crop Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Empowering Indian Farmers with AI-Driven Agricultural Insights</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<h2 style="color: #2E8B57;">🚀 Navigation</h2>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["🌱 Crop Recommendation", "🌿 Disease Detection"])

# Load models and data
@st.cache_resource
def load_crop_model():
    """Load the crop recommendation model"""
    try:
        # Check if model file exists
        model_path = "models/crop_model.pkl"
        features_path = "models/crop_features.pkl"
        
        if not os.path.exists(model_path):
            st.error(f"❌ Crop model not found at {model_path}")
            return None, None
            
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
            
        with open(features_path, 'rb') as file:
            features = pickle.load(file)
            
        return model, features
    except Exception as e:
        st.error(f"❌ Error loading crop model: {str(e)}")
        return None, None

@st.cache_resource
def load_disease_model():
    """Load disease detection model"""
    if not PYTORCH_AVAILABLE and not TENSORFLOW_AVAILABLE:
        return None, None
        
    try:
        # Check if model file exists
        model_path = "models/disease_model.h5"
        classes_path = "models/disease_classes.json"
        
        if not os.path.exists(model_path):
            st.error(f"❌ Disease model not found at {model_path}")
            return None, None
        
        # Try loading with PyTorch first
        if PYTORCH_AVAILABLE:
            # For PyTorch, we'd need .pth file, but trying to load .h5
            try:
                import torch
                model = torch.load(model_path.replace('.h5', '.pth'), map_location='cpu')
                with open(classes_path, 'r') as file:
                    class_names = json.load(file)
                return model, class_names
            except:
                pass
        
        # Fallback to TensorFlow
        if TENSORFLOW_AVAILABLE:
            model = tf.keras.models.load_model(model_path)
            with open(classes_path, 'r') as file:
                class_names = json.load(file)
            return model, class_names
            
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading disease model: {str(e)}")
        return None, None

# Load models
crop_model, crop_features = load_crop_model()
disease_model, disease_classes = load_disease_model()

# Tab 1: Crop Recommendation
with tab1:
    st.markdown('<h2 class="sub-header">🌱 Crop Recommendation</h2>', unsafe_allow_html=True)
    
    if crop_model is None:
        st.markdown('<div class="warning-message">', unsafe_allow_html=True)
        st.write("⚠️ **Crop model not loaded!** Please ensure:")
        st.write("1. You have trained the crop model in Google Colab")
        st.write("2. Downloaded `crop_model.pkl` and `crop_features.pkl`")
        st.write("3. Placed them in the `models/` folder")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Crop recommendation model loaded successfully!")
        
        # Input form for crop parameters
        st.markdown("### 📊 Enter Soil and Weather Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Soil nutrients
            st.markdown("#### 🌍 Soil Nutrients")
            nitrogen = st.slider("Nitrogen (N)", 0, 200, 90, help="Nitrogen content in soil (kg/ha)")
            phosphorus = st.slider("Phosphorus (P)", 0, 200, 42, help="Phosphorus content in soil (kg/ha)")
            potassium = st.slider("Potassium (K)", 0, 200, 43, help="Potassium content in soil (kg/ha)")
            ph = st.slider("pH Level", 0.0, 14.0, 6.5, 0.1, help="Soil pH level")
            
        with col2:
            # Weather conditions
            st.markdown("#### 🌤️ Weather Conditions")
            temperature = st.slider("Temperature (°C)", 0.0, 50.0, 20.8, 0.1, help="Average temperature")
            humidity = st.slider("Humidity (%)", 0, 100, 82, help="Relative humidity")
            rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 202.9, 0.1, help="Annual rainfall")
        
        # Prediction button
        if st.button("🔮 Recommend Crop", type="primary"):
            # Create input array in the exact order of training features
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            
            # Ensure the input order matches the training feature order
            if crop_features:
                # Reorder input to match training feature order
                feature_order = crop_features  # ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                input_dict = {
                    'N': nitrogen,
                    'P': phosphorus, 
                    'K': potassium,
                    'temperature': temperature,
                    'humidity': humidity,
                    'ph': ph,
                    'rainfall': rainfall
                }
                # Create input array in correct order
                input_data = np.array([[input_dict[feature] for feature in feature_order]])
            
            # Make prediction
            try:
                prediction = crop_model.predict(input_data)[0]
                confidence = crop_model.predict_proba(input_data).max() * 100
                
                # Display results
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.markdown("### 🎯 Recommended Crop")
                st.markdown(f"**{prediction.upper()}**")
                st.markdown(f"**Model Confidence (Probability): {confidence:.2f}% based on Random Forest classification**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Additional insights
                st.markdown("### 📈 Additional Insights")
                
                # Create a radar chart for input parameters
                fig = go.Figure()
                
                categories = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']
                values = [nitrogen, phosphorus, potassium, temperature, humidity, ph*10, rainfall/3]  # Normalize for display
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Current Conditions'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title="Input Parameters Visualization"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Crop-specific recommendations
                st.markdown("### 💡 Farming Tips")
                
                crop_tips = {
                    'rice': ["🌾 Requires plenty of water", "🌡️ Best in warm temperatures", "💧 High rainfall areas"],
                    'maize': ["🌽 Drought tolerant", "☀️ Full sunlight required", "🌱 Well-drained soil"],
                    'cotton': ["🌿 Long growing season", "🌞 Warm climate", "💦 Moderate water"],
                    'wheat': ["🌾 Cool season crop", "❄️ Tolerates light frost", "💧 Moderate rainfall"],
                    'sugarcane': ["🎋 High water requirement", "🌡️ Tropical climate", "🌱 Long growing period"]
                }
                
                crop_lower = prediction.lower()
                if crop_lower in crop_tips:
                    for tip in crop_tips[crop_lower]:
                        st.write(f"• {tip}")
                else:
                    st.write("• Consult local agricultural experts for specific guidance")
                    st.write("• Consider soil testing for precise nutrient management")
                    st.write("• Monitor weather conditions regularly")
                    
            except Exception as e:
                st.error(f"❌ Error making prediction: {str(e)}")

# Tab 2: Disease Detection
with tab2:
    st.markdown('<h2 class="sub-header">🌿 Plant Disease Detection</h2>', unsafe_allow_html=True)
    
    if disease_model is None:
        st.markdown('<div class="warning-message">', unsafe_allow_html=True)
        st.write("⚠️ **Disease model not loaded!** Please ensure:")
        st.write("1. You have trained the disease model in Google Colab")
        st.write("2. Downloaded `disease_model.h5` and `disease_classes.json`")
        st.write("3. Placed them in the `models/` folder")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Plant disease detection model loaded successfully!")
        
        # Image upload
        st.markdown("### 📸 Upload Plant Leaf Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of a plant leaf for disease detection"
        )
        
        if uploaded_file is not None:
            try:
                # Display the uploaded image
                image_data = Image.open(uploaded_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📷 Uploaded Image")
                    st.image(image_data, caption="Uploaded leaf image", use_column_width=True)
                
                # Process image and make prediction
                with col2:
                    st.markdown("#### 🔍 Analysis Results")
                    
                    if not TENSORFLOW_AVAILABLE:
                        st.markdown('<div class="warning-message">', unsafe_allow_html=True)
                        st.markdown("### ⚠️ TensorFlow Not Available")
                        st.markdown("Disease detection requires TensorFlow which is not compatible with Python 3.14.")
                        st.markdown("**Solutions:**")
                        st.markdown("1. Use Python 3.10 or 3.11 for full functionality")
                        st.markdown("2. Train disease model in Colab and deploy separately")
                        st.markdown("3. Use cloud deployment for disease detection")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        # Preprocess image
                        img = image_data.resize((224, 224))
                        img_array = image.img_to_array(img)
                        img_array = img_array / 255.0  # Normalize
                        img_array = np.expand_dims(img_array, axis=0)
                        
                        # Make prediction
                        prediction = disease_model.predict(img_array)[0]
                        predicted_class_idx = np.argmax(prediction)
                        confidence = prediction[predicted_class_idx] * 100
                        predicted_class = disease_classes[predicted_class_idx]
                        
                        # Display results
                        if confidence > 70:
                            st.markdown('<div class="success-message">', unsafe_allow_html=True)
                            st.markdown(f"### 🎯 Detected: **{predicted_class}**")
                            st.markdown(f"**Confidence: {confidence:.2f}%**")
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif confidence > 50:
                            st.markdown('<div class="warning-message">', unsafe_allow_html=True)
                            st.markdown(f"### ⚠️ Possible: **{predicted_class}**")
                            st.markdown(f"**Confidence: {confidence:.2f}%**")
                            st.markdown("**Note: Low confidence - please provide a clearer image**")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-message">', unsafe_allow_html=True)
                            st.markdown(f"### ❌ Uncertain Detection")
                            st.markdown(f"**Confidence: {confidence:.2f}%**")
                            st.markdown("**Please upload a clearer, well-lit image of the leaf**")
                            st.markdown('</div>', unsafe_allow_html=True)
                
                # Show confidence distribution
                if TENSORFLOW_AVAILABLE and disease_model is not None:
                    st.markdown("### 📊 Confidence Distribution")
                    
                    # Create confidence chart
                    fig = go.Figure(data=[
                        go.Bar(
                            x=disease_classes,
                            y=prediction * 100,
                            text=[f"{conf:.2f}%" for conf in prediction * 100],
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title="Model Confidence for Each Disease Class",
                        xaxis_title="Disease Class",
                        yaxis_title="Confidence (%)",
                        xaxis_tickangle=-45,
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Disease information and recommendations
                st.markdown("### 💡 Disease Information & Treatment")
                
                disease_info = {
                    'healthy': {
                        'description': 'No disease detected. The plant appears healthy.',
                        'treatment': 'Continue regular monitoring and maintain good agricultural practices.',
                        'prevention': 'Regular watering, proper fertilization, and crop rotation.'
                    },
                    'rust': {
                        'description': 'Rust disease caused by fungal pathogens.',
                        'treatment': 'Apply fungicides containing azoxystrobin or tebuconazole.',
                        'prevention': 'Ensure proper air circulation and avoid overhead watering.'
                    },
                    'powdery_mildew': {
                        'description': 'Fungal disease appearing as white powdery coating.',
                        'treatment': 'Apply sulfur-based fungicides or neem oil.',
                        'prevention': 'Maintain proper spacing and ensure good ventilation.'
                    },
                    'leaf_spot': {
                        'description': 'Bacterial or fungal infection causing spots on leaves.',
                        'treatment': 'Remove infected leaves and apply copper-based fungicides.',
                        'prevention': 'Avoid overhead watering and ensure proper drainage.'
                    }
                }
                
                disease_lower = predicted_class.lower()
                if disease_lower in disease_info:
                    info = disease_info[disease_lower]
                    st.markdown(f"**Description:** {info['description']}")
                    st.markdown(f"**Treatment:** {info['treatment']}")
                    st.markdown(f"**Prevention:** {info['prevention']}")
                else:
                    st.markdown("**Description:** Disease detected. Please consult with local agricultural experts.")
                    st.markdown("**Treatment:** Consult with plant pathologists for appropriate treatment.")
                    st.markdown("**Prevention:** Implement integrated pest management practices.")
                
                # General recommendations
                st.markdown("### 🌱 General Plant Health Tips")
                tips = [
                    "🔍 Regularly monitor plants for early disease symptoms",
                    "💧 Water plants at the base to avoid leaf wetness",
                    "🌱 Ensure proper plant spacing for air circulation",
                    "🧹 Remove and destroy infected plant material",
                    "🔄 Practice crop rotation to prevent disease buildup",
                    "🌡️ Maintain optimal growing conditions"
                ]
                
                for tip in tips:
                    st.write(f"• {tip}")
                    
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
        else:
            st.info("📷 Please upload an image to start disease detection")
            
            # Sample images guide
            st.markdown("### 📸 Image Guidelines")
            st.markdown("""
            **For best results, please:**
            - Use clear, well-lit images
            - Focus on the affected leaf area
            - Include the entire leaf if possible
            - Avoid blurry or dark images
            - Use plain background if possible
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌾 <strong>Saathi - AI Crop Advisor</strong> | Empowering Indian Farmers with Technology</p>
    <p><em>Built with ❤️ for Indian Agriculture | VPVS </em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Model Information")
st.sidebar.markdown(f"""
**Crop Recommendation Model:**
- ✅ Status: {'Loaded' if crop_model else 'Not Loaded'}
- 🎯 Algorithm: Random Forest
- 📈 Expected Accuracy: ~95%

**Disease Detection Model:**
- ✅ Status: {'Loaded' if disease_model else 'Not Loaded'}
- 🧠 Architecture: MobileNetV2
- 📈 Expected Accuracy: ~92%
""")

st.sidebar.markdown("### 🛠️ Technical Stack")
st.sidebar.markdown("""
- **Backend:** Python 3.10+
- **ML Libraries:** scikit-learn, TensorFlow
- **Web App:** Streamlit
- **Image Processing:** Pillow (PIL)
- **Data Visualization:** Plotly
""")

st.sidebar.markdown("### 📞 Need Help?")
st.sidebar.markdown("""
If you face any issues:
1. Check model files in `/models/` folder
2. Ensure all dependencies are installed
3. Verify image format (JPG/PNG)
4. Contact project maintainers
""")
