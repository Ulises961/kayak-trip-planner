from Resources.weather_state_resource import WEATHER_STATE_ENDPOINT
import json
from datetime import date, datetime


def test_insert_weather_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    weather = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "temperature": 30,
        "wind_direction": 262,
        "wind_force": 10
    }

    response = app.post(WEATHER_STATE_ENDPOINT, json=weather)
    assert response.status_code == 201


def test_get_weather_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    response = app.get(
        f"{WEATHER_STATE_ENDPOINT}?date={date}&day_number=1&itinerary_id=1&time={time}")
    json.loads(response.data) == {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "temperature": 30,
        "wind_direction": 262,
        "wind_force": 10
    }
    response.status_code == 200

def test_update_weather_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    weather_state = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "wind_direction" : 180,
        "wind_force" : 5
    }

    response = app.put(WEATHER_STATE_ENDPOINT, json= weather_state)
    json.loads(response.data)['wind_direction'] == 180
    json.loads(response.data)['wind_force'] == 5
    json.loads(response.data)['time'] == time
    response.status_code == 201

def test_delete_weather_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    current_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    request = app.delete(f"{WEATHER_STATE_ENDPOINT}?day_numer=1&itinerary_id=1&date={current_date}&time={time}")
    request.status_code == 200