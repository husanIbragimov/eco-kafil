import json

import openmeteo_requests
import pandas as pd
import requests_cache
from rest_framework.response import Response
from rest_framework.views import APIView
from retry_requests import retry


class WeatherView(APIView):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.2647,
        "longitude": 69.2163,
        "daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min",
                  "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max",
                  "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum",
                  "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max",
                  "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
        "current": "temperature_2m",
        "timezone": "auto",
        "past_days": 1,
        "timeformat": "unixtime",
        "temporal_resolution": "hourly_6",
    }

    def get(self, request):
        openmeteo = openmeteo_requests.Client(session=self.retry_session)
        responses = openmeteo.weather_api(self.URL, params=self.params)
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process current data. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()

        print(f"\nCurrent time: {current.Time()}")
        print(f"Current temperature_2m: {current_temperature_2m}")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
        daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
        daily_sunrise = daily.Variables(4).ValuesInt64AsNumpy()
        daily_sunset = daily.Variables(5).ValuesInt64AsNumpy()
        daily_daylight_duration = daily.Variables(6).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(7).ValuesAsNumpy()
        daily_uv_index_max = daily.Variables(8).ValuesAsNumpy()
        daily_uv_index_clear_sky_max = daily.Variables(9).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(10).ValuesAsNumpy()
        daily_showers_sum = daily.Variables(11).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(12).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(13).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(14).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(15).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(16).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(17).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(18).ValuesAsNumpy()
        daily_shortwave_radiation_sum = daily.Variables(19).ValuesAsNumpy()
        daily_et0_fao_evapotranspiration = daily.Variables(20).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ), "temperature_2m_max": daily_temperature_2m_max,
            "temperature_2m_min": daily_temperature_2m_min,
            "apparent_temperature_max": daily_apparent_temperature_max,
            "apparent_temperature_min": daily_apparent_temperature_min,
            "sunrise": daily_sunrise,
            "sunset": daily_sunset,
            "daylight_duration": daily_daylight_duration,
            "sunshine_duration": daily_sunshine_duration,
            "uv_index_max": daily_uv_index_max,
            "uv_index_clear_sky_max": daily_uv_index_clear_sky_max,
            "rain_sum": daily_rain_sum,
            "showers_sum": daily_showers_sum,
            "snowfall_sum": daily_snowfall_sum,
            "precipitation_sum": daily_precipitation_sum,
            "precipitation_hours": daily_precipitation_hours,
            "precipitation_probability_max": daily_precipitation_probability_max,
            "wind_speed_10m_max": daily_wind_speed_10m_max,
            "wind_gusts_10m_max": daily_wind_gusts_10m_max,
            "wind_direction_10m_dominant": daily_wind_direction_10m_dominant,
            "shortwave_radiation_sum": daily_shortwave_radiation_sum,
            "et0_fao_evapotranspiration": daily_et0_fao_evapotranspiration
        }

        daily_dataframe = pd.DataFrame(data=daily_data)
        real_json = daily_dataframe.to_json(orient="records", date_format="iso")
        real_json = json.loads(real_json)

        return Response(real_json)
