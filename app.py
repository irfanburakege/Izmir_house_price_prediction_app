import streamlit as st
import pandas as pd
import pickle
import time
st.set_page_config(page_title="İzmir House Price Predictor", page_icon="🏠")

# 1. Loading saved brain and memory with pickle
@st.cache_resource #so it only loads once
def load_data():
    model = pickle.load(open("model.pkl", "rb"))
    district_tiers = pickle.load(open("district_tiers.pkl", "rb"))
    return model, district_tiers

model, district_tiers = load_data()

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# a. District Selection
# We are getting the list of districts from our dictionary keys
district_list = sorted(list(district_tiers.keys()))
selected_district = st.sidebar.selectbox("Select District", district_list)

# b. Size and Rooms selection
size = st.sidebar.number_input("Size (m²)", min_value=20, max_value=500, value=125)
rooms = st.sidebar.selectbox("Number of Rooms (Living room included!)", [1, 2, 3, 4, 5, 6, 7, 8, 9])

# Calculating tier for the selected district
# We now get the tier directly from our K-Means dictionary
selected_tier = district_tiers[selected_district]


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

# Showing what user selected
col1, col2, col3 = st.columns(3)
col1.metric("District", selected_district)
col1.caption(f"Market Tier: {selected_tier}") 
col2.metric("Size", f"{size} m²")
col3.metric("Rooms", f"{rooms} Rooms")

st.write("")

# 2. Prediction
# Predict button
if st.button("Predict Price", type="primary"):
    
    # Showing a message to show it's working
    with st.spinner('Analyzing the market trends...'):
        time.sleep(1) 
        
    # main prediction
    prediction = model.predict(input_data)[0]
    
    # Displaying the results
    st.subheader(f"Estimated Price: {prediction:,.0f} TL")
    
    # Since we are using Gradient Boosting, we can directly access feature_importances_
    st.write("")
    st.subheader("Why this price?")
    
    feature_names = input_data.columns
    
    # Creating a simple dataframe for the chart
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    # Displaying it as a bar chart
    st.bar_chart(importance_df.set_index('Feature'))
    
    # final text
    top_feature = importance_df.iloc[0]['Feature']
    st.info(f"💡 The estimation relied heavily on **{top_feature}** for this specific prediction.")
    st.warning("⚠️ **Please note:** This estimation is based on about 1,000 listings and general location areas. It does not account for specific details like views, floor levels, or building amenities. Please view this as a helpful market guide rather than a formal appraisal.")
