import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.weather_state_schema import WeatherStateSchema
from Models.weather_state import WeatherState
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

WEATHER_STATE_ENDPOINT = "/api/weather_state"


class WeatherStateResource(Resource):

    def __retrieve_weather_state_by_key(self, day_id, time):
        return WeatherState.query.filter_by(day_id=day_id, time=time).first()

    def get(self, day_id):
        """
        WeatherStateResource GET method. Retrieves the information related to the weather state with the passed id in the request
        """
        try:
            weather_state = WeatherStateSchema().dump(request.get_json())
            weather_state = self.__retrieve_weather_state_by_key(day_id,
                                                                 weather_state.time
                                                                 )
            weather_state_json = WeatherStateSchema().dump(weather_state)
            if not weather_state_json:
                raise NoResultFound()
            return weather_state_json, 200
        except NoResultFound:
            abort(
                404, message=f"Weather State with id {id} not found in database")
        except Exception as e:
            abort(500, message=f"Error: {e}")

    def post(self):
        """
        WeatherStateResource POST method. Adds a new weather_state to the database.

        :return: WeatherState, 201 HTTP status code.
        """
        try:
            weather_state = WeatherStateSchema().load(request.get_json())
            db.session.add(weather_state)
            db.session.commit()
            weather_state = self.__retrieve_weather_state_by_key(
                weather_state.day_id,
                weather_state.time
            )
            return WeatherStateSchema().dump(weather_state), 201
        except IntegrityError as e:
            logger.error(
                f"Integrity Error, this weather_state is already in the database. Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Unexpected Error!")

    def put(self):
        try:
            logger.info(f"Update weather state {request.get_json()} in db")
            weather_state = WeatherStateSchema().load(request.get_json())
            db.session.merge(weather_state)
            db.session.commit()
            weather_state = self.__retrieve_weather_state_by_key(weather_state.day_id,
                                                                 weather_state.time
                                                                 )

            return WeatherStateSchema().dump(weather_state), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self, day_id):
        try:
            weather_state = WeatherStateSchema().dump(request.get_json())
            logger.info(f"Deleting weather state {weather_state} ")

            weather_state = self.__retrieve_weather_state_by_key(day_id,
                                                                 weather_state.time
                                                                 )
            db.session.delete(weather_state)
            db.session.commit()
            logger.info(f"Weather state {weather_state} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
