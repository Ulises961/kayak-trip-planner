from flask import Flask
from flask_restful import Api
from config import config
from database import db
import logging
import os

from Resources.user_resource import UserResource, USER_ENDPOINT
from Resources.image_resource import ImageResource, IMAGE_ENDPOINT
from Resources.inventory_resource import InventoryResource, INVENTORY_ENDPOINT
from Resources.item_resource import ItemResource, ITEM_ENDPOINT
from Resources.itinerary_resource import ItineraryResource, ITINERARY_ENDPOINT
from Resources.log_resource import LogResource, LOG_ENDPOINT
from Resources.point_resource import PointResource, POINT_ENDPOINT
from Resources.sea_resource import SeaResource, SEA_ENDPOINT
from Resources.sea_state_resource import SeaStateResource, SEA_STATE_ENDPOINT
from Resources.trip_resource import TripResource, TRIP_ENDPOINT
from Resources.user_resource import UserResource, USER_ENDPOINT
from Resources.weather_resource import WeatherResource, WEATHER_ENDPOINT
from Resources.weather_state_resource import WeatherStateResource, WEATHER_STATE_ENDPOINT


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

    # Configure logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[
            logging.RotatingFileHandler(
                "kayak-trip-planner.log", maxBytes=2000, backupCount=5, encoding='UTF-8'),
            logging.StreamHandler()
        ])
    api = Api(app)
    # api.add_resource(PlayersResource, PLAYERS_ENDPOINT, f"{PLAYERS_ENDPOINT}/<id>")
    # api.add_resource(SeasonsResource, SEASONS_ENDPOINT)
    # api.add_resource(StatsResource, STATS_ENDPOINT)
    # api.add_resource(StatsPlayerResource, STATS_PLAYER_ENDPOINT)
    # api.add_resource(StatsSeasonResource, STATS_SEASON_ENDPOINT)
    # api.add_resource(TeamsResource, TEAMS_ENDPOINT, f"{TEAMS_ENDPOINT}/<id>")
    return app


if __name__ == "__main__":
    app = createApp(os.getenv("CONFIG_MODE"))
    app.run()
