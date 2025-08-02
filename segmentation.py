import streamlit as st
import pandas as pd
import numpy as np
import joblib

kmeans = joblib.load('kmeans_model.pkl')
scaler = joblib.load('scaler_model.pkl')

st.title('customer segmentation App')
st.write ('Enter Customer details to predict the segment ')



st.header("About This App")
st.markdown("""
This app segments customers based on their demographic and purchasing behavior using KMeans clustering.  
Enter customer details below to predict which segment they belong to.
""")

st.header("Cluster Characteristics")
st.markdown("""
**Cluster 0:** Low income, minimal spending, low engagement.  
**Cluster 1:** Mid-age, moderate-high income, wine-focused, active online buyers.  
**Cluster 2:** Affluent, high-spending, diverse premium food buyers.  
**Cluster 3:** Middle class, low-moderate spending, basic consumption.  
**Cluster 4:** Older, luxury-oriented, high wine/gold consumption.  
**Cluster 5:** Elite, highest spending, very strong across all channels.
""")

st.header("Predict Customer Segment")

# Example input fields (customize as needed)
age = st.number_input("Age", min_value=18, max_value=100, value=30)
income = st.number_input("Income", min_value=0, value=30000)
education = st.selectbox("Education", ['Graduation', 'PhD', 'Master', 'Basic', '2n Cycle'])
marital_status = st.selectbox("Marital Status", ['Single', 'Married', 'Together', 'Divorced', 'Widow', 'others'])
total_children = st.number_input("Total Children", min_value=0, max_value=10, value=0)
total_spending = st.number_input("Total Spending", min_value=0, value=100)
mnt_wines = st.number_input("Wine Spending", min_value=0, value=0)
mnt_fruits = st.number_input("Fruit Spending", min_value=0, value=0)
mnt_meat = st.number_input("Meat Spending", min_value=0, value=0)
mnt_fish = st.number_input("Fish Spending", min_value=0, value=0)
mnt_sweets = st.number_input("Sweet Spending", min_value=0, value=0)
mnt_gold = st.number_input("Gold Spending", min_value=0, value=0)
num_deals = st.number_input("Number of Deals Purchases", min_value=0, value=0)
num_web = st.number_input("Number of Web Purchases", min_value=0, value=0)
num_catalog = st.number_input("Number of Catalog Purchases", min_value=0, value=0)
num_store = st.number_input("Number of Store Purchases", min_value=0, value=0)
num_web_visits = st.number_input("Number of Web Visits per Month", min_value=0, value=0)
recency = st.number_input("Recency (days since last purchase)", min_value=0, value=0)
customer_since = st.number_input("Customer Since (days)", min_value=0, value=0)

if st.button("Predict Segment"):
    # Prepare input as DataFrame
    input_dict = {
        'Age': age,
        'Education': education,
        'Total_spending': total_spending,
        'Marital_Status': marital_status,
        'Income': income,
        'Total_children': total_children,
        'MntWines': mnt_wines,
        'MntFruits': mnt_fruits,
        'MntMeatProducts': mnt_meat,
        'MntFishProducts': mnt_fish,
        'MntSweetProducts': mnt_sweets,
        'MntGoldProds': mnt_gold,
        'NumDealsPurchases': num_deals,
        'NumWebPurchases': num_web,
        'NumCatalogPurchases': num_catalog,
        'NumStorePurchases': num_store,
        'NumWebVisitsMonth': num_web_visits,
        'Recency': recency,
        'Customer_Since': customer_since
    }
    input_df = pd.DataFrame([input_dict])

    # One-hot encoding (must match training)
    input_encoded = pd.get_dummies(input_df, columns=['Education', 'Marital_Status'], drop_first=True)

    # Ensure all columns match training data
    # You may need to load the columns from your training set
    expected_cols = scaler.feature_names_in_
    for col in expected_cols:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[expected_cols]

    # Scale input
    input_scaled = scaler.transform(input_encoded)

    # Predict cluster
    cluster = kmeans.predict(input_scaled)[0]
    st.success(f"This customer belongs to **Cluster {cluster}**.")
