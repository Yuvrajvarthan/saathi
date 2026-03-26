#!/usr/bin/env python3
# Final Project Check - Before Git Push

import os
import pickle
import streamlit
import pandas as pd
import numpy as np

print("FINAL PROJECT CHECK - BEFORE GIT PUSH")
print("=" * 60)

# Check 1: Essential Files
print("\n1. ESSENTIAL FILES CHECK:")
essential_files = [
    "app_perfect.py",
    "requirements.txt", 
    "README.md",
    "SETUP_GUIDE.md",
    ".gitignore"
]

for file in essential_files:
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024
        print(f"  FOUND {file} ({size:.1f} KB)")
    else:
        print(f"  MISSING {file}!")

# Check 2: Datasets
print("\n2. DATASETS CHECK:")
datasets = [
    "crops_dataset.csv",
    "fruits_dataset.csv"
]

for dataset in datasets:
    if os.path.exists(dataset):
        df = pd.read_csv(dataset)
        print(f"  FOUND {dataset} ({df.shape[0]} samples, {df.shape[1]} columns)")
        print(f"     Types: {sorted(df['label'].unique())}")
    else:
        print(f"  MISSING {dataset}!")

# Check 3: Models
print("\n3. MODELS CHECK:")
model_files = [
    "models/crop_model_clean.pkl",
    "models/crop_features_clean.pkl", 
    "models/fruit_model_clean.pkl",
    "models/fruit_features_clean.pkl"
]

for model_file in model_files:
    if os.path.exists(model_file):
        size = os.path.getsize(model_file) / 1024
        print(f"  FOUND {model_file} ({size:.1f} KB)")
    else:
        print(f"  MISSING {model_file}!")

# Check 4: Model Loading Test
print("\n4. MODEL LOADING TEST:")
try:
    # Load crop model
    with open('models/crop_model_clean.pkl', 'rb') as file:
        crop_model = pickle.load(file)
    
    with open('models/crop_features_clean.pkl', 'rb') as file:
        crop_features = pickle.load(file)
    
    print(f"  Crop Model: {len(crop_model.classes_)} classes loaded")
    print(f"     Classes: {sorted(crop_model.classes_)}")
    
    # Load fruit model
    with open('models/fruit_model_clean.pkl', 'rb') as file:
        fruit_model = pickle.load(file)
    
    with open('models/fruit_features_clean.pkl', 'rb') as file:
        fruit_features = pickle.load(file)
    
    print(f"  Fruit Model: {len(fruit_model.classes_)} classes loaded")
    print(f"     Classes: {sorted(fruit_model.classes_)}")
    
except Exception as e:
    print(f"  Model Loading Error: {e}")

# Check 5: App Import Test
print("\n5. APP IMPORT TEST:")
try:
    import streamlit as st
    print("  Streamlit imported successfully")
    
    # Test if app file exists and is readable
    if os.path.exists('app_perfect.py'):
        with open('app_perfect.py', 'r') as file:
            app_content = file.read()
            if 'streamlit' in app_content:
                print("  app_perfect.py contains Streamlit code")
            else:
                print("  app_perfect.py missing Streamlit code")
    else:
        print("  app_perfect.py not found")
        
except ImportError as e:
    print(f"  Import Error: {e}")

# Check 6: Requirements Test
print("\n6. REQUIREMENTS TEST:")
try:
    with open('requirements.txt', 'r') as file:
        requirements = file.read().strip().split('\n')
        print(f"  {len(requirements)} packages listed:")
        for req in requirements[:5]:  # Show first 5
            print(f"     - {req}")
        if len(requirements) > 5:
            print(f"     ... and {len(requirements) - 5} more")
except Exception as e:
    print(f"  Requirements Error: {e}")

# Check 7: Git Status
print("\n7. GIT STATUS:")
if os.path.exists('.git'):
    print("  Git repository initialized")
    if os.path.exists('.gitignore'):
        print("  .gitignore present")
    else:
        print("  .gitignore missing")
else:
    print("  Git repository not initialized")

# Check 8: Notebooks
print("\n8. NOTEBOOKS CHECK:")
notebook_dir = 'notebooks'
if os.path.exists(notebook_dir):
    notebooks = [f for f in os.listdir(notebook_dir) if f.endswith('.ipynb')]
    print(f"  {len(notebooks)} notebooks found:")
    for nb in notebooks:
        print(f"     - {nb}")
else:
    print("  notebooks directory not found")

# Check 9: Final Test Scenarios
print("\n9. FINAL TEST SCENARIOS:")
try:
    # Test crop model
    test_rice = [[90, 42, 43, 20.8, 82.0, 6.5, 202.9]]
    input_dict = {
        'N': 90, 'P': 42, 'K': 43,
        'temperature': 20.8, 'humidity': 82.0,
        'ph': 6.5, 'rainfall': 202.9
    }
    
    input_data = np.array([[input_dict[feature] for feature in crop_features]])
    crop_pred = crop_model.predict(input_data)[0]
    crop_conf = crop_model.predict_proba(input_data).max() * 100
    
    print(f"  Crop Test: {crop_pred} ({crop_conf:.2f}% confidence)")
    
    # Test fruit model
    test_mango = [[85, 65, 75, 30.0, 80.0, 6.8, 180.0]]
    input_dict = {
        'N': 85, 'P': 65, 'K': 75,
        'temperature': 30.0, 'humidity': 80.0,
        'ph': 6.8, 'rainfall': 180.0
    }
    
    input_data = np.array([[input_dict[feature] for feature in fruit_features]])
    fruit_pred = fruit_model.predict(input_data)[0]
    fruit_conf = fruit_model.predict_proba(input_data).max() * 100
    
    print(f"  Fruit Test: {fruit_pred} ({fruit_conf:.2f}% confidence)")
    
except Exception as e:
    print(f"  Test Error: {e}")

# Final Summary
print("\n" + "=" * 60)
print("FINAL SUMMARY:")
print("=" * 60)

# Count files
total_files = 0
missing_files = []

# Check all essential files
all_checks = [
    essential_files + datasets + model_files,
    ["app_perfect.py", "requirements.txt", "README.md"],
    ["models/crop_model_clean.pkl", "models/fruit_model_clean.pkl"]
]

for check_list in all_checks:
    for file in check_list:
        total_files += 1
        if not os.path.exists(file):
            missing_files.append(file)

print(f"Total Essential Files: {total_files}")
print(f"Missing Files: {len(missing_files)}")

if missing_files:
    print(f"\nMISSING FILES:")
    for file in missing_files:
        print(f"  - {file}")
    print(f"\nDO NOT PUSH TO GIT UNTIL MISSING FILES ARE FIXED!")
else:
    print(f"\nALL ESSENTIAL FILES PRESENT!")
    print(f"PROJECT READY FOR GIT PUSH!")
    print(f"READY FOR TEACHER PRESENTATION!")
    print(f"READY FOR DISEASE DETECTION PHASE!")

print(f"\nNEXT STEPS:")
print(f"1. Run: streamlit run app_perfect.py")
print(f"2. Test all scenarios")
print(f"3. Git add, commit, push")
print(f"4. Present to teacher")
