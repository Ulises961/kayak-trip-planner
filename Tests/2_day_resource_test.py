from Resources.day_resource import DAY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from datetime import date, datetime
from Schemas.day_schema import DaySchema

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
        "day_number": 1,
        "itinerary_id": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "model": "ICON"
    }

    day = {
        "itinerary_id": 1,
        "day_number": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "weather": weather
    }
    response = app.post(DAY_ENDPOINT, json=day)
    assert response.status_code == 201


def test_insert_sea_to_day(app):
    sea = {
        "sea_states": [],
        "day_number": 1,
        "itinerary_id": 1,
        "low_tide": datetime.now().time().strftime('%H:%M'),
        "high_tide": datetime.now().time().strftime('%H:%M'),
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    }

    day = {
        "itinerary_id": 1,
        "day_number": 1,
        "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
        "sea": sea
    }
    response = app.put(DAY_ENDPOINT, json=day)
    assert response.status_code == 201


def test_get_day_by_id(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.get(
        f"{DAY_ENDPOINT}?itinerary_id=1&day_number=1&date={day_date}")
    assert response.status_code == 200


def test_delte_day(app):
    day_date = date.fromisoformat('2020-12-31').strftime("%Y-%m-%d")
    response = app.delete(
        f"{DAY_ENDPOINT}?itinerary_id=1&day_number=1&date={day_date}")
    assert response.status_code == 200
