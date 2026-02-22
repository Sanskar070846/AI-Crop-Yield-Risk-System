import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        raise ValueError("City not found")

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall