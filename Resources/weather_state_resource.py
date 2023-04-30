import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.weather_state_schema import WeatherStateSchema
from Models.weather_state import WeatherState
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

WEATHER_STATE_ENDPOINT = "/api/weather_state/<id>"

class WeatherStateResource(Resource):

    def retrieveWeatherStateById(id):
        weather_state = WeatherState.query.filter_by('id', id).first()
        weather_state_json = WeatherStateSchema.dump(weather_state)
        if not weather_state_json:
             raise NoResultFound()
        return weather_state_json
    
    def get(self, id=None):
        """
        WeatherStateResource GET method. Retrieves the information related to the weather state with the passed id in the request
        """
        try:
            self.retrieveWeatherStateById(id)
        except NoResultFound:
                abort(404, message=f"Weather State with id {id} not found in database")
    
    def post(self):
        """
        WeatherStateResource POST method. Adds a new weather_state to the database.

        :return: WeatherState, 201 HTTP status code.
        """
        weather_state = WeatherStateSchema().load(request.get_json())

        try:
            db.session.add(weather_state)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this weather_state is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return weather_state, 201
