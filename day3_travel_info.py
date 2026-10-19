
"""
Travel Weather & Country Information Tool

How to run:
1. Install dependencies: pip install requests python-dotenv
2. Add OPENWEATHER_API_KEY and REST_COUNTRIES_API_KEY
   to your .env file.
3. Run: python day3_travel_info.py

The tool fetches live weather and country information,
combines the results, and saves them to a JSON file.
"""

import requests
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()


def get_weather(city):
    """Fetch current weather for a city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Error: OpenWeatherMap API key is missing.")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("The weather service took too long to respond.")
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(f"City '{city}' was not found. Check the spelling.")
        else:
            print("The weather service returned an error.")
    except requests.exceptions.RequestException:
        print("Could not connect to the weather service.")

    return None


def get_country_info(country_code):
    """Fetch country information using its two-letter country code."""
    api_key = os.getenv("REST_COUNTRIES_API_KEY")

    if not api_key:
        print("Error: REST Countries API key is missing.")
        return None

    url = (
        "https://api.restcountries.com/countries/v5/"
        f"codes.alpha_2/{country_code}"
    )

    headers = {"Authorization": f"Bearer {api_key}"}

    params = {
        "response_fields": (
            "names.common,codes.alpha_2,region,"
            "population,currencies"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
        response.raise_for_status()

        payload = response.json()
        countries = payload.get("data", {}).get("objects", [])

        if countries:
            return countries[0]

        print("No country record was returned.")

    except requests.exceptions.RequestException:
        print("Could not retrieve country information.")
    except (ValueError, AttributeError):
        print("The country service returned unexpected data.")

    return None


def save_to_file(data, filename):
    """Save the combined report as readable JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        print(f"\nReport saved to: {filename}")
        return True

    except OSError:
        print("Could not save the JSON file.")
        return False


def run_tool():
    """Run the travel information tool."""
    print("\nTRAVEL WEATHER & COUNTRY INFORMATION")
    print("=" * 38)

    city = input("Enter a city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    print(f"\nFetching live information for {city}...")

    weather_data = get_weather(city)

    if weather_data is None:
        print("The report could not be completed.")
        return

    country_code = weather_data.get("sys", {}).get("country", "")
    country_data = get_country_info(country_code) if country_code else None

    # Extract the weather details we want to display and save.
    weather_report = {
        "city": weather_data.get("name", city),
        "country_code": country_code,
        "temperature_c": weather_data.get("main", {}).get("temp"),
        "condition": (
            weather_data.get("weather", [{}])[0].get("description", "Unknown")
        ),
        "humidity_percent": weather_data.get("main", {}).get("humidity"),
        "wind_speed_m_s": weather_data.get("wind", {}).get("speed")
    }

    country_report = None

    if country_data:
        currency_data = country_data.get("currencies", [])
        currencies = []

        if isinstance(currency_data, list):
            for currency in currency_data:
                if isinstance(currency, dict):
                    currencies.append(
                        currency.get("name")
                        or currency.get("code", "Unknown")
                    )
                else:
                    currencies.append(str(currency))

        elif isinstance(currency_data, dict):
            for code, details in currency_data.items():
                if isinstance(details, dict):
                    currencies.append(details.get("name", code))
                else:
                    currencies.append(code)

        country_report = {
            "name": country_data.get("names", {}).get(
                "common", country_code
            ),
            "region": country_data.get("region", "Unknown"),
            "population": country_data.get("population"),
            "currencies": currencies
        }

    # Combine both API results into one report.
    combined_report = {
        "weather": weather_report,
        "country": country_report
    }

    # Display a friendly report.
    print("\n" + "=" * 38)
    print(f"TRAVEL REPORT: {weather_report['city']}")
    print("=" * 38)
    print(f"Country code : {country_code}")
    print(f"Temperature  : {weather_report['temperature_c']} °C")
    print(f"Condition    : {weather_report['condition'].title()}")
    print(f"Humidity     : {weather_report['humidity_percent']}%")
    print(f"Wind speed   : {weather_report['wind_speed_m_s']} m/s")

    if country_report:
        population = country_report["population"]
        population_text = (
            f"{population:,}" if isinstance(population, int) else "Unknown"
        )
        currency_text = ", ".join(country_report["currencies"]) or "Unknown"

        print("\nCOUNTRY INFORMATION")
        print(f"Country      : {country_report['name']}")
        print(f"Region       : {country_report['region']}")
        print(f"Population   : {population_text}")
        print(f"Currency     : {currency_text}")
    else:
        print("\nCountry details are currently unavailable.")

    safe_city = re.sub(r"[^a-zA-Z0-9_-]+", "_", city.lower()).strip("_")
    filename = f"{safe_city or 'travel'}_travel_report.json"

    save_to_file(combined_report, filename)


if __name__ == "__main__":
    run_tool()
