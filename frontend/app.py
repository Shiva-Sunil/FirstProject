
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests

#Base URL
Backend_URL = 'http://backend:7860'

#Load Trained Model

@st.cache_resource()
def load_model():
    model = joblib.load('/content/deployment_files_backend/model.joblib')
    return model

model = load_model()

#Streamlit UI desing
st.title('Product Sales Prediction by SuperKart')
st.markdown('##')
st.write('This App helps you predict the Sales of a store for the upcoming quarter')

st.subheader('Enter the details')

#Get User Input
Product_Weight = st.number_input('Product Weight', min_value=5.7, value=12.6, step=0.1, max_value=20.4)
Product_Sugar_Content = st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
Product_Allocated_Area = st.number_input('Product Weight', min_value=0.001, value=0.06, step=0.001, max_value=0.3)
Product_Type = st.selectbox('Product Type', ['Dairy', 'Frozen Foods', 'Fruits and Vegetables', 'Meat',
                                            'Snack Foods', 'Canned', 'Soft Drinks', 'Baking Goods',
                                            'Household', 'Seafood', 'Breakfast', 'Health and Hygiene',
                                            'Starchy Foods', 'Breads', 'Others', 'Hard Drinks'])
Product_MRP = st.number_input('Product MRP', min_value=41, value=147, step=1, max_value=260)
Store_Id = st.selectbox('Store Id', ['OUT001', 'OUT004', 'OUT002', 'OUT003'])
Store_Establishment_Year = st.number_input('Store Establishment Year', min_value=1987, value=2002, step=1, max_value=2009)
Store_Location_City_Type = st.selectbox('Store Location City Type', ['Tier 1','Tier 2','Tier 3'])
Store_Type = st.selectbox('Store Type', ['Supermarket Type1', 'Supermarket Type2', 'Food Mart','Departmental Store'])
Store_Age = st.number_input('Store Age',min_value=17, value=23, step=1, max_value=39)

#Load User Input into a dataframe
input_date = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Store_Age': Store_Age
}])

#Predict Button
if st.button('Predict',type='primary'):
  response = requests.post(f'{Backend_URL}/v1/store', json=input_date.to_dict(orient='records')[0])
  if response.status_code == 200:
    prediction = response.json()
    st.success(f'The Predicted Sales is {prediction}')
  else:
    st.error('Error in prediction')

st.subheader('Batch_Prediction')

upload_file = st.file_uploader('Upload CSV file for multiple prediction', type=['csv'])

if upload_file is not None:
  if st.button('Predict Batch',type='primary'):
    response = requests.post(f'{Backend_URL}/v1/storebatch', files={'file': upload_file})
    if response.status_code == 200:
      prediction = response.json()
      st.success('Prediction Completed')
      st.write(prediction)
    else:
      st.error('Error in prediction')
  
