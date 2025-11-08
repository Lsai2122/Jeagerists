from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import json

app = Flask(__name__)

# Load all models and encoders
try:
    with open('crop_recommendation_model.pkl', 'rb') as f:
        crop_model = pickle.load(f)
    
    with open('fertilizer_model.pkl', 'rb') as f:
        fertilizer_model = pickle.load(f)
    
    with open('price_model.pkl', 'rb') as f:
        price_model = pickle.load(f)
    
    with open('production_model.pkl', 'rb') as f:
        production_model = pickle.load(f)
    
    with open('label_encoder_crop.pkl', 'rb') as f:
        crop_encoder = pickle.load(f)
    
    with open('label_encoder_state.pkl', 'rb') as f:
        state_encoder = pickle.load(f)
    
    with open('feature_info.json', 'r') as f:
        feature_info = json.load(f)
    
    print("All models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crop-recommendation')
def crop_recommendation():
    return render_template('crop_recommendation.html')

@app.route('/fertilizer-recommendation')
def fertilizer_recommendation():
    return render_template('fertilizer_recommendation.html')

@app.route('/price-analysis')
def price_analysis():
    return render_template('price_analysis.html')

@app.route('/production-estimation')
def production_estimation():
    return render_template('production_estimation.html')

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    try:
        data = request.json
        
        # Extract features
        features = [
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]
        
        # Make prediction
        prediction = crop_model.predict([features])[0]
        probabilities = crop_model.predict_proba([features])[0]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_crops = [crop_encoder.classes_[i] for i in top_3_indices]
        top_3_probabilities = [probabilities[i] for i in top_3_indices]
        
        return jsonify({
            'recommended_crop': crop_encoder.classes_[prediction],
            'confidence': float(probabilities[prediction]),
            'top_3_crops': top_3_crops,
            'top_3_confidences': top_3_probabilities
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_fertilizer', methods=['POST'])
def predict_fertilizer():
    try:
        data = request.json
        
        # Prepare features
        features = [
            int(data['crop_year']),
            float(data['area']),
            float(data['annual_rainfall']),
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium'])
        ]
        
        # Make predictions
        fertilizer_pred = fertilizer_model.predict([features])[0]
        
        return jsonify({
            'fertilizer_recommendation': round(fertilizer_pred, 2),
            'usage_tips': [
                'Apply fertilizer during early morning or late evening',
                'Water the field before applying fertilizer',
                'Use appropriate safety equipment when handling fertilizers'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_price', methods=['POST'])
def predict_price():
    try:
        data = request.json
        
        # Prepare features
        features = [
            float(data['current_price']),
            float(data['quantity']),
            float(data['storage_cost']),
            float(data['daily_loss']),
            float(data['interest_rate'])
        ]
        
        # Make predictions
        price_15d = price_model.predict([features])[0]
        
        # Calculate potential earnings
        current_value = float(data['current_price']) * float(data['quantity'])
        future_value_15d = price_15d * float(data['quantity'])
        
        # Determine recommendation based on price trend
        recommendation = "Store" if price_15d > float(data['current_price']) else "Sell Now"
        risk_level = "Low" if abs(price_15d - float(data['current_price'])) / float(data['current_price']) < 0.1 else "High"
        
        return jsonify({
            'predicted_price_15d': round(price_15d, 2),
            'current_value': round(current_value, 2),
            'future_value_15d': round(future_value_15d, 2),
            'potential_profit': round(future_value_15d - current_value, 2),
            'recommendation': recommendation,
            'risk_level': risk_level
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_production', methods=['POST'])
def predict_production():
    try:
        data = request.json
        
        # Prepare features
        features = [
            float(data['area']),
            float(data['nitrogen_req']),
            float(data['phosphorus_req']),
            float(data['potassium_req']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall']),
            float(data['wind_speed']),
            float(data['solar_radiation'])
        ]
        
        # Make predictions
        yield_per_ha = production_model.predict([features])[0]
        total_production = yield_per_ha * float(data['area'])
        
        return jsonify({
            'yield_per_hectare': round(yield_per_ha, 2),
            'total_production': round(total_production, 2),
            'optimization_tips': [
                'Monitor soil moisture regularly',
                'Adjust irrigation based on weather conditions',
                'Apply balanced nutrients according to soil test',
                'Protect crops from pests and diseases'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)