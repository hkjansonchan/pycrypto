import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import date
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import yfinance as yf
import pandas as pd
import numpy as np

# Fetch Bitcoin historical data
data = yf.download("BTC-USD", start="2010-01-01", end=date.today())

# Convert data to pandas dataframe
df = pd.DataFrame(data).reset_index()

# Set date as index
df.set_index("Date", inplace=True)

# Normalize the data

scaler = MinMaxScaler()
df[["Open", "High", "Low", "Close"]] = scaler.fit_transform(
    df[["Open", "High", "Low", "Close"]]
)


# Define the RNN model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(df.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss="mean_squared_error", optimizer="adam")

# Split data into training and testing sets
train_size = int(0.8 * len(df))
train_data, test_data = df[0:train_size], df[train_size : len(df)]

# Train the model
model.fit(train_data, epochs=50, batch_size=1, verbose=2)

# Make predictions on the test data
predictions = model.predict
