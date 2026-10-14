
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# API endpoint for Kenya (KE is Kenya's country code)
url = "https://countries.dev/alpha/KE"

try:
    # Send a request to the API
    request = Request(url, headers={"User-Agent": "PythonCountryReport/1.0"})

    with urlopen(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    # Extract information from the dictionary
    name = data.get("name", "Not available")
    capital = data.get("capital", "Not available")
    region = data.get("region", "Not available")
    population = data.get("population", 0)

    # Extract currency information
    currencies = data.get("currencies", [])
    currency_names = [
        item.get("name", "Unknown")
        for item in currencies
    ]

    # Extract language information
    languages = data.get("languages", [])
    language_names = [
        item.get("name", "Unknown")
        for item in languages
    ]

    # Display the report
    print("=" * 40)
    print("       COUNTRY INFORMATION REPORT")
    print("=" * 40)
    print(f"Country:       {name}")
    print(f"Capital:       {capital}")
    print(f"Region:        {region}")
    print(f"Population:    {population:,}")
    print("Currency:      " + (", ".join(currency_names) or "Not available"))
    print("Languages:     " + (", ".join(language_names) or "Not available"))
    print("=" * 40)
    print("Report generated successfully!")

except HTTPError as error:
    print(f"API request failed: HTTP {error.code}")

except URLError as error:
    print(f"Connection problem: {error.reason}")

except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
    print(f"Problem processing the API data: {error}")
