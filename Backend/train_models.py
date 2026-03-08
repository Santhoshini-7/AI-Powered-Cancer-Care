import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib

# --- RECTIFIED RISK MODEL TRAINING ---
print("Training Risk Model...")
try:
    df_risk = pd.read_csv('global_cancer_patients_2015_2024.csv')
    
    # DEBUG: Show columns found in the CSV
    print(f"Columns found in CSV: {df_risk.columns.tolist()}")

    # 1. Flexible Column Mapping
    if 'Location' in df_risk.columns:
        df_risk['Loc_Num'] = df_risk['Location'].map({'Urban': 0, 'Rural': 1})
    else:
        # Fallback: Create dummy data if column is missing
        print("Warning: 'Location' column not found. Using default values.")
        df_risk['Loc_Num'] = 0 

    if 'Gender' in df_risk.columns:
        df_risk['Gender_Num'] = df_risk['Gender'].map({'Male': 0, 'Female': 1})
    else:
        df_risk['Gender_Num'] = 0

    # 2. Define exactly 5 features
    X_risk = df_risk[['Age', 'Gender_Num', 'Smoking', 'Genetic_Risk', 'Loc_Num']]
    y_risk = df_risk['Target_Severity_Score']
    
    risk_model = RandomForestRegressor(n_estimators=100, random_state=42)
    risk_model.fit(X_risk, y_risk)
    joblib.dump(risk_model, 'cancer_risk_model.pkl')
    print("Risk Model Saved (5 features).")

except Exception as e:
    print(f"Risk Training Failed: {e}")

# --- 2. TRAIN DIAGNOSIS MODEL ---
print("Training Diagnosis Model...")
try:
    df_diag = pd.read_csv('cancer_data.csv') 
    X_diag = df_diag[['radius_mean', 'texture_mean', 'perimeter_mean']]
    y_diag = df_diag['diagnosis'].map({'M': 1, 'B': 0})
    
    diag_model = RandomForestClassifier(n_estimators=100, random_state=42)
    diag_model.fit(X_diag, y_diag)
    joblib.dump(diag_model, 'diagnosis_model.pkl')
    print("Diagnosis Model Saved.")
except Exception as e:
    print(f"Diagnosis Training Failed: {e}")

# --- 3. TRAIN PROGNOSIS MODEL ---
print("Training Prognosis Model...")
try:
    df_prog = pd.read_csv('colorectal_cancer_prediction.csv')
    agg_map = {"Low": 0, "Medium": 1, "High": 2}
    stage_map = {"I": 0, "II": 1, "III": 2, "IV": 3}
    
    X_prog = np.array([[stage_map[s], agg_map[a]] for s, a in zip(df_prog['Stage_at_Diagnosis'], df_prog['Tumor_Aggressiveness'])])
    y_prog = df_prog['Recurrence'].map({'Yes': 1, 'No': 0})
    
    prog_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    prog_model.fit(X_prog, y_prog)
    joblib.dump(prog_model, 'prognosis_model.pkl')
    print("Prognosis Model Saved.")
except Exception as e:
    print(f"Prognosis Training Failed: {e}")