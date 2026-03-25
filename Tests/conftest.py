from datetime import date
import json
import pytest
from sqlalchemy.exc import NoResultFound

from Models.user import User
from Resources.inventory_resource import INVENTORY_ENDPOINT
from Resources.itinerary_resource import ITINERARY_ENDPOINT
from Resources.trip_resource import TRIP_ENDPOINT
from Services.Middleware.auth_middleware import JWTService
from Api.app import createApp
from Api.database import db as _db

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    
    app = createApp('testing')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # db is already initialized in createApp(), no need to init again
    _db.create_all()
    
    def teardown():
        _db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope="session")
def user_1(app):
    client = app.test_client()
    user1 = {
        "mail": "test.user@gmail.com",
        "pwd": "testPassword6$",
        "phone": "+390123456789",
        "name": "Test User",
        "username": "test",
        "admin": True
    }
    response = client.post("/api/auth/register", json=user1)
    assert response.status_code == 201
    
    # Query the database directly for the public_id
    user = User.query.filter_by(mail="test.user@gmail.com").first()
    if not user:
        raise NoResultFound()
    
    return user

@pytest.fixture(scope="session")
def user_2(app):
    client = app.test_client()
    user2 = {
        "mail": "test1.user@gmail.com",
        "pwd": "pwdTest2$",
        "phone": "+391234567899",
        "name": "Don",
        "surname": "charles",
        "username": "charles99"
    }
    response = client.post("/api/auth/register", json=user2)
    assert response.status_code == 201
    
    # Query the database directly for the public_id
    user = User.query.filter_by(mail="test1.user@gmail.com").first()
    if not user:
        raise NoResultFound()
    return user

@pytest.fixture(scope='session')
def client(app):
    """Test client for making requests."""
    return app.test_client()

@pytest.fixture(scope='session')
def id(user_1):
    """Create first test user and return their public_id."""   
    return str(user_1.id)

@pytest.fixture(scope='session')
def id_2(user_2):
    """Create second test user and return their id."""    
  
    return str(user_2.id)


@pytest.fixture(scope='session')
def auth_token(app, user_1):
    """Get JWT token for the test user."""

    token = JWTService.generate_access_token(user_1.id, user_1.mail, user_1.admin)
    return token

@pytest.fixture(scope='session')
def auth_headers(auth_token):
    """Return authorization headers for authenticated requests."""
    return {'Authorization': f'Bearer {auth_token}'}

@pytest.fixture(scope="function")
def inventory_with_items(client, auth_headers, id):
    """Create an inventory with items for testing"""
    inventory_items = [
        {"category": 'travel', "name": 'compass'}, 
        {"category": "firstAid", "name": 'scissors'}
    ]
    inventory = {"items": inventory_items}
    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    inventory_data = json.loads(response.data)
    
    yield inventory_data
    
    # Cleanup: try to delete the inventory
    try:
        client.delete(f"{INVENTORY_ENDPOINT}/{inventory_data['id']}", headers=auth_headers)
    except:
        pass


@pytest.fixture(scope='function')
def empty_inventory(client, auth_headers, id):
    """Create an empty inventory for testing"""
    inventory = {"items": []}
    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    inventory_data = json.loads(response.data)
    
    yield inventory_data
    
    # Cleanup: try to delete the inventory
    try:
        client.delete(f"{INVENTORY_ENDPOINT}/{inventory_data['id']}", headers=auth_headers)
    except:
        pass

@pytest.fixture(scope="function")
def trip_w_o_itinerary(client, auth_headers):
    inventory = {"items":
                 [{"category": 'travel', "name": 'compass'}, {"category": "firstAid", "name": 'scissors'}]}
    trip = {"inventory":inventory}
    response = client.post(f"{TRIP_ENDPOINT}/create", json=trip, headers=auth_headers)
    assert response.status_code == 201
    trip_data = json.loads(response.data)
    
    yield trip_data

     # Cleanup: try to delete the inventory
    try:
        client.delete(f"{TRIP_ENDPOINT}/{trip_data['id']}", headers=auth_headers)
    except:
        pass

@pytest.fixture(scope="function")
def itinerary(client, auth_headers, trip_w_o_itinerary):
    days = [
        {
            "dayNumber": 1,
            "date": date.fromisoformat('2020-12-31').strftime("%Y-%m-%d"),
            "points": [],
        },
        {
            "dayNumber": 2,
            "date": date.fromisoformat('2020-01-01').strftime("%Y-%m-%d"),
            "points": []
        }
    ]

    itinerary = {"days": days, "tripId": trip_w_o_itinerary["id"]}
    response = client.post(f"{ITINERARY_ENDPOINT}/create", json=itinerary, headers=auth_headers)
    assert response.status_code == 201

    itinerary_data = json.loads(response.data)

    yield itinerary_data

     # Cleanup: try to delete the itinerary
    try:
        client.delete(f"{ITINERARY_ENDPOINT}/{itinerary_data['id']}", headers=auth_headers)
    except:
        pass

