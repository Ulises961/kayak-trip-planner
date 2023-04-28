from flask import Flask
from flask_restful import Api
from config import config
from database import db
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
                "kayak-trip-planner.log", maxBytes=2000, backupCount=5, encoding='UTF-8'),
            logging.StreamHandler()
        ])
    api = Api(app)
    api.add_resource(DayResource, DAY_ENDPOINT)
    api.add_resource(ImageResource, IMAGE_ENDPOINT)
    api.add_resource(InventoryResource, INVENTORY_ENDPOINT)
    api.add_resource(ItemResource, ITEM_ENDPOINT)
    api.add_resource(ItineraryResource, ITINERARY_ENDPOINT)
    api.add_resource(LogResource, LOG_ENDPOINT)
    api.add_resource(PointResource, POINT_ENDPOINT)
    api.add_resource(SeaResource, SEA_ENDPOINT)
    api.add_resource(SeaStateResource, SEA_STATE_ENDPOINT)
    api.add_resource(TripResource, TRIP_ENDPOINT)
    api.add_resource(UserResource, USER_ENDPOINT)
    api.add_resource(WeatherResource, WEATHER_ENDPOINT)
    api.add_resource(WeatherStateResource, WEATHER_STATE_ENDPOINT)
    return app


if __name__ == "__main__":
    load_dotenv()
    app = createApp(os.getenv("CONFIG_MODE"))
    app.run()
