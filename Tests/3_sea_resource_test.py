from Resources.sea_resource import SEA_ENDPOINT
import json
from datetime import date, datetime

def test_insert_sea(app):
    sea = {
        "day_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":None,
        "sea_states": [],
    }

    response = app.post(SEA_ENDPOINT, json=sea)
    assert response.status_code == 201

def test_delete_sea_by_key(app):
    response = app.delete(f"{SEA_ENDPOINT}/1")
    assert response.status_code == 200


def test_update_sea(app):
    sea = {
        "day_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":"Crescent",
        "sea_states": [],
    }
    response = app.put(SEA_ENDPOINT, json=sea)
    
    assert json.loads(response.data)['moon_phase'] == "Crescent"
    assert response.status_code == 201


def test_get_sea(app):
    response = app.get(f"{SEA_ENDPOINT}/1")
    assert json.loads(response.data) == {
        "day_id": 1,
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "moon_phase":"Crescent",
        "sea_states": [],
    }
    assert response.status_code == 200

