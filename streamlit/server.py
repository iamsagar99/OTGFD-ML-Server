from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# Load the model and scaler from the .pkl files
model_filename = '/Users/sagarpoudel/Downloads/transfer/pyserver/fast_api_app/isolation_forest_model_12bajyo.pkl'
scaler_filename = '/Users/sagarpoudel/Downloads/transfer/pyserver/fast_api_app/scaler_12bajyo.pkl'

try:
    model = joblib.load(model_filename)
    scaler = joblib.load(scaler_filename)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Model or scaler loading failed: {e}")

class PredictRequest(BaseModel):
    features: list

def predict_anomaly(raw_input, model, scaler):
    if isinstance(raw_input, pd.Series):
        raw_input = raw_input.values.reshape(1, -1)
    elif isinstance(raw_input, pd.DataFrame):
        raw_input = raw_input.values
    elif isinstance(raw_input, np.ndarray) and raw_input.ndim == 1:
        raw_input = raw_input.reshape(1, -1)
    
    raw_input_scaled = scaler.transform(raw_input)
    prediction = model.predict(raw_input_scaled)
    anomaly_score = model.decision_function(raw_input_scaled)
    return int(prediction[0]), float(anomaly_score[0])

@app.post('/predict')
def predict(request: PredictRequest):
    features = request.features
    if not isinstance(features, list) or len(features) == 0:
        raise HTTPException(status_code=400, detail="Invalid input format. Expected a list of features.")
    
    try:
        # Convert to a numpy array and reshape for a single prediction
        input_data = np.array(features).reshape(1, -1)
        prediction, anomaly_score = predict_anomaly(input_data, model, scaler)
        return {"prediction": prediction, "anomaly_score": anomaly_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8001)
    
    # Print a message to indicate the server is running
    print(f"Server is running on http://127.0.0.1:8001")
