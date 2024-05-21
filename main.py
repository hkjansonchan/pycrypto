import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential # type: ignore
from keras.layers import Dense, LSTM, Dropout # type: ignore
import discord

TOKEN = ""

# Run fetch.py
try:
    os.system("fetch.py")
except Exception as e:
    print(f"Error: {e}")

# Load the data
data = pd.read_csv("data.csv")

# Preprocess the data
data["date"] = pd.to_datetime(data["date"])
data = data.set_index("date")
data = data.drop_duplicates()
data = data.resample("15T").interpolate()
data = data[["open", "high", "low", "close", "volume"]]

# Scale the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Prepare the data for the LSTM model
X_train = []
y_train = []
for i in range(60, len(scaled_data)):
    X_train.append(scaled_data[i - 60 : i, :])
    y_train.append(scaled_data[i, 3])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 5))

# Build the LSTM model
input_layer = Input(shape=(X_train.shape[1], 5))
lstm_layer1 = LSTM(units=50, return_sequences=True)(input_layer)
lstm_layer2 = LSTM(units=50)(lstm_layer1)
output_layer = Dense(1)(lstm_layer2)
model = Sequential([input_layer, lstm_layer1, lstm_layer2, output_layer])

# Compile the model
model.compile(loss="mean_squared_error", optimizer="adam")

# Train the model
model.fit(X_train, y_train, epochs=1, batch_size=1, verbose=2)

# Prepare the data for prediction
test_data = scaled_data[training_data_len - 60 :, :]
X_test = []
for i in range(60, len(test_data)):
    X_test.append(test_data[i - 60 : i, :])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 5))

# Make predictions
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# Determine if the future several hours are bullish, bearish, or sideways
future_predictions = []
for i in range(len(predictions)):
    if predictions[i] > data["close"][i]:
        future_predictions.append("Bullish")
    elif predictions[i] < data["close"][i]:
        future_predictions.append("Bearish")
    else:
        future_predictions.append("Sideways")

client = discord.Client()


@client.event
async def on_ready():  #  Called when internal cache is loaded

    channel = client.get_channel("1226724862240886816")  #  Gets channel from internal cache
    await channel.send(future_predictions)  #  Sends message to channel


client.run(TOKEN)  # Starts up the bot
