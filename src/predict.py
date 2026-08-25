import datetime
from pathlib import Path
import joblib
import pandas as pd
import requests

# Resolve path safely so it works from anywhere
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "weather_model.joblib"

# 1. Load trained model pipeline
model = joblib.load(MODEL_PATH)

FEATURES = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "cloud_cover_mean",
    "pressure_msl_mean",
    "wind_speed_10m_max",
    "wind_direction_10m_dominant",
    "sunshine_duration",
    "month",
    "day_of_week"
]

def get_coordinates(city_name: str):
    """Converts a city name into latitude, longitude, and timezone."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(geo_url, params={"name": city_name, "count": 1}).json()
    
    if not geo_res.get("results"):
        raise ValueError(f"City '{city_name}' not found. Please check spelling.")
    
    top_result = geo_res["results"][0]
    return {
        "name": top_result["name"],
        "country": top_result.get("country", ""),
        "latitude": top_result["latitude"],
        "longitude": top_result["longitude"],
        "timezone": top_result.get("timezone", "auto")
    }

def predict_by_city(city_name: str):
    """
    Takes a city name, fetches live today's weather metrics,
    and predicts whether it will rain tomorrow.
    """
    # 1. Get location coordinates
    location = get_coordinates(city_name)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # 2. Fetch today's weather metrics from Open-Meteo Forecast API
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "cloud_cover_mean",
            "pressure_msl_mean",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
            "sunshine_duration"
        ],
        "timezone": location["timezone"],
        "start_date": today_str,
        "end_date": today_str
    }
    
    res = requests.get(weather_url, params=params).json()
    daily_data = res["daily"]
    today = datetime.datetime.strptime(today_str, "%Y-%m-%d")
    
    # 3. Assemble the exact 12 features expected by the model
    input_dict = {
        "temperature_2m_mean": daily_data["temperature_2m_mean"][0],
        "temperature_2m_max": daily_data["temperature_2m_max"][0],
        "temperature_2m_min": daily_data["temperature_2m_min"][0],
        "relative_humidity_2m_mean": daily_data["relative_humidity_2m_mean"][0],
        "precipitation_sum": daily_data["precipitation_sum"][0],
        "cloud_cover_mean": daily_data["cloud_cover_mean"][0],
        "pressure_msl_mean": daily_data["pressure_msl_mean"][0],
        "wind_speed_10m_max": daily_data["wind_speed_10m_max"][0],
        "wind_direction_10m_dominant": daily_data["wind_direction_10m_dominant"][0],
        "sunshine_duration": daily_data["sunshine_duration"][0],
        "month": today.month,
        "day_of_week": today.weekday()
    }
    
    input_df = pd.DataFrame([input_dict])[FEATURES]
    
    # 4. Predict
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])
    
    return {
        "city": f"{location['name']}, {location['country']}",
        "date": today_str,
        "rain_tomorrow": "YES" if prediction == 1 else "NO",
        "rain_probability": f"{probability * 100:.2f}%"
    }

if __name__ == "__main__":
    print("\n--- Running Live Predictions ---")
    print(predict_by_city("Chennai"))
    print(predict_by_city("Boston"))
    print("--------------------------------\n")