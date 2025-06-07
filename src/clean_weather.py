import os
import json
import pandas as pd

# Folder where raw JSON files are stored
RAW_DIR = "data/raw"
CLEAN_FILE = "data/clean_weather.csv"

def clean_weather():
    all_data = []

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RAW_DIR, filename)

            with open(filepath, "r") as f:
                data = json.load(f)

                record = {
                    "city": data.get("name"),
                    "datetime": pd.to_datetime(data.get("dt"), unit='s'),
                    "temperature_C": data["main"]["temp"],
                    "humidity_percent": data["main"]["humidity"],
                    "weather_main": data["weather"][0]["main"],
                    "weather_description": data["weather"][0]["description"]
                }

                all_data.append(record)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_data)
    df.to_csv(CLEAN_FILE, index=False)
    print(f"Cleaned data saved to {CLEAN_FILE}")

if __name__ == "__main__":
    clean_weather()
