Weather ETL Pipeline – Code Overview

This document presents a complete walkthrough of the code inside the `src/` folder for the Weather ETL & ML project, organized in a step-by-step ETL + ML format.

---

## Extraction

```python
# src/fetch_weather.py

import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["Surat", "Mumbai", "Delhi"]

def fetch_weather():
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            filename = f"data/raw/weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Weather data for {city} saved to {filename}")
        else:
            print(f"❌ Failed to fetch data for {city} — Status code:", response.status_code)

if __name__ == "__main__":
    fetch_weather()
```

---

##  Transformation

```python
# src/clean_weather.py

import json
import os
import pandas as pd
from glob import glob

raw_files = glob("data/raw/*.json")
data = []

for file in raw_files:
    with open(file, "r") as f:
        weather = json.load(f)
        city = weather["name"]
        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        condition = weather["weather"][0]["main"]
        timestamp = weather["dt"]
        data.append({
            "city": city,
            "temperature": temp,
            "humidity": humidity,
            "weather_main": condition,
            "timestamp": timestamp
        })

df = pd.DataFrame(data)
df.to_csv("data/clean_weather.csv", index=False)
print("✅ Clean weather data saved to data/clean_weather.csv")
```

---

##  Loading

```python
# src/store_to_sqlite.py

import pandas as pd
import sqlite3
import os

db_path = "data/db/weather_data.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

df = pd.read_csv("data/clean_weather.csv")
conn = sqlite3.connect(db_path)
df.to_sql("weather", conn, if_exists="append", index=False)
conn.close()

print("✅ Data successfully inserted into SQLite DB.")
```

---

##  ML Prediction

```python
# src/predict_temperature.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/clean_weather.csv")
df = df.sort_values(by="timestamp")
X = df[["timestamp"]]
y = df["temperature"]

model = LinearRegression()
model.fit(X, y)

next_timestamp = [[df["timestamp"].max() + 3600]]
predicted_temp = model.predict(next_timestamp)

output = pd.DataFrame({
    "next_timestamp": [next_timestamp[0][0]],
    "predicted_temperature": [predicted_temp[0]]
})
output.to_csv("data/prediction_output.csv", index=False)

print("✅ Predicted temperature:", predicted_temp[0])
```

---

##  Logging

```python
# Inside src/run_etl.py

import logging
from datetime import datetime
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"etl_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL process started")
```

---

##  Scheduling (Python alternative to Task Scheduler)

```python
# scheduling.py

import schedule
import time
from run_etl import run_etl

schedule.every().day.at("08:00").do(run_etl)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

##  Email Alerts

```python
# src/send_email.py

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = os.getenv("EMAIL_RECEIVER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
```

---

##  Summary

Each Python file contributes to the automation and orchestration of the weather ETL process and prediction model:
- Data is **fetched**, **cleaned**, and **stored**
- Predictions are made and **visualized** in Power BI
- Execution is **automated** and monitored through **email alerts** and logs

This code overview is designed to help understand the flow of data and logic across the ETL + ML pipeline.
