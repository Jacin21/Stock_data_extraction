#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

# Function to fetch and store data
def fetch_and_store_data():
    # Set up MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_data']
    collection = db['icici_bank']

    # Get the current time and the desired time range (11:15 AM - 2:15 PM)
    current_time = datetime.datetime.now()
    start_time = current_time.replace(hour=11, minute=15, second=0, microsecond=0)
    end_time = current_time.replace(hour=14, minute=15, second=0, microsecond=0)

    if start_time <= current_time <= end_time:
        # Get the historical data from Yahoo Finance
        icici_bank = yf.Ticker("ICICIBANK.NS")
        historical_data = icici_bank.history(start=start_time, end=current_time, interval='10m')

        # Convert historical data to JSON format
        historical_data_json = historical_data.to_dict(orient='index')

        # Flatten the data structure and convert Timestamp keys to strings
        historical_data_flattened = {}
        for timestamp, data in historical_data_json.items():
            timestamp_str = str(timestamp)
            historical_data_flattened[timestamp_str] = {
                "Open": data["Open"],
                "High": data["High"],
                "Low": data["Low"],
                "Close": data["Close"],
                "Volume": data["Volume"]
            }

        # Store data in MongoDB
        collection.insert_one({'timestamp': current_time, 'data': historical_data_flattened})
        print(f"Data for {current_time} stored in the database.")

# Create a scheduler and add the job
scheduler = BlockingScheduler()
scheduler.add_job(fetch_and_store_data, 'interval', minutes=10)

# Start the scheduler
scheduler.start()


# In[ ]:




