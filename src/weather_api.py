import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    return {
        "temperature": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "rainfall": response.get("rain", {}).get("1h", 0)
    }