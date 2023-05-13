from Resources.day_resource import DAY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from datetime import date

def test_insert_day_with_sea_and_weather(app):
    daysList = [
        {
            "day_number": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points":[],
        }
    ]
    itinerary ={"days":daysList, "trip_id":1}
    response = app.post(ITINERARY_ENDPOINT, json=itinerary)
    assert response.status_code == 201