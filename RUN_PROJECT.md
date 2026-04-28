# 🚀 Complete Guide to Run Saathi Project

## 📋 Step 1: Prerequisites Check

### ✅ Required Software:
- **Python 3.14+** (Check with: `python --version`)
- **Git** (Check with: `git --version`)
- **VS Code** (Recommended IDE)
- **Internet Connection** (For dependencies)

---

## 📁 Step 2: Navigate to Project Directory

```bash
# Open Command Prompt/Terminal
cd c:\Users\yuvra\OneDrive\Desktop\Saathi
```

---

## 🔧 Step 3: Setup Virtual Environment

### 3.1 Create Virtual Environment (First Time Only)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate
```

### 3.2 Verify Virtual Environment
```bash
# Check if activated (should show venv path)
which python
```

---

## 📦 Step 4: Install Dependencies

### 4.1 Install Required Packages
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### 4.2 Verify Installation
```bash
# Check key packages
python -c "import streamlit, sklearn, pandas, numpy, plotly; print('All packages installed successfully')"
```

---

## 🎯 Step 5: Verify Project Files

### 5.1 Check Essential Files
```bash
# List files in project
dir

# Should see:
# - app_perfect.py
# - requirements.txt
# - README.md
# - SETUP_GUIDE.md
# - models/ folder
# - crops_dataset.csv
# - fruits_dataset.csv
# - notebooks/ folder
```

### 5.2 Check Model Files
```bash
# Check models folder
dir models

# Should see:
# - crop_model_clean.pkl
# - crop_features_clean.pkl
# - fruit_model_clean.pkl
# - fruit_features_clean.pkl
```

---

## 🚀 Step 6: Run the Application

### 6.1 Start Streamlit App
```bash
# Method 1: Basic run
streamlit run app_perfect.py

# Method 2: With specific port
streamlit run app_perfect.py --server.port 8501

# Method 3: Headless mode (for production)
streamlit run app_perfect.py --server.headless true
```

### 6.2 Access the Application
- **Local URL**: http://localhost:8501
- **Network URL**: http://your-local-ip:8501
- **Browser**: Open Chrome/Firefox and go to the URL

---

## 🧪 Step 7: Test the Application

### 7.1 Test Crop Recommendations
1. **Open**: http://localhost:8501
2. **Select**: "🌾 Agricultural Crops" tab
3. **Set Parameters**:
   - Nitrogen (N): 90
   - Phosphorus (P): 42
   - Potassium (K): 43
   - Temperature: 20.8
   - Humidity: 82.0
   - pH: 6.5
   - Rainfall: 202.9
4. **Click**: "🔮 Recommend Crop"
5. **Expected Result**: rice (97% confidence)

### 7.2 Test Fruit Recommendations
1. **Select**: "🍎 Fruits" tab
2. **Set Parameters**:
   - Nitrogen (N): 85
   - Phosphorus (P): 65
   - Potassium (K): 75
   - Temperature: 30.0
   - Humidity: 80.0
   - pH: 6.8
   - Rainfall: 180.0
3. **Click**: "🔮 Recommend Fruit"
4. **Expected Result**: banana (67% confidence)

---

## 🔧 Troubleshooting

### ❌ Common Issues & Solutions

#### **Issue 1: "streamlit is not recognized"
```bash
# Solution: Install streamlit
pip install streamlit

# Or reinstall all dependencies
pip install -r requirements.txt --upgrade
```

#### **Issue 2: "ModuleNotFoundError: No module named 'sklearn'"
```bash
# Solution: Install scikit-learn
pip install scikit-learn

# Check virtual environment is activated
which python
```

#### **Issue 3: "Model loading failed"
```bash
# Check if models exist
dir models

# Re-download models if missing
# Check SETUP_GUIDE.md for model training
```

#### **Issue 4: "Port 8501 already in use"
```bash
# Use different port
streamlit run app_perfect.py --server.port 8502

# Or kill existing process
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### **Issue 5: "Git not recognized"
```bash
# Install Git first
# Download from: https://git-scm.com/download/win

# Or use VS Code integrated Git
```

---

## 🎯 Quick Start Commands

### 🚀 One-Command Start (Everything Ready)
```bash
# Navigate to project
cd c:\Users\yuvra\OneDrive\Desktop\Saathi

# Activate virtual environment
venv\Scripts\activate

# Run app
streamlit run app_perfect.py
```

### 📱 Mobile Access
```bash
# Run with network access
streamlit run app_perfect.py --server.address 0.0.0.0

# Access from mobile
http://your-pc-ip:8501
```

---

## 🎓 Success Checklist

- [ ] Python 3.14+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] All model files present
- [ ] App starts without errors
- [ ] Browser opens to localhost:8501
- [ ] Crop recommendations working
- [ ] Fruit recommendations working
- [ ] Radar charts displaying
- [ ] Tips showing correctly

---

## 🏆 Expected Results

### ✅ What You Should See:
1. **Beautiful UI**: Green agricultural theme
2. **Category Selection**: Crops vs Fruits tabs
3. **Interactive Sliders**: N, P, K, temperature, humidity, pH, rainfall
4. **Predictions**: High confidence recommendations
5. **Visualizations**: Radar charts for input parameters
6. **Tips**: Farming/growing guidance
7. **100% Category Accuracy**: No cross-confusion

### 🎯 Test Scenarios for Teacher:
1. **Rice**: 97% confidence (perfect conditions)
2. **Cotton**: 100% confidence (ideal conditions)
3. **Maize**: 32% confidence (realistic uncertainty)
4. **Mango**: 67% confidence (good fruit conditions)
5. **Papaya**: 51% confidence (moderate conditions)

---

## 📞 Support

### 🆘 If Issues Persist:
1. **Check Python version**: `python --version`
2. **Verify virtual environment**: `which python`
3. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
4. **Check model files**: `dir models`
5. **Restart computer**: Sometimes fixes environment issues

---

*Built with ❤️ for Easy Project Running | VPVS*
