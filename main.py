import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Input # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.losses import MeanSquaredError # type: ignore
from sklearn.metrics import mean_squared_error

# Fetch Bitcoin historical data
start_date = date.today() - timedelta(days=365*5)
data = yf.download("BTC-USD", start=start_date, end=date.today())

# Convert data to pandas dataframe
df = pd.DataFrame(data).reset_index()

# Set date as index
df.set_index("Date", inplace=True)

# Normalize the data
scaler = MinMaxScaler()
df[['Open', 'High', 'Low', 'Close']] = scaler.fit_transform(df[['Open', 'High', 'Low', 'Close']])

# Calculate daily return
df['Daily Return'] = df['Close'].pct_change()

# Classify each day as bullish or bearish
df['Bullish/Bearish'] = np.where(df['Daily Return'] > 0, 'Bullish', 'Bearish')

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_df = df[:train_size].copy()
test_df = df[train_size:].copy()

# Define the model
model = Sequential()

# Add the Input layer
model.add(Input(shape=(1,)))

# Add LSTM layer
model.add(LSTM(50, activation='relu'))

# Add Dense layer
model.add(Dense(1))

# Compile the model
model.compile(optimizer=Adam(), loss=MeanSquaredError())

# Remove rows with None values from the data
train_df.dropna(inplace=True)
test_df.dropna(inplace=True)

# Fit the model
model.fit(train_df['Daily Return'].values.reshape(-1, 1), epochs=50, batch_size=1, verbose=2)

# Make predictions on the test data
predictions = model.predict(test_df['Daily Return'].values.reshape(-1, 1))

# Evaluate the performance of the model
mse = mean_squared_error(test_df['Daily Return'], predictions)
print('MSE:', mse)