import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify

#Intialize Flask
SuperKart_api = Flask('SuperKart Price Predictor')

#Load the trained Model 
model = joblib.load('deployment_files_backend/model.joblib')

#Get Request
@SuperKart_api.get('/')
def home():
  return '<h1>Welcome to SuperKart Price Predictor</h1>'

#Post Request
@SuperKart_api.post('v1/store')
def predict_store_sales():
  store_data = request.get_json()

  #Retrive date from json
  extract = {
    'Product_Weight': store_data['Product_Weight'],
    'Product_Sugar_Content': store_data['Product_Sugar_Content'],
    'Product_Allocated_Area': store_data['Product_Allocated_Area'],
    'Product_Type': store_data['Product_Type'],
    'Product_MRP': store_data['Product_MRP'],
    'Store_Id': store_data['Store_Id'],
    'Store_Establishment_Year': store_data['Store_Establishment_Year'],
    'Store_Location_City_Type': store_data['Store_Location_City_Type'],
    'Store_Type': store_data['Store_Type'],
    'Store_Age': store_data['Store_Age']
  }

  #Load data into DF
  extract_data = pd.DataFrame(['extract'])

  #Predict the sales based on the input by passing the data to model
  predicted_sales = model.predict(extract_data)

  return jsonify({'Predicted Sales is': float(predicted_sales)})

#Post Request for Batch
@SuperKart_api.post('v1/storebatch')
def predict_store_sales_batch():
  file = request.files['file']

  #Read file
  extract_csv = pd.read_csv(file)

  #Predict the sales based on the input by passing the data to model
  predicted_sales = model.predict(extract_csv).tolist()

  #Create dict 
  store_id = extract_csv['Store_Id'].tolist()
  predicted_sales_dict = dict(zip(store_id, predicted_sales))

  return predicted_sales_dict

# Run the Flask app in debug mode
if __name__ == '__main__':
    SuperKart_api.run(debug=True)
