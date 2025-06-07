import pandas as pd

# Load cleaned weather data
df = pd.read_csv("data/clean_weather.csv")

# Convert datetime column to datetime object
df["datetime"] = pd.to_datetime(df["datetime"])

# Sort data by datetime (oldest to newest)
df = df.sort_values("datetime")

# Convert datetime to UNIX timestamp for regression
df["timestamp"] = df["datetime"].astype(int) / 10**9

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Features and target
X = df[["timestamp"]]
y = df["temperature_C"]

# Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Measure accuracy using Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f" Mean Squared Error: {mse:.2f}")

import numpy as np

# Predict temperature for 1 hour after the last timestamp
next_time = X["timestamp"].max() + 3600  # add 1 hour in seconds

# Fix the column name warning using DataFrame
next_temp = model.predict(pd.DataFrame(np.array([[next_time]]), columns=["timestamp"]))

# Output the prediction
print(f" Predicted temperature 1 hour later: {next_temp[0]:.2f}°C")

# Save to a CSV for visualization use
with open("data/prediction_output.csv", "w") as f:
    f.write("Predicted_Temperature\n")
    f.write(f"{next_temp[0]:.2f}")

