import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# Add project root to sys.path so we can import from src/
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.predict import predict_by_city

app = FastAPI(
    title="Weather Rain Forecast ML API",
    description="Predicts if it will rain tomorrow for any city using live Open-Meteo weather data and classical ML.",
    version="1.0.0"
)

class WeatherForecastResponse(BaseModel):
    city: str
    date: str
    rain_tomorrow: str
    rain_probability: str

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Weather Forecasting ML API is running. Go to /docs for interactive Swagger UI."
    }

@app.get("/predict", response_model=WeatherForecastResponse)
def get_prediction(city: str = Query(..., description="Name of the city (e.g., Mumbai, Tokyo, London)")):
    try:
        result = predict_by_city(city)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
