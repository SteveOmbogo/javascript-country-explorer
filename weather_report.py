import os
import requests
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Get the API key securely
api_key = os.getenv("OPENWEATHER_API_KEY")

# Stop if the key is missing
if not api_key:
    print("Error: API key not found.")
    print("Check that your .env file exists and contains OPENWEATHER_API_KEY.")
    raise SystemExit(1)

# Choose the city
city = input("Enter a city (e.g., Nairobi): ").strip()


if not city:
    print("Error: City name cannot be empty.")
    raise SystemExit(1)

# Prepare the API request
url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}

try:
    # Send the request; timeout prevents waiting indefinitely
    response = requests.get(url, params=params, timeout=10)

    # Handle specific HTTP error codes
    if response.status_code == 401:
        print("Authentication error: Check your API key.")
    elif response.status_code == 404:
        print(f"City not found: {city}. Check the spelling.")
    elif response.status_code == 429:
        print("Rate limit reached. Please try again later.")
    elif response.status_code >= 500:
        print("Weather service is temporarily unavailable.")
    else:
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary
        data = response.json()

        # Extract the information we need
        location = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        # Display a clean weather report
        print("\n" + "=" * 35)
        print("       CURRENT WEATHER REPORT")
        print("=" * 35)
        print(f"Location:     {location}, {country}")
        print(f"Conditions:   {description.title()}")
        print(f"Temperature:  {temperature:.1f} °C")
        print(f"Feels like:   {feels_like:.1f} °C")
        print(f"Humidity:     {humidity}%")
        print("=" * 35)

except requests.exceptions.Timeout:
    print("Connection timed out. Please try again.")

except requests.exceptions.ConnectionError:
    print("Network error. Check your internet connection.")

except requests.exceptions.HTTPError as error:
    print(f"HTTP error: {error}")

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")

except (KeyError, IndexError, ValueError) as error:
    print(f"Could not process the weather data: {error}")
