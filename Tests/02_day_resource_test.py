from Resources.day_resource import DAY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from datetime import date, datetime
from Schemas.day_schema import DaySchema
import json

def test_insert_itinerary_with_day(app):
    daysList = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points": [],
        }
    ]
    itinerary = {
        "days": daysList,
        "trip_id": 1
    }
    response = app.post(ITINERARY_ENDPOINT, json=itinerary)
    assert response.status_code == 201


def test_insert_weather_to_day(app):
    weather = {
        "weather_states": [],
        "day_id": 1,
        "model": "ICON"
    }

    day = {
        "id": 1,
        "weather": weather
    }
    response = app.put(DAY_ENDPOINT, json=day)
    assert response.status_code == 201


def test_insert_sea_to_day(app):
    sea = {
        "sea_states": [],
        "day_id": 1,
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "high_tide": datetime.now().time().strftime('%H:%M'),
    }

    day = {
        "id": 1,
        "itinerary_id":1,
        "sea": sea
    }
    response = app.put(DAY_ENDPOINT, json=day)
    assert response.status_code == 201


def test_get_day_by_key(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.get(
        f"{DAY_ENDPOINT}?itinerary_id=1&day_number=1&date={day_date}")
    assert response.status_code == 200

def test_get_day_by_id(app):
    response = app.get(
        f"{DAY_ENDPOINT}/1")
    assert response.status_code == 200

def test_get_all_days(app):
    response = app.get(
        f"{DAY_ENDPOINT}")
    assert response.status_code == 200
    assert len(json.loads(response.data)) == 1

def test_delete_day_by_key(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.delete(
        f"{DAY_ENDPOINT}?itinerary_id=1&day_number=1&date={day_date}")
    assert response.status_code == 200

def test_update_day(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    sea = None
    updated_day = {'id':1,'date':day_date,'itinerary_id':1,'day_number':1, 'sea':sea} 
    response = app.put(f"{DAY_ENDPOINT}", json=updated_day)
    assert json.loads(response.data)['sea'] == sea
    assert response.status_code == 201

def test_delete_day_by_id(app):
    response = app.delete(
        f"{DAY_ENDPOINT}/1")
    assert response.status_code == 200

def test_reinsert_day(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    new_day = {'id':1,'date':day_date,'itinerary_id':1,'day_number':1} 
    response = app.post(f"{DAY_ENDPOINT}", json=new_day)

    assert response.status_code == 201
