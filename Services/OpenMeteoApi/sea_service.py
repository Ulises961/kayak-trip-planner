import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://marine-api.open-meteo.com/v1/marine"
params = {
	"latitude": 50.8284,
	"longitude": -0.1395,
	"hourly": "wave_height",
	"models": "best_match",
	"current": ["ocean_current_direction", "ocean_current_velocity", "sea_level_height_msl", "wave_height", "wave_direction", "wave_period", "wind_wave_height", "wind_wave_direction", "wind_wave_period", "swell_wave_height", "swell_wave_direction", "swell_wave_period"],
	"minutely_15": ["ocean_current_velocity", "ocean_current_direction", "sea_level_height_msl"],
	"forecast_hours": 1,
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_ocean_current_direction = current.Variables(0).Value()
current_ocean_current_velocity = current.Variables(1).Value()
current_sea_level_height_msl = current.Variables(2).Value()
current_wave_height = current.Variables(3).Value()
current_wave_direction = current.Variables(4).Value()
current_wave_period = current.Variables(5).Value()
current_wind_wave_height = current.Variables(6).Value()
current_wind_wave_direction = current.Variables(7).Value()
current_wind_wave_period = current.Variables(8).Value()
current_swell_wave_height = current.Variables(9).Value()
current_swell_wave_direction = current.Variables(10).Value()
current_swell_wave_period = current.Variables(11).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current ocean_current_direction: {current_ocean_current_direction}")
print(f"Current ocean_current_velocity: {current_ocean_current_velocity}")
print(f"Current sea_level_height_msl: {current_sea_level_height_msl}")
print(f"Current wave_height: {current_wave_height}")
print(f"Current wave_direction: {current_wave_direction}")
print(f"Current wave_period: {current_wave_period}")
print(f"Current wind_wave_height: {current_wind_wave_height}")
print(f"Current wind_wave_direction: {current_wind_wave_direction}")
print(f"Current wind_wave_period: {current_wind_wave_period}")
print(f"Current swell_wave_height: {current_swell_wave_height}")
print(f"Current swell_wave_direction: {current_swell_wave_direction}")
print(f"Current swell_wave_period: {current_swell_wave_period}")

# Process minutely_15 data. The order of variables needs to be the same as requested.
minutely_15 = response.Minutely15()
minutely_15_ocean_current_velocity = minutely_15.Variables(0).ValuesAsNumpy()
minutely_15_ocean_current_direction = minutely_15.Variables(1).ValuesAsNumpy()
minutely_15_sea_level_height_msl = minutely_15.Variables(2).ValuesAsNumpy()

minutely_15_data = {"date": pd.date_range(
	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = minutely_15.Interval()),
	inclusive = "left"
)}

minutely_15_data["ocean_current_velocity"] = minutely_15_ocean_current_velocity
minutely_15_data["ocean_current_direction"] = minutely_15_ocean_current_direction
minutely_15_data["sea_level_height_msl"] = minutely_15_sea_level_height_msl

minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
print("\nMinutely15 data\n", minutely_15_dataframe)

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["wave_height"] = hourly_wave_height

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)
