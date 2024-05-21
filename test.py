import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from keras.models import Sequential  # type: ignore
from keras.layers import Dense, LSTM, Dropout  # type: ignore
from sklearn.preprocessing import StandardScaler
from keras.callbacks import EarlyStopping, ReduceLROnPlateau  # type: ignore
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


# Load the data from the CSV file
df = pd.read_csv("data.py")
df["Trend"] = np.where(df["Close"].shift(-1) > df["Close"], "Up", "Down")

# Preprocess the data:
# Use only the relevant columns: 'Open', 'High', 'Low', 'Close', 'Volume' and drop the rest
# Use the StandardScaler to transform the features data so that they have a mean of 0 and a standard deviation of 1
# Use the OneHotEncoder class on the target variable: 'Trend'

train_preprocess = ColumnTransformer(
    transformers=[
        ("numerical", StandardScaler(), df.drop(columns=["Date", "Trend"], axis=1)),
        ("categorical", OneHotEncoder(), ["Trend"]),
    ],
)

# Prepare the data for training:
#  - Create time steps of 15 minutes as our input sequences
#  - Use one-hot-encoding (or dummy variables) as our output sequences
y = df["Trend"]
X = train_preprocess.fit_transform(df.drop("Trend", axis=1))
X = X.reshape((X.shape[0] - 15, 15, X.shape[1]))
y = y[15:]

# Define the LSTM model. Here the model includes dropout layers and the ReLU activation function
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=100))
model.add(Dropout(0.2))
model.add(Dense(units=3, activation="softmax"))

# Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Use the EarlyStopping callback to monitor the validation loss and stop training if it does not improve for 5 consecutive epochs
# Use the ReduceLROnPlateau callback to reduce the learning rate if the validation loss does not improve for 3 consecutive epochs
es = EarlyStopping(patience=5)
lr = ReduceLROnPlateau(patience=3)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train the model
model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[es, lr],
)

# Evaluate the model's performance
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1] * 100))

# Generate predictions for future trends
y_pred = model.predict(X_test)
y_pred_class = np.argmax(y_pred, axis=1)

# Generate and plot predictions over the full dataset
y_hat = model.predict(X)
y_hat_class = np.argmax(y_hat, axis=1)
df["Predicted Trend"] = y_hat_class
plt.figure(figsize=(12, 6), label="Predicted Trend")
plt.legend()
plt.show()
