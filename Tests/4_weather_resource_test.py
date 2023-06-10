from Resources.weather_resource import WEATHER_ENDPOINT
import json
from datetime import date, datetime

def test_insert_weather(app):
    weather = {
        "day_id": 1,
        "model":"ICON",
        "weather_states": []
    }

    response = app.post(WEATHER_ENDPOINT, json=weather)
    assert response.status_code == 201

def test_delete_weather(app):
    response = app.delete(f"{WEATHER_ENDPOINT}/1")
    assert response.status_code == 200

def test_update_weather(app):
    weather = {
        "day_id": 1,
        "model":"GFS",
        "weather_states": [],
    }
    response = app.put(WEATHER_ENDPOINT, json=weather)   
    assert json.loads(response.data)['model'] == "GFS"
    assert response.status_code == 200


def test_get_weather(app):
    response = app.get(f"{WEATHER_ENDPOINT}/1")
    assert json.loads(response.data) == {
        "day_id": 1,
        "model":"GFS",
        "weather_states": [],
    }
    assert response.status_code == 200

