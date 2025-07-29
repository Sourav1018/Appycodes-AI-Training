import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from retry_requests import retry

# Setup Open-Meteo client with retry & caching
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def geocode_location(location: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}
    resp = requests.get(url, params=params)
    data = resp.json()

    if not data.get("results"):
        raise Exception(f"Location '{location}' not found")

    result = data["results"][0]
    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result["country"],
    }


def get_weather_by_location(location: str):
    geo = geocode_location(location)

    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "models": [
            "CMCC_CM2_VHR4",
            "FGOALS_f3_H",
            "HiRAM_SIT_HR",
            "MRI_AGCM3_2_S",
            "EC_Earth3P_HR",
            "MPI_ESM1_2_XR",
            "NICAM16_8S",
        ],
        "daily": "temperature_2m_max",
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max

    daily_dataframe = pd.DataFrame(data=daily_data)
    preview = daily_dataframe.to_dict(orient="records")

    # Fix serialization of pd.Timestamp
    for row in preview:
        row["date"] = row["date"].isoformat()

    return {
        "location": f"{geo['name']}, {geo['country']}",
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "weather_preview": preview,
        "elevation": response.Elevation(),
    }
