from Resources.point_resource import POINT_ENDPOINT
import json
from datetime import date, datetime


def test_insert_points(app):
    point_1 = {
        "itinerary_id": 1,
        "day_number": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "type": "interest"
    }
    point_2 = {
        "itinerary_id": 1,
        "day_number": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "type": "position"
    }
    point_3 = {
        "itinerary_id": 1,
        "day_number": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "type": "interest"
    }
    point_4 = {
        "type": "interest"
    }

    response_1 = app.post(POINT_ENDPOINT, json=point_1)
    response_2 = app.post(POINT_ENDPOINT, json=point_2)
    response_3 = app.post(POINT_ENDPOINT, json=point_3)
    response_4 = app.post(POINT_ENDPOINT, json=point_4)
    assert response_1.status_code == 201
    assert response_2.status_code == 201
    assert response_3.status_code == 201


def test_update_point(app):
    point = {
        "id": 1,
        "type": "stop"
    }
    response = app.put(POINT_ENDPOINT, json=point)
    assert json.loads(response.data)['type'] == "stop"
    assert response.status_code == 201


def test_link_points(app):
    point = {
        "id": 1,
        "next": {'id': 2},
        "nearby": [{'id': 3}, {'id': 4}]
    }
    point_3 = {'date': '2020-12-31',
               'day_number': 1,
               'gps': None,
               'id': 3,
               'images': {},
               'itinerary_id': 1,
               'notes': None,
               'type': 'interest'}
    point_4 = {'date': None,
               'day_number': None,
               'gps': None,
               'id': 4,
               'images': {},
               'itinerary_id': None,
               'notes': None,
               'type': 'interest'}

    response = app.put(POINT_ENDPOINT, json=point)
    assert json.loads(response.data) == {
        'date': '2020-12-31',
        'day_number': 1,
        'gps': None,
        'id': 1,
        'images': {},
        'itinerary_id': 1,
        'nearby': [point_3, point_4],
        'next': {'date': '2020-12-31',
                 'day_number': 1,
                 'gps': None,
                 'id': 2,
                 'images': {},
                 'itinerary_id': 1,
                 'notes': None,
                 'type': 'position'},
        'notes': None,
        'previous': None,
        'type': 'stop'}

    assert json.loads(response.data)['nearby'][0]['id'] == 3
    assert response.status_code == 201


def test_delete_point(app):
    response = app.delete(f"{POINT_ENDPOINT}?id=3")
    assert response.status_code == 200
    response = app.get(f"{POINT_ENDPOINT}?id=3")
    assert response.status_code == 404


def test_get_inexistent_point(app):
    response = app.get(f"{POINT_ENDPOINT}?id=3")
    assert response.status_code == 404


def test_get_point(app):
    response = app.get(f"{POINT_ENDPOINT}?id=2")
    assert response.status_code == 200
    assert json.loads(response.data)['type'] == "position"
