import pytest
import path
import sys

 # directory reach
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from Api.app import createApp
from Api.database import db as _db

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    
    app = createApp('testing')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    _db.app = app
    _db.create_all()
    
    def teardown():
        ctx.pop()
        with ctx:
            _db.drop_all()

    request.addfinalizer(teardown)
    with app.test_client() as client:
        yield client

