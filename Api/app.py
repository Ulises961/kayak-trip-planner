from flask import Flask
import os
import sys

 # directory reach
directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(directory))

from Api.config import config
from Api.database import db
from Api.logging_config import setup_logging
from Api.error_handlers import register_error_handlers
from dotenv import load_dotenv
from flask_migrate import Migrate


from Resources.image_resource import image_api
from Resources.user_resource import user_api
from Resources.trip_resource import trip_api
from Resources.itinerary_resource import itinerary_api

from Resources.day_resource import day_api
from Resources.point_resource import point_api

from Resources.inventory_resource import inventory_api
from Resources.item_resource import item_api

from Resources.log_resource import log_api

from Resources.authentication_resource import api as authApi


def createApp(config_mode:str):
    """
    Creates and configurates the Flask app, the logger to be used throughout  the application 
    and the database to use. Returns the configured app that is to be used in the main function.
    
    Params:
    config_mode -- the mode in which the app is to be run: development | testing | staging | production
    """

    app = Flask(__name__)
    # Get current config from the config.py file using the config_mode set in .env file
    app.config.from_object(config[config_mode])
    app.register_blueprint(authApi)
    app.register_blueprint(day_api)
    app.register_blueprint(image_api)
    app.register_blueprint(inventory_api)
    app.register_blueprint(item_api)
    app.register_blueprint(itinerary_api)
    app.register_blueprint(log_api)
    app.register_blueprint(trip_api)
    app.register_blueprint(point_api)
    app.register_blueprint(user_api)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate()
    migrate.init_app(app,db)

    # Configure logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    load_dotenv()
    app = createApp(os.getenv("CONFIG_MODE", "development"))
    app.run(host=os.environ['FLASK_HOST'])
