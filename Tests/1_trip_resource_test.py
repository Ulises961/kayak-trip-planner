from Resources.trip_resource import TRIP_ENDPOINT
from datetime import date
NUM_TRIPS_IN_DB = 3

def test_insert_trip_w_itinerary_and_inventory(app):
    itinerary = {"is_public": True, "total_miles": 25,"days":[ ]}
    inventory = {"items":
                 [{"category": 'travel', "name": 'compass'}, {"category": "first_aid", "name": 'scissors'}]}
    trip = {"inventory":inventory, "itinerary":itinerary}

    response = app.post(TRIP_ENDPOINT, json=trip)
    assert response.status_code == 201

def test_insert_trip_w_itinerary_and_empty_inventory(app):
    itinerary = {"is_public": True, "total_miles": 25, 'days':[]}
    inventory = {}
    trip = {"inventory":inventory, "itinerary":itinerary}

    response = app.post(TRIP_ENDPOINT, json=trip)
    assert response.status_code == 201

def test_insert_trip_w_o_itinerary(app):
    inventory = {"items":
                 [{"category": 'travel', "name": 'compass'}, {"category": "first_aid", "name": 'scissors'}]}
    trip = {"inventory":inventory}
    response = app.post(TRIP_ENDPOINT, json=trip)
    assert response.status_code == 201

def test_get_all_trips(app):
    response = app.get(TRIP_ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == NUM_TRIPS_IN_DB

def test_get_trip_by_id(app):
    response = app.get(f"{TRIP_ENDPOINT}/1")
    assert response.status_code == 200
