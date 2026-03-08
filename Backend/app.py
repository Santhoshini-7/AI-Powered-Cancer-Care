from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# --- LOAD MODELS ---
try:
    risk_model = joblib.load('cancer_risk_model.pkl')
    diag_model = joblib.load('diagnosis_model.pkl')
    prog_model = joblib.load('prognosis_model.pkl')
    print("System Ready: All 3 Models Loaded.")
except Exception as e:
    print(f"Initialization Error: {e}")

# --- ROUTE 1: RISK ASSESSMENT ---
@app.route('/predict_risk', methods=['POST'])
def predict_risk():
    try:
        data = request.json
        print(f"DEBUG - Received Data: {data}")

        # 1. Explicitly convert strings to floats to avoid errors
        age = float(str(data.get('age', 0)).strip())
        smoking = float(data.get('smoking', 0))
        genetic = float(str(data.get('genetic', 0)).strip())
        
        # 2. Map Categories
        gender = 1.0 if data.get('gender') == "Female" else 0.0
        location = 1.0 if data.get('location') == "Rural" else 0.0

        # 3. Create the feature array (Ensure 5 features in the correct order)
        features = np.array([[age, gender, smoking, genetic, location]])
        
        # 4. Predict using the loaded model
        prediction = risk_model.predict(features)[0]
        
        return jsonify(round(float(prediction), 2))

    except ValueError as ve:
        print(f"DATA ERROR: Ensure Age and Genetic Risk are numerical. {ve}")
        return jsonify("Error: Invalid Input"), 400
    except Exception as e:
        print(f"SYSTEM ERROR: {e}")
        return jsonify("Model Error (500)"), 500

# --- ROUTE 2: DIAGNOSIS ---
@app.route('/predict_diagnosis', methods=['POST'])
def predict_diagnosis():
    try:
        data = request.json
        print(f"Diagnosis Input: {data}")
        
        features = np.array([[
            float(data['radius']), 
            float(data['texture']), 
            float(data['perimeter'])
        ]])
        
        prediction = diag_model.predict(features)[0]
        result = "Malignant" if prediction == 1 else "Benign"
        return jsonify(result)
    except Exception as e:
        print(f"Diagnosis Error: {e}")
        return jsonify("Error"), 500

# --- ROUTE 3: PROGNOSIS ---
@app.route('/predict_prognosis', methods=['POST'])
def predict_prognosis():
    try:
        data = request.json
        agg_map = {"Low": 0, "Medium": 1, "High": 2}
        stage_map = {"I": 0, "II": 1, "III": 2, "IV": 3}
        
        agg_val = agg_map.get(data['agg'])
        stage_val = stage_map.get(data['stage'])
        
        # 1. Get Model Prediction
        features = np.array([[stage_val, agg_val]])
        model_prediction = prog_model.predict(features)[0]
        
        # 2. Hybrid Logic (Safety Rule)
        if stage_val == 3 or (stage_val == 2 and agg_val == 2):
            result = "High Risk of Recurrence"
        else:
            result = "High Risk of Recurrence" if model_prediction == 1 else "Low Risk of Recurrence"
            
        print(f"Input: Stage {data['stage']}, Agg {data['agg']} -> Result: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"Prognosis Error: {e}")
        return jsonify(f"Server Error: {str(e)}"), 500

if __name__ == '__main__':
    print("Flask Server active at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)