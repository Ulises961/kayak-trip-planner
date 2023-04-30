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


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session