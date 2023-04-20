import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.weather_state_schema import WeatherStateSchema
from Models.weather_state import WeatherState

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/weather_state/<id>"

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
        