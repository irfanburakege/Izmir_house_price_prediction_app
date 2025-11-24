import streamlit as st
import pandas as pd
import pickle
import numpy as np 
import time
st.set_page_config(page_title="İzmir House Price Predictor", page_icon="🏠")

# Loading saved brain and memory
# We use a specific Streamlit command (@st.cache) so it only loads once
# instead of reloading every time you click a button.
@st.cache_resource
def load_data():
    model = pickle.load(open("model.pkl", "rb"))
    district_avgs = pickle.load(open("district_avgs.pkl", "rb"))
    return model, district_avgs

model, district_avgs = load_data()

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# A. District Selection
# We get the list of districts from our dictionary keys
district_list = sorted(list(district_avgs.keys()))
selected_district = st.sidebar.selectbox("Select District", district_list)

# B. Size and Rooms selection
size = st.sidebar.number_input("Size (m²)", min_value=20, max_value=500, value=100)
rooms = st.sidebar.selectbox("Number of Rooms (Living room included!)", [1, 2, 3, 4, 5, 6, 7, 8, 9])

# Calculating tier for the selected district
def get_tier(district):
    price = district_avgs.get(district, 5000000)
    if price >= 8000000: return 3
    elif price >= 5000000: return 2
    else: return 1

selected_tier = get_tier(selected_district)

# -Prediction
# dictionary for columns
input_data = pd.DataFrame({
    'Rooms': [rooms],
    'Size_m2': [size],
    'Tier': [selected_tier]
})

# Main UI
st.title("🏠 İzmir House Price Estimator")
st.markdown("Use the sidebar to enter house details and get an instant valuation.")

st.write("") # Divider line

# Showing what the user selected
col1, col2, col3 = st.columns(3)
col1.metric("District", selected_district)
col1.caption(f"Market Tier: {selected_tier}") 
col2.metric("Size", f"{size} m²")
col3.metric("Rooms", f"{rooms} Rooms")

st.write("")

# Predict button
if st.button("Predict Price", type="primary"):
    
    # Showing a message to show it's working
    with st.spinner('Analyzing the market trends...'):
        time.sleep(1) 
        
    # main prediction
    prediction = model.predict(input_data)[0]
    
    # Calculating confidence range
    individual_preds = [tree.predict(input_data)[0] for tree in model.estimators_]
    
    # 10th and 90th percentiles
    low_estimate = np.percentile(individual_preds, 10)
    high_estimate = np.percentile(individual_preds, 90)
    
    # Displaying the results
    st.subheader(f"Estimated Price: {prediction:,.0f} TL")
    
    # Showing the range graph
    st.write(f"📉 **Confidence Range:** {low_estimate:,.0f} TL — {high_estimate:,.0f} TL")
    st.progress(0.5) # A visual bar (dummy value for aesthetics)
    
    # Explaining the "why" (Feature Importance)
    st.write("")
    st.subheader("Why this price?")
    
    # Getting importance scores
    importances = model.feature_importances_
    feature_names = input_data.columns
    
    # Creating a simple dataframe for the chart
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Displaying it as a bar chart
    st.bar_chart(importance_df.set_index('Feature'))
    
    # final text
    top_feature = importance_df.iloc[0]['Feature']
    st.info(f"💡 The AI relied most heavily on **{top_feature}** for this specific prediction.")
    st.warning("⚠️ **Please note:** This estimation is based on about 1,000 listings and general location areas. It does not account for specific details like views, floor levels, or building amenities. Please view this as a helpful market guide rather than a formal appraisal.")
