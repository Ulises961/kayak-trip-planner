from Resources.sea_resource import SEA_ENDPOINT
import json
from datetime import date, datetime

def test_insert_sea(app):
    sea = {
        "itinerary_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":None,
        "day_number": 1,
        "sea_states": [],
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }

    response = app.post(SEA_ENDPOINT, json=sea)
    assert response.status_code == 201

def test_delete_sea(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.delete(f"{SEA_ENDPOINT}?day_number=1&itinerary_id=1&date={day_date}")
    assert response.status_code == 200

def test_update_sea(app):
    sea = {
        "itinerary_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":"Crescent",
        "day_number": 1,
        "sea_states": [],
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }
    response = app.put(SEA_ENDPOINT, json=sea)
    
    assert json.loads(response.data)['moon_phase'] == "Crescent"
    assert response.status_code == 201


def test_get_sea(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.get(f"{SEA_ENDPOINT}?day_number=1&itinerary_id=1&date={day_date}")
    assert json.loads(response.data) == {
        "itinerary_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":"Crescent",
        "day_number": 1,
        "sea_states": [],
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }
    assert response.status_code == 200

