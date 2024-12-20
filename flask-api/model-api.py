from flask import Flask, request, jsonify
import pickle
import numpy as np
import traceback
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Load the pre-trained Random Forest model
try:
    with open("rf_model.pkl", "rb") as file:
        rf_model = pickle.load(file)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    rf_model = None

@app.route('/predict', methods=['POST'])
def predict():
    logging.info("Received prediction request") 
    try:
        # Get JSON payload from request
        data = request.json
        logging.info(f"Received data: {data}")

        # Validasi input
        required_keys = ['bedroomCount', 'bathroomCount', 'carportCount', 
                        'landArea', 'buildingArea', 'locationEncoded']
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing key: {key}"}), 400

        # Extract input features
        try:
            features = [
                float(data['bedroomCount']),
                float(data['bathroomCount']),
                float(data['carportCount']),
                float(data['landArea']),
                float(data['buildingArea']),
                float(data['locationEncoded'])
            ]
        except ValueError as ve:
            return jsonify({"error": "Invalid input data. Ensure all values are numeric."}), 400

        # Validasi model
        if rf_model is None:
            return jsonify({"error": "Model not loaded"}), 500

        # Convert features to NumPy array and reshape
        features_array = np.array(features).reshape(1, -1)

        # Perform prediction
        predicted_price = rf_model.predict(features_array)[0]

        # Return prediction as JSON
        return jsonify({"predictedPrice": float(predicted_price)})

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
