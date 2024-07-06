import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

model = joblib.load('isolation_forest_model_12bajyo.pkl')
scaler = joblib.load('scaler_12bajyo.pkl')

def predict(features):
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)
    return prediction[0]

st.set_page_config(page_title='Anomaly Detection App', layout='wide')
st.markdown(
    """
    <style>
    .main {
        background-color: rgb(34, 34, 34);
        color: #EBC62F;
        font-size: 20px;
    }
    label, .stNumberInput input {
        font-size: 24px !important;
    }
    .stNumberInput div div input {
        font-size: 24px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Anomaly Detection App')
st.write("""
## Predict anomalies using an Isolation Forest model
Enter the feature values below and click on 'Predict' to see if the input is an anomaly.
""")

feature_names = [
    "Age", "Speed", "totalAmountMonthly", "totalCountMonthly", "Session_Len_deviation",
    "login_attempt_deviation", "Distance_Moved_km_deviation", "Amount_deviation", "score_device",
    "score_os", "score_auth_used", "score_txn_purpose", "Hour", "DayOfWeek"
]

with st.form("prediction_form"):
    columns = st.columns(2)
    feature_inputs = []

    for idx, feature in enumerate(feature_names):
        with columns[idx % 2]:
            value = st.number_input(f'{feature}', value=0.0, step=0.1, format="%.2f")
            feature_inputs.append(value)

    submitted = st.form_submit_button("Predict")

if submitted:
    features = np.array(feature_inputs)
    prediction = predict(features)
    result = "Anomaly" if prediction == -1 else "Normal"
    st.write(f'The predicted result is: {result}')
