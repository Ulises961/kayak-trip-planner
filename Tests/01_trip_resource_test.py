from Resources.trip_resource import TRIP_ENDPOINT
import json

def test_insert_trip_w_itinerary_and_inventory(client, auth_headers):
    itinerary = {"is_public": True, "total_miles": 25,"days":[ ]}
    inventory = {"items":
                 [{"category": 'travel', "name": 'compass'}, {"category": "first_aid", "name": 'scissors'}]}
    trip = {"inventory":inventory, "itinerary":itinerary}

    response = client.post(f"{TRIP_ENDPOINT}/create", json=trip, headers=auth_headers)
    assert response.status_code == 201

def test_insert_trip_w_itinerary_and_empty_inventory(client, auth_headers):
    itinerary = {"is_public": True, "total_miles": 25, 'days':[]}
    inventory = {}
    trip = {"inventory":inventory, "itinerary":itinerary}

    response = client.post(f"{TRIP_ENDPOINT}/create", json=trip, headers=auth_headers)
    assert response.status_code == 201

def test_insert_trip_w_o_itinerary(client, auth_headers):
    inventory = {"items":
                 [{"category": 'travel', "name": 'compass'}, {"category": "first_aid", "name": 'scissors'}]}
    trip = {"inventory":inventory}
    response = client.post(f"{TRIP_ENDPOINT}/create", json=trip, headers=auth_headers)
    assert response.status_code == 201

def test_get_all_trips(client, auth_headers, public_id):
    response = client.get(f"{TRIP_ENDPOINT}/{public_id}/all", headers=auth_headers)
    assert response.status_code == 200
    # Number of trips depends on what was created in previous tests
    assert isinstance(json.loads(response.data), list)

def test_get_trip_by_id(client, auth_headers):
    # First create a trip to get its ID
    trip_data = {
        "itinerary": {"is_public": True, "total_miles": 25, "days": []},
        "inventory": {}
    }
    create_response = client.post(f"{TRIP_ENDPOINT}/create", json=trip_data, headers=auth_headers)
    assert create_response.status_code == 201
    
    trip_id = json.loads(create_response.data)['id']
    response = client.get(f"{TRIP_ENDPOINT}/{trip_id}", headers=auth_headers)
    assert response.status_code == 200
