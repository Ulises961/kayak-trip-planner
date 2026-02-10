from Resources.itinerary_resource import ITINERARY_ENDPOINT
import json
from datetime import date


def test_update_itinerary(client, auth_headers, itinerary):
    days = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2026-12-31').strftime("%Y-%m-%d"),
            "points": [],
        },
        {
            "day_number": 2,
            "date": date.fromisoformat('2026-01-01').strftime("%Y-%m-%d"),
            "points": [],
        }
    ]

    itinerary = {**itinerary, "days": days, }

    response = client.post(f"{ITINERARY_ENDPOINT}/{itinerary['id']}/update", headers=auth_headers, json=itinerary)
    updated_itinerary = json.loads(response.data)

    assert response.status_code == 200
    assert updated_itinerary['days'][0]['day_number'] == 1
    assert updated_itinerary['days'][0]['date'] == "2026-12-31"
    assert updated_itinerary['trip_id'] == itinerary['trip_id']

def test_get_itinerary_by_id(client, auth_headers, itinerary):
    response = client.get(f"{ITINERARY_ENDPOINT}/{itinerary['id']}", headers=auth_headers)
    retrieved_itinerary = json.loads(response.data)
    assert retrieved_itinerary['days'][0]['day_number'] == 1
    assert retrieved_itinerary['days'][0]['date'] == "2020-12-31"
    assert len(retrieved_itinerary['days']) == 2
    assert response.status_code == 200

def test_remove_days_from_itinerary(client, auth_headers, itinerary):
    update_data = {"days": [], "trip_id": itinerary["trip_id"]}

    response = client.post(f"{ITINERARY_ENDPOINT}/{itinerary['id']}/update", headers=auth_headers, json=update_data)
    updated_itinerary = json.loads(response.data)

    assert len(updated_itinerary['days']) == 0
    assert updated_itinerary['trip_id'] == itinerary['trip_id']
    assert response.status_code == 200



def test_delete_itinerary(client, auth_headers, itinerary):
    response = client.delete(f"{ITINERARY_ENDPOINT}/{itinerary['id']}", headers=auth_headers)
    assert response.status_code == 200
