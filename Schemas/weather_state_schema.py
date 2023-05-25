from marshmallow import Schema, fields, post_load
from Models.weather_state import WeatherState


class WeatherStateSchema(Schema):
    """ 
    Weather State Schema
    used for loading/dumping Weather State entities
    """

    day_number = fields.Integer(allow_none=False)
    itinerary_id=fields.Integer(allow_none=False)
    date =fields.Date('%Y-%m-%d',allow_none=False)
    time=fields.Time('%H:%M:%S',allow_none=False)
    temperature=fields.Float(allow_none=True)
    precipitation=fields.Float(allow_none=True)
    wind_direction=fields.Float(allow_none=True)
    wind_force=fields.Float(allow_none=True)
    cloud=fields.String(allow_none=True)


    @post_load
    def make_weather_state(self, data, **kwargs):
        return WeatherState(**data)