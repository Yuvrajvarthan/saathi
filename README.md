# 🌾 Saathi – AI Crop Advisor for Indian Farmers

A smart web application that helps Indian farmers make better agricultural decisions using AI.

## 🚀 Features

1. **Crop Recommendation** - Get personalized crop suggestions based on:
   - Soil nutrients (Nitrogen, Phosphorus, Potassium)
   - Environmental conditions (Temperature, Humidity, pH, Rainfall)

2. **Plant Disease Detection** - Upload leaf photos to detect:
   - Common plant diseases
   - Early disease identification for better treatment

## 🛠️ Tech Stack

- **Backend**: Python 3.10+
- **ML Libraries**: scikit-learn, TensorFlow/Keras
- **Web App**: Streamlit
- **Data Processing**: pandas, numpy
- **Image Processing**: Pillow (PIL)

## 📋 Project Structure

```
Saathi/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── models/               # Trained ML models (not in repo)
│   ├── crop_model.pkl    # Crop recommendation model
│   └── disease_model.h5  # Disease detection model
└── notebooks/            # Google Colab notebooks
    ├── crop_training.ipynb
    └── disease_training.ipynb
```

## 🚀 Quick Start

### Step 1: Setup Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/saathi.git
cd saathi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Models
1. Open the provided Google Colab notebooks
2. Train and download the models
3. Place models in the `models/` folder:
   - `crop_model.pkl` from crop recommendation notebook
   - `disease_model.h5` from disease detection notebook

### Step 3: Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Model Performance

- **Crop Recommendation Accuracy**: ~95%
- **Disease Detection Accuracy**: ~92%

## 📚 Datasets Used

- [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- [Plant Disease Detection Dataset](https://www.kaggle.com/datasets/mgmitesh/plant-disease-detection-dataset)

## 🤝 Contributing

This project is developed as a mini-project for BE IT Semester 6. Feel free to fork and improve!

## 📧 Contact

Developed by: Yuvrajvarthan  
Email: yuvrajvarthannadar@gmail.com

---

*Built with ❤️ for Indian Farmers*
