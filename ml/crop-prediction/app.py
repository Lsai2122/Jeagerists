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
    
    # Try to load additional models (they may not exist yet)
    try:
        with open('fertilizer_model.pkl', 'rb') as f:
            fertilizer_model = pickle.load(f)
    except FileNotFoundError:
        fertilizer_model = None
        print("Fertilizer model not found - will use mock predictions")
    
    try:
        with open('price_model.pkl', 'rb') as f:
            price_model = pickle.load(f)
    except FileNotFoundError:
        price_model = None
        print("Price model not found - will use mock predictions")
    
    try:
        with open('production_model.pkl', 'rb') as f:
            production_model = pickle.load(f)
    except FileNotFoundError:
        production_model = None
        print("Production model not found - will use mock predictions")
    
    with open('label_encoder_crop.pkl', 'rb') as f:
        crop_encoder = pickle.load(f)
    
    try:
        with open('label_encoder_state.pkl', 'rb') as f:
            state_encoder = pickle.load(f)
    except FileNotFoundError:
        state_encoder = None
        print("State encoder not found")
    
    with open('feature_info.json', 'r') as f:
        feature_info = json.load(f)
    
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    crop_model = None
    fertilizer_model = None
    price_model = None
    production_model = None
    crop_encoder = None
    state_encoder = None
    feature_info = {}

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
        if not crop_model or not crop_encoder:
            return jsonify({'error': 'Crop recommendation model not available'}), 500
        
        data = request.json
        
        # Validate input data
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract and validate features
        try:
            features = [
                float(data['nitrogen']),
                float(data['phosphorus']),
                float(data['potassium']),
                float(data['temperature']),
                float(data['humidity']),
                float(data['ph']),
                float(data['rainfall'])
            ]
        except ValueError as e:
            return jsonify({'error': 'Invalid input data: please provide numeric values'}), 400
        
        # Validate ranges
        if not (0 <= features[0] <= 200):  # nitrogen
            return jsonify({'error': 'Nitrogen must be between 0-200'}), 400
        if not (0 <= features[1] <= 200):  # phosphorus
            return jsonify({'error': 'Phosphorus must be between 0-200'}), 400
        if not (0 <= features[2] <= 400):  # potassium
            return jsonify({'error': 'Potassium must be between 0-400'}), 400
        if not (0 <= features[3] <= 50):  # temperature
            return jsonify({'error': 'Temperature must be between 0-50°C'}), 400
        if not (0 <= features[4] <= 100):  # humidity
            return jsonify({'error': 'Humidity must be between 0-100%'}), 400
        if not (0 <= features[5] <= 14):  # ph
            return jsonify({'error': 'pH must be between 0-14'}), 400
        if not (0 <= features[6] <= 500):  # rainfall
            return jsonify({'error': 'Rainfall must be between 0-500mm'}), 400
        
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
            'top_3_confidences': [round(prob, 3) for prob in top_3_probabilities]
        })
    
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/predict_fertilizer', methods=['POST'])
def predict_fertilizer():
    try:
        data = request.json
        
        # Validate input data
        required_fields = ['crop_year', 'area', 'annual_rainfall', 'nitrogen', 'phosphorus', 'potassium']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare features
        try:
            features = [
                int(data['crop_year']),
                float(data['area']),
                float(data['annual_rainfall']),
                float(data['nitrogen']),
                float(data['phosphorus']),
                float(data['potassium'])
            ]
        except ValueError as e:
            return jsonify({'error': 'Invalid input data: please provide numeric values'}), 400
        
        # Make predictions (use model if available, otherwise mock)
        if fertilizer_model:
            fertilizer_pred = fertilizer_model.predict([features])[0]
        else:
            # Mock prediction based on nitrogen levels
            fertilizer_pred = features[3] * 2.5 + np.random.uniform(-10, 10)
        
        return jsonify({
            'fertilizer_recommendation': round(fertilizer_pred, 2),
            'usage_tips': [
                'Apply fertilizer during early morning or late evening',
                'Water the field before applying fertilizer',
                'Use appropriate safety equipment when handling fertilizers',
                'Test soil pH before application',
                'Follow recommended dosage instructions'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': f'Fertilizer prediction failed: {str(e)}'}), 500

@app.route('/predict_price', methods=['POST'])
def predict_price():
    try:
        data = request.json
        
        # Validate input data
        required_fields = ['current_price', 'quantity', 'storage_cost', 'daily_loss', 'interest_rate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare features
        try:
            features = [
                float(data['current_price']),
                float(data['quantity']),
                float(data['storage_cost']),
                float(data['daily_loss']),
                float(data['interest_rate'])
            ]
        except ValueError as e:
            return jsonify({'error': 'Invalid input data: please provide numeric values'}), 400
        
        # Validate ranges
        if features[0] <= 0:  # current_price
            return jsonify({'error': 'Current price must be positive'}), 400
        if features[1] <= 0:  # quantity
            return jsonify({'error': 'Quantity must be positive'}), 400
        if features[2] < 0:  # storage_cost
            return jsonify({'error': 'Storage cost cannot be negative'}), 400
        if features[3] < 0:  # daily_loss
            return jsonify({'error': 'Daily loss cannot be negative'}), 400
        if not (0 <= features[4] <= 100):  # interest_rate
            return jsonify({'error': 'Interest rate must be between 0-100%'}), 400
        
        # Make predictions (use model if available, otherwise mock)
        current_price = float(data['current_price'])
        if price_model:
            price_15d = price_model.predict([features])[0]
        else:
            # Mock prediction with some market volatility
            volatility = np.random.uniform(-0.15, 0.15)  # ±15% price change
            price_15d = current_price * (1 + volatility)
        
        # Calculate potential earnings
        current_value = current_price * float(data['quantity'])
        future_value_15d = price_15d * float(data['quantity'])
        
        # Determine recommendation based on price trend
        price_change = (price_15d - current_price) / current_price
        recommendation = "Store" if price_15d > current_price else "Sell Now"
        
        # Risk assessment
        if abs(price_change) < 0.05:
            risk_level = "Very Low"
        elif abs(price_change) < 0.1:
            risk_level = "Low"
        elif abs(price_change) < 0.2:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return jsonify({
            'predicted_price_15d': round(price_15d, 2),
            'price_change_percent': round(price_change * 100, 2),
            'current_value': round(current_value, 2),
            'future_value_15d': round(future_value_15d, 2),
            'potential_profit': round(future_value_15d - current_value, 2),
            'recommendation': recommendation,
            'risk_level': risk_level,
            'market_insights': [
                'Monitor local market trends for better timing',
                'Consider storage costs in your decision',
                'Factor in transportation costs to market',
                'Check weather forecasts that might affect prices'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': f'Price prediction failed: {str(e)}'}), 500

@app.route('/predict_production', methods=['POST'])
def predict_production():
    try:
        data = request.json
        
        # Validate input data
        required_fields = ['area', 'nitrogen_req', 'phosphorus_req', 'potassium_req', 
                          'temperature', 'humidity', 'ph', 'rainfall', 'wind_speed', 'solar_radiation']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare features
        try:
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
        except ValueError as e:
            return jsonify({'error': 'Invalid input data: please provide numeric values'}), 400
        
        # Validate ranges
        if features[0] <= 0:  # area
            return jsonify({'error': 'Area must be positive'}), 400
        if not (0 <= features[1] <= 200):  # nitrogen_req
            return jsonify({'error': 'Nitrogen requirement must be between 0-200'}), 400
        if not (0 <= features[2] <= 200):  # phosphorus_req
            return jsonify({'error': 'Phosphorus requirement must be between 0-200'}), 400
        if not (0 <= features[3] <= 400):  # potassium_req
            return jsonify({'error': 'Potassium requirement must be between 0-400'}), 400
        if not (0 <= features[4] <= 50):  # temperature
            return jsonify({'error': 'Temperature must be between 0-50°C'}), 400
        if not (0 <= features[5] <= 100):  # humidity
            return jsonify({'error': 'Humidity must be between 0-100%'}), 400
        if not (0 <= features[6] <= 14):  # ph
            return jsonify({'error': 'pH must be between 0-14'}), 400
        if not (0 <= features[7] <= 500):  # rainfall
            return jsonify({'error': 'Rainfall must be between 0-500mm'}), 400
        if not (0 <= features[8] <= 50):  # wind_speed
            return jsonify({'error': 'Wind speed must be between 0-50 km/h'}), 400
        if not (0 <= features[9] <= 50):  # solar_radiation
            return jsonify({'error': 'Solar radiation must be between 0-50 MJ/m²/day'}), 400
        
        # Make predictions (use model if available, otherwise mock)
        area = float(data['area'])
        if production_model:
            yield_per_ha = production_model.predict([features])[0]
        else:
            # Mock prediction based on environmental factors
            base_yield = 25  # Base yield of 25 tons/ha
            temp_factor = min(1.0, max(0.3, 1 - abs(features[4] - 25) / 25))  # Optimal temp around 25°C
            rainfall_factor = min(1.0, features[7] / 200)  # Good rainfall up to 200mm
            soil_factor = min(1.0, (features[1] + features[2] + features[3] / 2) / 300)  # Nutrient balance
            yield_per_ha = base_yield * temp_factor * rainfall_factor * soil_factor * np.random.uniform(0.8, 1.2)
        
        total_production = yield_per_ha * area
        
        return jsonify({
            'yield_per_hectare': round(yield_per_ha, 2),
            'total_production': round(total_production, 2),
            'production_per_acre': round(yield_per_ha * 0.4047, 2),  # Convert to acres
            'optimization_tips': [
                'Monitor soil moisture regularly using sensors',
                'Adjust irrigation based on weather forecasts',
                'Apply balanced nutrients according to soil test results',
                'Protect crops from pests and diseases with IPM',
                'Consider crop rotation for soil health',
                'Use high-quality seeds adapted to local conditions',
                'Implement proper weed management strategies'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': f'Production estimation failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint to verify system status"""
    models_status = {
        'crop_model': crop_model is not None,
        'fertilizer_model': fertilizer_model is not None,
        'price_model': price_model is not None,
        'production_model': production_model is not None,
        'crop_encoder': crop_encoder is not None,
        'state_encoder': state_encoder is not None
    }
    
    all_models_ready = all(models_status.values())
    
    return jsonify({
        'status': 'healthy' if crop_model else 'degraded',
        'models_loaded': models_status,
        'api_version': '1.0.0',
        'features_available': list(feature_info.keys()) if feature_info else []
    })

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'KrishiKavach AI Farming API',
        'version': '1.0.0',
        'description': 'AI-powered farming decision support system',
        'endpoints': {
            'crop_recommendation': '/predict_crop',
            'fertilizer_recommendation': '/predict_fertilizer',
            'price_analysis': '/predict_price',
            'production_estimation': '/predict_production',
            'health_check': '/health'
        },
        'features': feature_info
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting KrishiKavach AI Farming System...")
    print(f"Crop model available: {crop_model is not None}")
    print(f"Fertilizer model available: {fertilizer_model is not None}")
    print(f"Price model available: {price_model is not None}")
    print(f"Production model available: {production_model is not None}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)