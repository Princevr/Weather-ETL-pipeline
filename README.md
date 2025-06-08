
# 🌦️ Weather ETL & Forecasting: OpenWeatherMap to SQLite & Power BI

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using Python and SQLite for analyzing weather conditions across multiple cities. Real-time weather data is collected from the OpenWeatherMap API, processed, stored, and visualized using Power BI. Additionally, a machine learning model is used to forecast future temperatures.

---

## 📝 Overview

This repository showcases an end-to-end ETL + ML + Visualization pipeline built with Python and Power BI. It collects real-time weather data for multiple cities, transforms it using pandas, stores the data into SQLite, and enables automated execution using Task Scheduler. The output is visualized through Power BI dashboards, with forecasted temperature data included.

This project highlights practical data engineering skills with:

- ✅ Automated data pipeline
- ✅ Multi-city real-time weather tracking
- ✅ Temperature forecasting with machine learning
- ✅ Visual insights through Power BI

---

## 🌍 About the Data

- **Source**: [OpenWeatherMap API](https://openweathermap.org/api)
- **Data Format**: JSON (converted to CSV)
- **Fields Used**: temperature (°C), humidity (%), weather condition, datetime, city
- **Storage**: Cleaned data stored as CSV + SQLite

---

## 📈 Key Concepts

- **Data Source**: OpenWeatherMap API
- **Storage**: SQLite database and CSV
- **ML Forecasting**: Linear regression to predict next hour's temperature
- **Automation**: Task Scheduler (Windows) 
- **Email Alerts**: Email notifications are sent on success or failure of ETL using SMTP (Gmail App Password)  
- **Logging**: ETL runs and errors are written to `etl_log.txt`  

---

## 🔄 ETL Pipeline Flow

### ?? Extraction

```python
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["Surat", "Mumbai", "Delhi"]
```

Each city's weather is fetched in real-time and saved as:

```
data/raw/weather_CITYNAME_TIMESTAMP.json
```

---

### 🧼 Transformation

```python
# Raw JSON to clean CSV
# Extract: temperature, humidity, weather type, datetime, city
df_cleaned.to_csv("data/clean_weather.csv", index=False)
```

---

### 🗃️ Loading

```python
# Load cleaned CSV to SQLite
conn = sqlite3.connect("data/db/weather_data.db")
df_cleaned.to_sql("weather", conn, if_exists="append", index=False)
```

---

## 🧠 Machine Learning

| Feature         | Value                          |
|----------------|---------------------------------|
| Model           | Linear Regression               |
| Input           | UNIX timestamp                  |
| Output          | Temperature prediction (°C)     |
| Output File     | `data/prediction_output.csv`    |

---

## 📊 Power BI Dashboard Visuals

- Temperature and Predicted Temperature Over Time (Line chart)
- Average Temperature by City (Map)
- Humidity vs Temperature Colored by Weather Type (scatter chart)
- Average Temperature by Weather Condition (Clustered bar chart)
- Average of Prediction_temperature (Gauge)


Dashboard File: `weather_dashboard.pbix`

---

## ⚙️ How to Run the Project

Follow these steps to fetch, clean, store, and predict weather data:

### 🔹 Step 1: Set Up Environment

```bash
# Clone the repository (if applicable)
git clone https://github.com/yourusername/weather-etl.git
cd weather-etl

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # for Windows
# or
source venv/bin/activate  # for Mac/Linux

# Install required packages
pip install -r requirements.txt
```

### 🔹 Step 2: Configure Environment Variables

Create a `.env` file in the project root with the following content:

```ini
OPENWEATHER_API_KEY=your_api_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
```

### 🔹 Step 3: Fetch Weather Data (Extract)

```bash
python src/fetch_weather.py
```

This fetches weather data for multiple cities and saves it in `data/raw/` as JSON files.

### 🔹 Step 4: Clean Weather Data (Transform)

```bash
python src/clean_weather.py
```

- Reads the raw JSON files
- Extracts relevant weather data
- Saves it as `data/clean_weather.csv`

### 🔹 Step 5: Store Clean Data to SQLite (Load)

```bash
python src/store_to_sqlite.py
```

- Loads the cleaned CSV into `data/db/weather_data.db`

### 🔹 Step 6: Run Full ETL Pipeline with Logging + Email

```bash
python src/run_etl.py
```

- Runs all 3 steps (fetch, clean, store)
- Sends email notification on success/failure
- Logs the run in `etl_log.txt`

### 🔹 Step 7: Run Machine Learning Prediction

```bash
python src/predict_temperature.py
```

- Trains a Linear Regression model on historical weather data
- Predicts next-hour temperature
- Saves result to `data/prediction_output.csv`

### 🔹 Step 8: Open and Refresh Power BI Dashboard

- Open `weather_dashboard.pbix` in Power BI Desktop
- Refresh the connected datasets: `clean_weather.csv` and `prediction_output.csv`
- Explore charts, filters, and ML forecasts

## 📤 Final Deliverables

- `README.md`
- Python scripts (`src/`)
- SQLite database (optional)
- Power BI dashboard
- ML prediction output
- Screenshots of dashboard
- `.env` (locally only)
- `etl_log.txt`

---

## 🌟 Author Notes

This project was completed as part of the MADSC301 Business Intelligence final assessment using real-time data, forecasting, automation, and BI visualization techniques.

