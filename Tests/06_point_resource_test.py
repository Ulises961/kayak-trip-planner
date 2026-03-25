import pytest
from Resources.point_resource import POINT_ENDPOINT
import json
from datetime import date, datetime


@pytest.fixture(scope="function")
def points(client, auth_headers, itinerary):
    point_1 = {"dayId": itinerary["days"][0]["id"], "type": "interest"}
    point_2 = {"dayId": itinerary["days"][0]["id"], "type": "position"}
    point_3 = {"dayId": itinerary["days"][0]["id"], "type": "interest"}
    point_4 = {"dayId": itinerary["days"][0]["id"], "type": "interest"}

    response_1 = client.post(
        f"{POINT_ENDPOINT}/create", headers=auth_headers, json=point_1
    )
    response_2 = client.post(
        f"{POINT_ENDPOINT}/create", headers=auth_headers, json=point_2
    )
    response_3 = client.post(
        f"{POINT_ENDPOINT}/create", headers=auth_headers, json=point_3
    )
    response_4 = client.post(
        f"{POINT_ENDPOINT}/create", headers=auth_headers, json=point_4
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201
    assert response_3.status_code == 201
    assert response_4.status_code == 201

    responses = [response_1, response_2, response_3, response_4]
    points = [response.json for response in responses]
    
    yield points
    
    # Clean up
    try:
        response_1 = client.delete(
            f"{POINT_ENDPOINT}/{point_1["id"]}", headers=auth_headers, json=point_1
        )
        response_2 = client.delete(
            f"{POINT_ENDPOINT}/{point_2["id"]}", headers=auth_headers, json=point_2
        )
        response_3 = client.delete(
            f"{POINT_ENDPOINT}/{point_3["id"]}", headers=auth_headers, json=point_3
        )
        response_4 = client.delete(
            f"{POINT_ENDPOINT}/{point_4["id"]}", headers=auth_headers, json=point_4
        )
    except:
        pass


def test_update_point(client, points, auth_headers):
    point = points[0]
    point_id = point["id"]
    point = {**point, "type": "stop"}

    response = client.post(
        f"{POINT_ENDPOINT}/{point_id}/update", headers=auth_headers, json=point
    )
    assert response.status_code == 200
    assert json.loads(response.data)["type"] == "stop"


def test_link_points(client, points, auth_headers):
    [point, point_2, _, _] = points
    point["next"] = point_2

    response = client.post(
        f"{POINT_ENDPOINT}/{point['id']}/update", headers=auth_headers, json=point
    )

    assert json.loads(response.data) == {
        "dayId": point["dayId"],
        "latitude": None,
        "longitude": None,
        "id": point["id"],
        "images": [],
        "next": {
            "dayId": point_2["dayId"],
            "latitude": None,
            "longitude": None,
            "id": point_2["id"],
            "images": [],
            "notes": None,
            "type": "position",
        },
        "notes": None,
        "type": "interest",
    }

    assert response.status_code == 200
    assert json.loads(response.data)["next"]["id"] == point_2["id"]


def test_delete_point(client, auth_headers, points):
    point = points[3]
    response = client.delete(f"{POINT_ENDPOINT}/{point["id"]}", headers=auth_headers)
    assert response.status_code == 200
    response = client.get(f"{POINT_ENDPOINT}/{point["id"]}", headers=auth_headers)
    assert response.status_code == 404
