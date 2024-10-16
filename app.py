from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")  # Replace with your OpenWeatherMap API key
API_URL = 'https://api.openweathermap.org/data/2.5/weather'


@app.get("/weather")
def fetch_weather(location: str):
    url = f"{API_URL}?q={location}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        }

    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

# To run the app, use Uvicorn:
# uvicorn <filename_without_extension>:app --reload
