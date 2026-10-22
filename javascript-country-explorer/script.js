

const form = document.getElementById("search-form");
const cityInput = document.getElementById("city-input");
const searchButton = document.getElementById("search-button");
const status = document.getElementById("status");
const result = document.getElementById("weather-result");

// Run when the user submits the search form.
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const city = cityInput.value.trim();

    if (!city) {
        status.textContent = "Please enter a city name.";
        status.className = "error";
        result.replaceChildren();
        return;
    }

    // Display the loading state.
    status.textContent = "Loading...";
    status.className = "";
    result.replaceChildren();
    searchButton.disabled = true;

    try {
        // Step 1: Find the city's coordinates.
        const locationUrl =
            `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;

        const locationResponse = await fetch(locationUrl);

        if (!locationResponse.ok) {
            throw new Error("Unable to find the city. Please try again.");
        }

        const locationData = await locationResponse.json();

        if (!locationData.results || locationData.results.length === 0) {
            throw new Error("City not found. Check the spelling and try again.");
        }

        const place = locationData.results[0];

        // Step 2: Fetch weather using the coordinates.
        const weatherUrl =
            `https://api.open-meteo.com/v1/forecast?latitude=${place.latitude}&longitude=${place.longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m`;

        const weatherResponse = await fetch(weatherUrl);

        if (!weatherResponse.ok) {
            throw new Error("Unable to retrieve weather data.");
        }

        const weatherData = await weatherResponse.json();
        const weather = weatherData.current;

        if (!weather) {
            throw new Error("No current weather data was returned.");
        }

        // Create the weather card.
        const card = document.createElement("article");
        card.className = "weather-card";

        const heading = document.createElement("h2");
        heading.textContent =
            `${place.name}, ${place.country || ""}`;

        const temperature = document.createElement("p");
        temperature.className = "temperature";
        temperature.textContent =
            `${weather.temperature_2m} °C`;

        const details = [
            ["Humidity", `${weather.relative_humidity_2m}%`],
            ["Wind speed", `${weather.wind_speed_10m} km/h`],
            ["Coordinates", `${place.latitude}, ${place.longitude}`]
        ];

        card.append(heading, temperature);

        details.forEach(([label, value]) => {
            const row = document.createElement("p");
            row.className = "detail";

            const strong = document.createElement("strong");
            strong.textContent = `${label}: `;

            row.append(strong, document.createTextNode(value));
            card.append(row);
        });

        result.append(card);

        status.textContent = "Weather data loaded successfully.";

    } catch (error) {
        status.textContent = `Error: ${error.message}`;
        status.className = "error";

    } finally {
        // Re-enable the button even if an error occurs.
        searchButton.disabled = false;
    }
});

// Automatically fetch Nairobi's weather on page load.
form.requestSubmit();
