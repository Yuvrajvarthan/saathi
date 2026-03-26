#!/usr/bin/env python3
# Test Current Model with Agricultural Crops

import pickle
import numpy as np

# Load model and features
print("Loading current model...")
try:
    with open('models/crop_model.pkl', 'rb') as file:
        crop_model = pickle.load(file)
    
    with open('models/crop_features.pkl', 'rb') as file:
        crop_features = pickle.load(file)
    
    print("Model loaded successfully!")
    print(f"Feature order: {crop_features}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Test agricultural crops only (exclude fruits)
agricultural_tests = [
    {
        'name': 'Rice (High Rainfall)',
        'values': [90, 42, 43, 20.8, 82.0, 6.5, 202.9],
        'expected': 'rice'
    },
    {
        'name': 'Maize (Drought Tolerant)',
        'values': [50, 50, 50, 25.0, 70.0, 7.0, 150.0],
        'expected': 'maize'
    },
    {
        'name': 'Cotton (Warm Climate)',
        'values': [117, 46, 19, 23.9, 79.8, 6.9, 80.3],
        'expected': 'cotton'
    },
    {
        'name': 'Jute (Fiber Crop)',
        'values': [78, 46, 39, 24.9, 79.6, 6.7, 174.7],
        'expected': 'jute'
    },
    {
        'name': 'Coffee (Plantation Crop)',
        'values': [101, 28, 29, 25.5, 58.8, 6.7, 158.0],
        'expected': 'coffee'
    }
]

print("Testing Agricultural Crops Only")
print("=" * 50)

results = []

for i, test in enumerate(agricultural_tests, 1):
    print(f"\nTest {i}: {test['name']}")
    print(f"Input: {test['values']}")
    print(f"Expected: {test['expected']}")
    
    # Create input in correct order
    input_dict = {
        'N': test['values'][0],
        'P': test['values'][1], 
        'K': test['values'][2],
        'temperature': test['values'][3],
        'humidity': test['values'][4],
        'ph': test['values'][5],
        'rainfall': test['values'][6]
    }
    
    # Create input array in training feature order
    input_data = np.array([[input_dict[feature] for feature in crop_features]])
    
    # Make prediction
    prediction = crop_model.predict(input_data)[0]
    confidence = crop_model.predict_proba(input_data).max() * 100
    correct = prediction == test['expected']
    
    print(f"Predicted: {prediction}")
    print(f"Confidence: {confidence:.2f}%")
    print(f"{'CORRECT' if correct else 'INCORRECT'}")
    
    results.append({
        'test': test['name'],
        'expected': test['expected'],
        'predicted': prediction,
        'confidence': confidence,
        'correct': correct
    })

print("\n" + "=" * 50)
print("AGRICULTURAL CROPS TEST RESULTS")
print("=" * 50)

# Calculate statistics
correct_predictions = sum(1 for r in results if r['correct'])
total_tests = len(results)
accuracy = (correct_predictions / total_tests) * 100
avg_confidence = sum(r['confidence'] for r in results) / total_tests

print(f"Total Tests: {total_tests}")
print(f"Correct Predictions: {correct_predictions}")
print(f"Agricultural Crops Accuracy: {accuracy:.1f}%")
print(f"Average Confidence: {avg_confidence:.2f}%")

print("\nDetailed Results:")
for i, result in enumerate(results, 1):
    status = "CORRECT" if result['correct'] else "INCORRECT"
    print(f"{i}. {result['test']}")
    print(f"   Expected: {result['expected']}")
    print(f"   Predicted: {result['predicted']}")
    print(f"   Confidence: {result['confidence']:.2f}% {status}")

# Grade agricultural performance
if accuracy >= 80:
    print(f"\nAGRICULTURAL CROPS: {accuracy:.1f}% accuracy - GOOD!")
    print("Your model works well for agricultural crops!")
else:
    print(f"\nAGRICULTURAL CROPS: {accuracy:.1f}% accuracy - NEEDS IMPROVEMENT")

print(f"\nNote: Fruits (papaya, mango, etc.) will have low accuracy due to dataset composition")
