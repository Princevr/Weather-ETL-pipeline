import pandas as pd
import sqlite3
import os

# Load cleaned data
df = pd.read_csv("data/clean_weather.csv")

# Create /data/db folder if it doesn't exist
os.makedirs("data/db", exist_ok=True)

# Connect to SQLite database (creates file if not exist)
conn = sqlite3.connect("data/db/weather_data.db")
cursor = conn.cursor()

# Optional: Drop table if re-running script
cursor.execute("DROP TABLE IF EXISTS weather")

# Create table
cursor.execute("""
CREATE TABLE weather (
    city TEXT,
    datetime TEXT,
    temperature_C REAL,
    humidity_percent REAL,
    weather_main TEXT,
    weather_description TEXT
)
""")

# Insert data from DataFrame
df.to_sql("weather", conn, if_exists="append", index=False)

conn.commit()
conn.close()
print(" Cleaned data successfully stored in SQLite database.")
