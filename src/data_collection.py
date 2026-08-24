import os
import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "daily": [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "rain_sum",
    "cloud_cover_mean",
    "pressure_msl_mean",
    "wind_speed_10m_max",
    "wind_direction_10m_dominant",
    "sunshine_duration"
],
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)

response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["daily"])



print(df.head())
print(df.shape)



os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/weather_raw.csv", index=False)

print("Data saved successfully!")