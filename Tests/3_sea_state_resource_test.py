from Resources.sea_state_resource import SEA_STATE_ENDPOINT
import json
from datetime import date, datetime


def test_insert_sea_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    sea = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "wave_height": 1.30,
        "wave_direction": 262,
        "swell_direction": 200,
        "swell_period": 10
    }

    response = app.post(SEA_STATE_ENDPOINT, json=sea)
    assert response.status_code == 201


def test_get_sea_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    response = app.get(
        f"{SEA_STATE_ENDPOINT}?date={date}&day_number=1&itinerary_id=1&time={time}")
    json.loads(response.data) == {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "wave_height": 1.30,
        "wave_direction": 262,
        "swell_direction": 200,
        "swell_period": 10
    }
    response.status_code == 200

def test_update_sea_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    sea_state = {
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "time": time,
        "wave_height": 1.30,
        "wave_direction": 200,
        "swell_direction": 200,
        "swell_period": 20
    }

    response = app.put(SEA_STATE_ENDPOINT, json= sea_state)
    json.loads(response.data)['wave_height'] == 1.30
    json.loads(response.data)['wave_direction'] == 200
    json.loads(response.data)['swell_direction'] == 200
    json.loads(response.data)['time'] == time
    response.status_code == 201

def test_delete_sea_state(app):
    time = datetime.strptime('20:25:00', '%H:%M:%S').time().strftime('%H:%M:%S')
    current_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    request = app.delete(f"{SEA_STATE_ENDPOINT}?day_numer=1&itinerary_id=1&date={current_date}&time={time}")
    request.status_code == 200