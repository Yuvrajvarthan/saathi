# 🚀 Complete Setup Guide for Saathi Project

## 📋 Step 0: Prerequisites & Software Installation

### 1. Install Python
- **Download**: https://www.python.org/downloads/
- **Version**: Python 3.10 or 3.11
- **Important**: During installation, check "Add Python to PATH"

### 2. Install VS Code
- **Download**: https://code.visualstudio.com/
- **Extensions to install**:
  - Python (by Microsoft)
  - Jupyter (by Microsoft)
  - GitLens (for better Git integration)

### 3. Install Git
- **Download**: https://git-scm.com/download/win
- **Installation**: Use default settings

### 4. Create GitHub Account
- Go to https://github.com and create a free account
- Verify your email address

---

## 🌐 Step 1: GitHub Repository Setup

### 1.1 Create New Repository
1. Login to GitHub
2. Click "+" → "New repository"
3. Repository name: `saathi`
4. Description: `AI Crop Advisor for Indian Farmers`
5. Make it **Public**
6. Check "Add a README file"
7. Click "Create repository"

### 1.2 Clone Repository to VS Code
1. Open VS Code
2. Open Terminal (Ctrl + `)
3. Navigate to your Desktop: `cd Desktop`
4. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/saathi.git
cd saathi
```

---

## 💻 Step 2: Local Development Setup

### 2.1 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2.2 Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### 2.3 Create Project Structure
Your project should look like this:
```
saathi/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── SETUP_GUIDE.md        # This file
├── models/               # ML models (create this folder)
└── notebooks/            # Colab notebooks
    ├── crop_training.ipynb
    └── disease_training.ipynb
```

---

## 🧠 Step 3: Model Training in Google Colab

### 3.1 Open Crop Recommendation Notebook
1. Go to https://colab.research.google.com
2. Upload `notebooks/crop_training.ipynb`
3. Follow the instructions cell by cell
4. **Important**: Download these files when done:
   - `crop_model.pkl`
   - `crop_features.pkl`

### 3.2 Open Disease Detection Notebook
1. Open a new Colab notebook
2. Upload `notebooks/disease_training.ipynb`
3. **Enable GPU**: Runtime → Change runtime type → GPU
4. Follow the instructions cell by cell
5. **Important**: Download these files when done:
   - `disease_model.h5`
   - `disease_classes.json`

### 3.3 Place Models in Project
Create a `models` folder in your VS Code project and place all downloaded model files there:
```
models/
├── crop_model.pkl
├── crop_features.pkl
├── disease_model.h5
└── disease_classes.json
```

---

## 🚀 Step 4: Run the Streamlit App

### 4.1 Start the Application
```bash
# Make sure you're in the saathi directory with activated venv
streamlit run app.py
```

### 4.2 Access the App
- Open your browser
- Go to: http://localhost:8501
- You should see the Saathi app with two tabs

---

## 📤 Step 5: Push to GitHub

### 5.1 First Commit
```bash
# Check status
git status

# Add all files
git add .

# First commit
git commit -m "Initial commit: Complete Saathi AI Crop Advisor project"

# Push to GitHub
git push origin main
```

### 5.2 Future Commits
```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "Add feature: Improved disease detection UI"

# Push to GitHub
git push origin main
```

---

## 🧪 Step 6: Testing the Application

### 6.1 Test Crop Recommendation
1. Go to "🌱 Crop Recommendation" tab
2. Enter sample values:
   - Nitrogen: 90
   - Phosphorus: 42
   - Potassium: 43
   - Temperature: 20.8
   - Humidity: 82
   - pH: 6.5
   - Rainfall: 202.9
3. Click "🔮 Recommend Crop"
4. Should show a crop recommendation with confidence

### 6.2 Test Disease Detection
1. Go to "🌿 Disease Detection" tab
2. Upload a leaf image (JPG/PNG)
3. Should detect disease and show confidence

---

## 🐛 Common Troubleshooting

### Issue 1: "Model not found" Error
**Solution**: 
- Ensure model files are in the `models/` folder
- Check file names match exactly
- Verify files are not corrupted

### Issue 2: Virtual Environment Problems
**Solution**:
```bash
# Delete and recreate venv
deactivate
rmdir /s venv  # Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 3: Streamlit Not Starting
**Solution**:
```bash
# Install streamlit specifically
pip install streamlit

# Check installation
streamlit --version
```

### Issue 4: GPU Issues in Colab
**Solution**:
- Runtime → Change runtime type → GPU
- Restart the notebook
- Reduce batch size if memory error

---

## 📊 Expected Performance

### Crop Recommendation Model
- **Accuracy**: ~95%
- **Algorithm**: Random Forest
- **Training Time**: 2-5 minutes
- **Model Size**: ~500 KB

### Disease Detection Model
- **Accuracy**: ~92%
- **Architecture**: MobileNetV2
- **Training Time**: 10-15 minutes (GPU)
- **Model Size**: ~15-25 MB

---

## 🎯 Project Submission Checklist

### Code Repository ✅
- [ ] All code files uploaded to GitHub
- [ ] Proper folder structure
- [ ] README.md with project description
- [ ] requirements.txt with dependencies
- [ ] .gitignore properly configured

### Models ✅
- [ ] Crop model trained and saved
- [ ] Disease model trained and saved
- [ ] Models placed in correct folder
- [ ] Models load without errors

### Application ✅
- [ ] Streamlit app runs locally
- [ ] Both tabs work correctly
- [ ] UI is user-friendly
- [ ] Error handling implemented

### Documentation ✅
- [ ] Project report prepared
- [ ] PPT slides created
- [ ] Demo video recorded
- [ ] Code comments added

---

## 📞 Support Resources

### For Technical Issues
1. Check this SETUP_GUIDE.md first
2. Search online for specific error messages
3. Ask in class/WhatsApp group
4. Contact project instructor

### Dataset Issues
- Crop Dataset: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
- Disease Dataset: https://www.kaggle.com/datasets/mgmitesh/plant-disease-detection-dataset

### Learning Resources
- Python for Data Science: https://www.w3schools.com/python/
- Machine Learning Basics: https://www.coursera.org/learn/machine-learning
- Streamlit Documentation: https://docs.streamlit.io/

---

## 🎉 Congratulations!

You've successfully set up the Saathi AI Crop Advisor project! 

**What you've built:**
- ✅ Complete ML-powered web application
- ✅ Two functional AI models
- ✅ Professional GitHub repository
- ✅ Real-world agricultural solution

**Next Steps:**
1. Test thoroughly with different inputs
2. Prepare project report and presentation
3. Record demo video
4. Submit project on time

**Good luck with your project submission! 🚀**
