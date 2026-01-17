from http import HTTPStatus
from Resources.day_resource import DAY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from datetime import date, datetime
from Schemas.day_schema import DaySchema
import json

def test_insert_itinerary_with_day(client):
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
    response = client.post(ITINERARY_ENDPOINT, json=itinerary)
    assert response.status_code == 201


def test_insert_weather_to_day(client):
    weather = {
        "weather_states": [],
        "day_id": 1,
        "model": "ICON"
    }

    day = {
        "id": 1,
        "weather": weather
    }
    response = client.post(f"{DAY_ENDPOINT}/update", json=day)
    assert response.status_code == HTTPStatus.OK


def test_insert_sea_to_day(client):
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
    response = client.post(f"{DAY_ENDPOINT}/update", json=day)
    assert response.status_code == HTTPStatus.OK


def test_get_day_by_key(client):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    json = {
        "itinerary_id":1,
        'day_number':1,
        'date':day_date
    }

    response = client.post(
        f"{DAY_ENDPOINT}/by-key", json=json)
    assert response.status_code == 200

def test_get_day_by_id(client):
    json_data = {
        "ids": [1]
    }
    response = client.post(
        f"{DAY_ENDPOINT}/read_by_ids", json=json_data)
    assert response.status_code == HTTPStatus.OK

def test_get_all_days(client):
    response = client.get(
        f"{DAY_ENDPOINT}/itinerary/1")
    assert response.status_code == HTTPStatus.OK
    assert len(json.loads(response.data)) == 1

def test_delete_day_by_key(client):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = client.delete(
        f"{DAY_ENDPOINT}?itinerary_id=1&day_number=1&date={day_date}")
    assert response.status_code == HTTPStatus.OK

def test_update_day(client):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    sea = None
    updated_day = {'id':1,'date':day_date,'itinerary_id':1,'day_number':1, 'sea':sea} 
    response = client.post(f"{DAY_ENDPOINT}/update", json=updated_day)
    assert json.loads(response.data)['sea'] == sea
    assert response.status_code == HTTPStatus.OK

def test_delete_day_by_id(client):
    response = client.delete(
        f"{DAY_ENDPOINT}/1")
    assert response.status_code == HTTPStatus.OK

def test_reinsert_day(client):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    new_day = {'id':1,'date':day_date,'itinerary_id':1,'day_number':1} 
    response = client.post(f"{DAY_ENDPOINT}", json=new_day)

    assert response.status_code == HTTPStatus.CREATED
