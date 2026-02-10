from http import HTTPStatus
from Resources.day_resource import DAY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from Resources.trip_resource import TRIP_ENDPOINT
from datetime import date, datetime
from Schemas.day_schema import DaySchema
import json
import pytest

@pytest.fixture
def test_trip(client, auth_headers):
    """Create a test trip and return its ID."""
    trip_data = {
        "itinerary": {"is_public": True, "total_miles": 25, "days": []},
        "inventory": {}
    }
    response = client.post(f"{TRIP_ENDPOINT}/create", json=trip_data, headers=auth_headers)
    assert response.status_code == 201
    return json.loads(response.data)['id']

@pytest.fixture
def test_itinerary_with_day(client, auth_headers, test_trip):
    """Create a test itinerary with one day and return itinerary_id and day_id."""
    daysList = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points": [],
        }
    ]
    itinerary = {
        "days": daysList,
        "trip_id": test_trip
    }

    response = client.post(f"{ITINERARY_ENDPOINT}/create", json=itinerary, headers=auth_headers)
    
    assert response.status_code == 201
    itinerary_data = json.loads(response.data)

    yield itinerary_data

     # Cleanup: try to delete the itinerary
    try:
        client.delete(f"{ITINERARY_ENDPOINT}/{itinerary_data['id']}", headers=auth_headers)
    except:
        pass




def test_insert_itinerary_with_day(client, auth_headers, test_trip):
    daysList = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points": [],
        }
    ]
    itinerary = {
        "days": daysList,
        "trip_id": test_trip
    }
    response = client.post(f"{ITINERARY_ENDPOINT}/create", json=itinerary, headers=auth_headers)
    assert response.status_code == 201


def test_insert_weather_to_day(client, auth_headers, test_itinerary_with_day):
    day_id = test_itinerary_with_day["days"][0]['id']
    weather = {
        "weather_states": [],
        "day_id": day_id,
        "model": "ICON"
    }

    day = {
        "id": day_id,
        "weather": weather
    }
    response = client.post(f"{DAY_ENDPOINT}/{day_id}/update", json=day, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK


def test_insert_sea_to_day(client, auth_headers, test_itinerary_with_day):
    day_id = test_itinerary_with_day["days"][0]['id']
    itinerary_id = test_itinerary_with_day['id']
    sea = {
        "sea_states": [],
        "day_id": day_id,
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "high_tide": datetime.now().time().strftime('%H:%M'),
    }

    day = {
        "id": day_id,
        "itinerary_id": itinerary_id,
        "sea": sea
    }
    response = client.post(f"{DAY_ENDPOINT}/{day_id}/update", json=day, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK


def test_get_day_by_key(client, auth_headers, test_itinerary_with_day):
    itinerary_id = test_itinerary_with_day['id']
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    json_data = {
        "itinerary_id": itinerary_id,
        'day_number': 1,
        'date': day_date
    }

    response = client.post(
        f"{DAY_ENDPOINT}/by-key", json=json_data, headers=auth_headers)
    assert response.status_code == 200


def test_get_all_days(client, auth_headers, test_itinerary_with_day):
    itinerary_id = test_itinerary_with_day['id']
    response = client.get(
        f"{DAY_ENDPOINT}/itinerary/{itinerary_id}", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert len(json.loads(response.data)) == 1

def test_update_day(client, auth_headers, test_itinerary_with_day):
    day_id = test_itinerary_with_day["days"][0]['id']
    itinerary_id = test_itinerary_with_day['id']
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    sea = None
    updated_day = {'id': day_id, 'date': day_date, 'itinerary_id': itinerary_id, 'day_number': 1, 'sea': sea} 
    response = client.post(f"{DAY_ENDPOINT}/{day_id}/update", json=updated_day, headers=auth_headers)
    json_data = json.loads(response.data)
    print("json data ",json_data)
    assert json_data['sea'] == sea
    assert response.status_code == HTTPStatus.OK

def test_delete_day_by_id(client, auth_headers, test_itinerary_with_day):
    day_id = test_itinerary_with_day["days"][0]['id']
    response = client.delete(
        f"{DAY_ENDPOINT}/{day_id}", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
