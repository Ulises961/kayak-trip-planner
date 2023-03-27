from marshmallow import Schema, fields, post_load
from Models.weather_state import WeatherState


class WeatherStateSchema(Schema):
    """ 
    Sea State Schema
    used for loading/dumping Sea State entities
    """

    day_number = fields.Integer(allow_none=True)
    itinerary_id=fields.Integer(allow_none=False)
    date =fields.Date('dd-mm-yyyy',allow_none=False)
    time=fields.Time('hh:mm:ss',allow_none=True)
    temperature=fields.Float(allow_none=False)
    precipitation=fields.Float(allow_none=False)
    wind_direction=fields.Float(allow_none=False)
    wind_force=fields.Float(allow_none=False)
    cloud=fields.String(allow_none=False)


    @post_load
    def make_weather_state(self, data, **kwargs):
        return WeatherState(**data)