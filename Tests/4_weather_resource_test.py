from Resources.weather_resource import WEATHER_ENDPOINT
import json
from datetime import date, datetime

def test_insert_weather(app):
    weather = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "model":"ICON",
        "weather_states": []
    }

    response = app.post(WEATHER_ENDPOINT, json=weather)
    assert response.status_code == 201

def test_delete_weather(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.delete(f"{WEATHER_ENDPOINT}?day_number=1&itinerary_id=1&date={day_date}")
    assert response.status_code == 200

def test_update_weather(app):
    weather = {
        "itinerary_id": 1,
        "model":"GFS",
        "day_number": 1,
        "weather_states": [],
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }
    response = app.put(WEATHER_ENDPOINT, json=weather)
    
    assert json.loads(response.data)['model'] == "GFS"
    assert response.status_code == 200


def test_get_weather(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.get(f"{WEATHER_ENDPOINT}?day_number=1&itinerary_id=1&date={day_date}")
    assert json.loads(response.data) == {
        "itinerary_id": 1,
        "model":"GFS",
        "day_number": 1,
        "weather_states": [],
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }
    assert response.status_code == 200

