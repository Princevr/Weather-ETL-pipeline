import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load the API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# List of cities to fetch weather for
CITIES = ["Paris", "London", "Rome", "Barcelona", "Amsterdam", "Venice", "Prague", "Istanbul", "Vienna", "Athens", "Tokyo", "Beijing", "Dubai", "Mumbai", "Seoul", "Bangkok", "Singapore", "Hong Kong", "Jerusalem", "Shanghai", "New York City", "Los Angeles", "Toronto", "Mexico City", "Chicago", "Las Vegas", "Miami", "San Francisco", "Washington D.C.", "Vancouver", "Rio de Janeiro", "Buenos Aires", "Lima", "Santiago", "Bogotá", "Cairo", "Cape Town", "Marrakech", "Nairobi", "Lagos", "Sydney", "Melbourne"]

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city}")
        print("Temp:", data["main"]["temp"], "°C")
        print("Humidity:", data["main"]["humidity"], "%")

        # Create directory if it doesn't exist
        os.makedirs("data/raw", exist_ok=True)

        # Save the data to a file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/raw/weather_{city.lower()}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Saved to", filename)
    else:
        print(f"Error fetching data for {city}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    for city in CITIES:
        fetch_weather(city.strip())
