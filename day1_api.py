import requests
url="https://restcountries.com/v3.1/name/kenya"
response=requests.get(url)
print("Status code:",response.status_code)
print("Data recieved:",response.json())
import requests

url = "https://restcountries.com/v3.1/name/ghana"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    country = data[0]

    name = country["name"]["common"]
    capital = country["capital"][0]
    population = country["population"]
    currency = list(country["currencies"].keys())[0]

    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population:,}")
    print(f"Currency: {currency}")
else:
    print("Request failed. Status:", response.status_code)