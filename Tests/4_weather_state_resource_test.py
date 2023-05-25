from Resources.weather_state_resource import WEATHER_STATE_ENDPOINT
import json
from datetime import date,datetime

def test_insert_weather_state(app):
    weather = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time":datetime.now().time().strftime("%H:%M:%S"),
        "temperature": 30,
        "wind_direction": 262,
        "wind_force":10        
    }

    response = app.post(WEATHER_STATE_ENDPOINT, json=weather)
    assert response.status_code == 201
