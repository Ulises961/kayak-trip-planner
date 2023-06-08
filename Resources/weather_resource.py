import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.weather_schema import WeatherSchema
from Models.weather import Weather
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

WEATHER_ENDPOINT = "/api/weather"


class WeatherResource(Resource):

    def __retrieve_weather_by_key(self, day_id):
        return Weather.query.filter_by(day_id=day_id).first()

    def get(self, day_id=None):
        """
        WeatherResource GET method. Retrieves the information related to the weather with the passed id in the request
        """
        try:
            if day_id:
                weather = self.__retrieve_weather_by_key(
                    day_id)
                weather_json = WeatherSchema().dump(weather)
                if not weather_json:
                    raise NoResultFound()
                return weather_json, 200
                
            else:
                logger.info(f"Retrive all weather from db")
                weather = Weather.query.all()
                weather_json = [WeatherSchema().dump(weather) for weather in weather]
                if len(weather_json) == 0:
                    raise NoResultFound()
                return weather_json, 200
        except NoResultFound:
            abort(404, message=f"Weather with id {id} not found in database")
        except Exception as e:
            abort(500, message=f"Error:{e}")


    def post(self):
        """
        WeatherResource POST method. Adds a new weather to the database.
        :return: Weather, 201 HTTP status code.
        """
        try:
            weather = WeatherSchema().load(request.get_json())
            db.session.add(weather)
            db.session.commit()

            weather = self.__retrieve_weather_by_key(
                weather.day_id
                )
            return WeatherSchema().dump(weather), 201
        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def put(self):
        """
        Weather Resource POST method. Updates an existing user.

        :return: Weather, 201 HTTP status code.
        """

        try:
            updated_weather = WeatherSchema().load(request.get_json())
            db.session.merge(updated_weather)
            db.session.commit()
            updated_weather = self.__retrieve_weather_by_key(
                updated_weather.day_id
            )
            logger.info(
                f"Weather: {updated_weather}"
            )
            return WeatherSchema().dump(updated_weather), 200

        except Exception as e:
            logger.error(
                f"Error: {e}")
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def delete(self, day_id):
        """
        Weather Resource DELETE method. Eliminates an existing weather from the db.

        :return: Deletion successful,200 HTTP status code. | 500, Error
        """
        try:
            weather = self.__retrieve_weather_by_key(day_id)

            db.session.delete(weather)
            db.session.commit()
            logger.info(
                f"Weather with with day id{weather.day_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}")
            abort(
                500, message=f"Error: {e}")