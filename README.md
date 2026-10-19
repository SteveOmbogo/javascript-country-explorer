# Travel Weather & Country Information Tool

## Problem It Solves

Planning a trip involves checking the weather and learning basic information about the destination. This command-line tool combines live weather data with country information in one convenient report.

## Features

- Accepts a city name from the user.
- Retrieves current weather from the OpenWeatherMap API.
- Retrieves country information from the REST Countries API.
- Combines both results into a single JSON report.
- Displays readable information in the terminal.
- Handles common API and connection errors gracefully.

## Requirements

- Python 3
- An OpenWeatherMap API key
- A REST Countries API key

## Installation

1. Clone this repository or download the project.
2. Install dependencies:

   `pip install requests python-dotenv`

3. Create a `.env` file in the project folder and add your API keys:

   `OPENWEATHER_API_KEY=your_key_here`

   `REST_COUNTRIES_API_KEY=your_key_here`

4. Ensure `.env` is included in `.gitignore`.

## How to Run

Run the following command from the project directory:

`python day3_travel_info.py`

Enter a city name when prompted.

The program displays the results and saves a JSON report in the project directory.

## Technologies Used

- Python
- Requests
- python-dotenv
- OpenWeatherMap API
- REST Countries API
- JSON

## Learning Outcomes

This project demonstrates user input, HTTP requests, API integration, JSON processing, file handling, environment variables, and error handling.
