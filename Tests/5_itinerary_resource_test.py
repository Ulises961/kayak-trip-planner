from Resources.itinerary_resource import ITINERARY_ENDPOINT
import json
from datetime import date


def test_update_itinerary(app):
    days = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points": [],
        },
        {
            "day_number": 2,
            "date": date.fromisoformat('2020-01-01').strftime("%Y-%m-%d"),
            "points": [],
            "itinerary_id":1
        }
    ]

    itinerary = {"id": 1, "days": days, "trip_id":1}

    response = app.put(ITINERARY_ENDPOINT, json=itinerary)
    itinerary = json.loads(response.data)

    assert itinerary['days'][0]['day_number'] == 1
    assert itinerary['days'][0]['itinerary_id'] == 1
    assert itinerary['days'][0]['date'] == "2020-12-31"
    assert itinerary['trip_id'] == 1
    assert response.status_code == 201

def test_get_itinerary_by_id(app):
    response = app.get(f"{ITINERARY_ENDPOINT}?id=1")
    itinerary = json.loads(response.data)
    assert itinerary['days'][0]['day_number'] == 1
    assert itinerary['days'][0]['itinerary_id'] == 1
    assert itinerary['days'][0]['date'] == "2020-12-31"
    assert len(itinerary['days']) == 2
    assert response.status_code == 200

def test_remove_days_from_itinerary(app):
    itinerary = {"id": 1, "days": [], "trip_id":1}

    response = app.put(ITINERARY_ENDPOINT, json=itinerary)
    itinerary = json.loads(response.data)

    assert len(itinerary['days']) == 0
    assert itinerary['trip_id'] == 1
    assert response.status_code == 201



def test_delete_itinerary(app):
    response = app.delete(f"{ITINERARY_ENDPOINT}?id=1")
    assert response.status_code == 200
