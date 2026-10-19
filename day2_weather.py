import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Nairobi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    print(f"Weather in {city}: {temp}C, {description}, humidity {humidity}%")

elif response.status_code == 401:
    print("API key is invalid or not yet active. Check your .env file.")