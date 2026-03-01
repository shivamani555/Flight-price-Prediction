import streamlit as st
import pandas as pd
import joblib

# load model & features
model = joblib.load('flight_price_model.pkl')
features = joblib.load('model_features.pkl')

st.title("✈️ Flight Price Prediction App")

st.write("Enter flight details to predict price")

# ----- user inputs -----
airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet"])
source = st.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai"])
destination = st.selectbox("Destination", ["Cochin", "Delhi", "Hyderabad", "Kolkata"])

total_stops = st.selectbox("Total Stops", [0, 1, 2, 3, 4])

journey_day = st.number_input("Journey Day", 1, 31)
journey_month = st.number_input("Journey Month", 1, 12)

arrival_hour = st.number_input("Arrival Hour", 0, 23)
arrival_min = st.number_input("Arrival Minute", 0, 59)

duration_mins = st.number_input("Duration (minutes)", 30, 2000)

# ----- prediction button -----
# ----- fixed prediction block -----
if st.button("Predict Price"):
    # Initialize basic numeric data
    input_data = {
        'Total_Stops': total_stops,
        'Journey_day': journey_day,
        'Journey_month': journey_month,
        'Arrival_hour': arrival_hour,
        'Arrival_min': arrival_min,
        'Duration_mins': duration_mins
    }

    # Add Categorical logic: Set the selected Airline, Source, and Destination to 1
    # This matches the One-Hot Encoding used during training
    for col in features:
        if col not in input_data:
            if col == f"Airline_{airline}" or col == f"Source_{source}" or col == f"Destination_{destination}":
                input_data[col] = 1
            else:
                input_data[col] = 0

    input_df = pd.DataFrame([input_data])
    input_df = input_df[features] # Reorder columns to match the model

    prediction = model.predict(input_df)[0]
    st.success(f"💰 Estimated Flight Price: ₹{int(prediction)}")