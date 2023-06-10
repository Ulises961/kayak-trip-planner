from flask import Flask
from flask_restful import Api
import path
import sys

 # directory reach
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from Api.config import config
from Api.database import db
import logging
from logging.handlers import RotatingFileHandler 
import os
from dotenv import load_dotenv



from Resources.image_resource import ImageResource, IMAGE_ENDPOINT
from Resources.user_resource import UserResource, USER_ENDPOINT
from Resources.trip_resource import TripResource, TRIP_ENDPOINT
from Resources.itinerary_resource import ItineraryResource, ITINERARY_ENDPOINT

from Resources.day_resource import DayResource, DAY_ENDPOINT
from Resources.point_resource import PointResource, POINT_ENDPOINT

from Resources.inventory_resource import InventoryResource, INVENTORY_ENDPOINT
from Resources.item_resource import ItemResource, ITEM_ENDPOINT

from Resources.sea_resource import SeaResource, SEA_ENDPOINT
from Resources.sea_state_resource import SeaStateResource, SEA_STATE_ENDPOINT

from Resources.weather_resource import WeatherResource, WEATHER_ENDPOINT
from Resources.weather_state_resource import WeatherStateResource, WEATHER_STATE_ENDPOINT


from Resources.log_resource import LogResource, LOG_ENDPOINT


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
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Configure logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[
            RotatingFileHandler(
                "./var/log/kayak-trip-planner.log", maxBytes=2000, backupCount=5, encoding='UTF-8'),
            logging.StreamHandler()
        ])
    api = Api(app)
    api.add_resource(DayResource, DAY_ENDPOINT, f"{DAY_ENDPOINT}/<id>")
    api.add_resource(ImageResource, IMAGE_ENDPOINT),f"{IMAGE_ENDPOINT}/<id>"
    api.add_resource(InventoryResource, INVENTORY_ENDPOINT,f"{INVENTORY_ENDPOINT}/<id>")
    api.add_resource(ItemResource, ITEM_ENDPOINT,f"{ITEM_ENDPOINT}/<id>")
    api.add_resource(ItineraryResource, ITINERARY_ENDPOINT, f"{ITINERARY_ENDPOINT}/<id>")
    api.add_resource(LogResource, LOG_ENDPOINT,f"{LOG_ENDPOINT}/<id>")
    api.add_resource(PointResource, POINT_ENDPOINT, f"{POINT_ENDPOINT}/<id>")
    api.add_resource(SeaResource, SEA_ENDPOINT, f"{SEA_ENDPOINT}/<day_id>")
    api.add_resource(SeaStateResource, SEA_STATE_ENDPOINT, f"{SEA_STATE_ENDPOINT}/<day_id>")
    api.add_resource(TripResource, TRIP_ENDPOINT, f"{TRIP_ENDPOINT}/<id>")
    api.add_resource(UserResource, USER_ENDPOINT, f"{USER_ENDPOINT}/<id>")
    api.add_resource(WeatherResource, WEATHER_ENDPOINT, f"{WEATHER_ENDPOINT}/<day_id>")
    api.add_resource(WeatherStateResource, WEATHER_STATE_ENDPOINT, f"{WEATHER_STATE_ENDPOINT}/<day_id>")
    return app


if __name__ == "__main__":
    load_dotenv()
    app = createApp(os.getenv("CONFIG_MODE"))
    app.run()
