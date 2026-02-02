import uuid
import pytest
import os
import sys

from sqlalchemy import cast
from sqlalchemy.exc import NoResultFound

 # directory reach - add parent directory to path
directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(directory))

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

@pytest.fixture(scope='function')
def client(app):
    """Test client for making requests."""
    return app.test_client()

@pytest.fixture(scope='session')
def public_id(app):
    """Create first test user and return their public_id."""
    from Models.user import User
    
    client = app.test_client()
    user1 = {
        "mail": "test.user@gmail.com",
        "pwd": "testPassword",
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
    return user.public_id

@pytest.fixture(scope='session')
def public_id_1(app):
    """Create second test user and return their public_id."""
    from Models.user import User
    
    client = app.test_client()
    user2 = {
        "mail": "test1.user@gmail.com",
        "pwd": "pwd",
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
    return user.public_id

@pytest.fixture(scope='function')
def user_id(app, public_id):
    """Get integer user ID for the test user."""
    from Models.user import User
    
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        raise NoResultFound()
    return user.id

@pytest.fixture(scope='function')
def auth_token(app, public_id):
    """Get JWT token for the test user."""
    from Services.Middleware.auth_middleware import JWTService
    from Models.user import User
    
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        raise NoResultFound()
    token = JWTService.generate_access_token(user.public_id, user.mail, user.admin)
    return token

@pytest.fixture(scope='function')
def auth_headers(auth_token):
    """Return authorization headers for authenticated requests."""
    return {'Authorization': f'Bearer {auth_token}'}