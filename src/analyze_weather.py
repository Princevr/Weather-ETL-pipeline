import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned weather data
df = pd.read_csv("data/clean_weather.csv")

# Convert 'datetime' column to datetime format (if it's not already)
df["datetime"] = pd.to_datetime(df["datetime"])

# Sort by datetime (optional but useful)
df = df.sort_values("datetime")

# Set seaborn style
sns.set(style="darkgrid")

# 📈 Plot temperature over time
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="datetime", y="temperature_C", marker="o")
plt.title("Temperature Over Time")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 📉 Plot humidity over time
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="datetime", y="humidity_percent", marker="s", color="blue")
plt.title("Humidity Over Time")
plt.xlabel("Date/Time")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
