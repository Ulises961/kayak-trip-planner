import pytest
from Resources.point_resource import POINT_ENDPOINT
import json
from datetime import date, datetime


@pytest.fixture(scope="function")
def points(client, auth_headers):
    point_1 = {"day_id": 1, "type": "interest"}
    point_2 = {"day_id": 1, "type": "position"}
    point_3 = {"day_id": 1, "type": "interest"}
    point_4 = {"day_id": 1, "type": "interest"}

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
    points = [json.loads(response.data) for response in responses]
    return points


def test_update_point(client, points, auth_headers):
    point_id = points[0]["id"]
    point = {"type": "stop"}

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
        "day_id": 1,
        "latitude": None,
        "longitude": None,
        "id": 1,
        "images": [],
        "next": {
            "day_id": 1,
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
    assert json.loads(response.data)["next"]["id"] == 2


def test_delete_point(client, auth_headers):
    response = client.delete(f"{POINT_ENDPOINT}/3", headers=auth_headers)
    assert response.status_code == 200
    response = client.get(f"{POINT_ENDPOINT}/3", headers=auth_headers)
    assert response.status_code == 404


def test_get_inexistent_point(client, auth_headers):
    response = client.get(f"{POINT_ENDPOINT}/3", headers=auth_headers)
    assert response.status_code == 404


def test_get_point(client, auth_headers):
    response = client.get(f"{POINT_ENDPOINT}/2", headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)["type"] == "position"
