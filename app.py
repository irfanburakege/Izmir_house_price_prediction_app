import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="İzmir House Price Predictor", page_icon="🏠")

# 2. LOAD THE SAVED BRAINS
# We use a specific Streamlit command (@st.cache) so it only loads once
# instead of reloading every time you click a button.
@st.cache_resource
def load_data():
    model = pickle.load(open("model.pkl", "rb"))
    district_avgs = pickle.load(open("district_avgs.pkl", "rb"))
    return model, district_avgs

model, district_avgs = load_data()

#3. THE SIDEBAR (User Inputs)
st.sidebar.header("Filter Options")

# A. District Selection
# We get the list of districts from our dictionary keys
district_list = sorted(list(district_avgs.keys()))
selected_district = st.sidebar.selectbox("Select District", district_list)

# Size and Rooms selection
size = st.sidebar.number_input("Size (m²)", min_value=20, max_value=500, value=100)
rooms = st.sidebar.selectbox("Number of Rooms (Living room included!)", [1, 2, 3, 4, 5, 6, 7, 8, 9])

#  4. THE LOGIC (Behind the Scenes) 
# We need to calculate the "Tier" for the selected district
# exactly like we did in the Jupyter Notebook.

def get_tier(district):
    price = district_avgs.get(district, 5000000)
    if price >= 8000000: return 3
    elif price >= 5000000: return 2
    else: return 1

selected_tier = get_tier(selected_district)

#  5. THE PREDICTION 
# Create a dictionary for the model (must match training columns!)
input_data = pd.DataFrame({
    'Rooms': [rooms],
    'Size_m2': [size],
    'Tier': [selected_tier]
})

#  6. THE MAIN PAGE UI 
st.title("🏠 İzmir House Price Estimator")
st.markdown("Use the sidebar to enter house details and get an instant valuation.")

st.write("") # Divider line

# Show what the user selected
col1, col2, col3 = st.columns(3)
col1.metric("District", selected_district)
col1.caption(f"Market Tier: {selected_tier}") # Show the hidden logic
col2.metric("Size", f"{size} m²")
col3.metric("Rooms", f"{rooms} Rooms")

st.write("")

import numpy as np # Add this at the top of your file!
import time

# ... (Keep your existing setup code) ...

if st.button("Predict Price", type="primary"):
    
    # 1. VISUAL EFFECT: Simulate calculation
    with st.spinner('Consulting the AI Architects...'):
        time.sleep(1) # Just for dramatic effect
        
    # 2. GET THE MAIN PREDICTION
    prediction = model.predict(input_data)[0]
    
    # 3. GET THE "RANGE" (The INTJ Feature)
    # We ask all 100 trees for their individual opinion
    # Note: This works because 'model' is a RandomForestRegressor
    individual_preds = [tree.predict(input_data)[0] for tree in model.estimators_]
    
    # We take the pessimistic view (10th percentile) and optimistic view (90th percentile)
    low_estimate = np.percentile(individual_preds, 10)
    high_estimate = np.percentile(individual_preds, 90)
    
    # 4. DISPLAY RESULTS
    st.subheader(f"Estimated Price: {prediction:,.0f} TL")
    
    # Show the range graph
    st.write(f"📉 **Confidence Range:** {low_estimate:,.0f} TL — {high_estimate:,.0f} TL")
    st.progress(0.5) # A visual bar (dummy value for aesthetics)
    
    # 5. EXPLAIN THE "WHY" (Feature Importance)
    st.write("")
    st.subheader("Why this price?")
    
    # Get importance scores
    importances = model.feature_importances_
    feature_names = input_data.columns
    
    # Create a simple dataframe for the chart
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Display it as a bar chart
    st.bar_chart(importance_df.set_index('Feature'))
    
    # Interpretation text
    top_feature = importance_df.iloc[0]['Feature']
    st.info(f"💡 The AI relied most heavily on **{top_feature}** for this specific prediction.")