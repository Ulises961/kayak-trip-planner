import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.weather_schema import WeatherSchema
from Models.weather import Weather

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/weather/<id>"

class WeatherResource(Resource):

    def retrieveWeatherById(id):
        weather = Weather.query.filter_by('id', id).first()
        weather_json = WeatherSchema.dump(weather)
        if not weather_json:
             raise NoResultFound()
        return weather_json
    
    def get(self, id=None):
        """
        WeatherResource GET method. Retrieves the information related to the weather with the passed id in the request
        """
        try:
            self.retrieveWeatherById(id)
        except NoResultFound:
                abort(404, message=f"Weather with id {id} not found in database")
        