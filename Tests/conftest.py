import pytest
import os
import sys

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

