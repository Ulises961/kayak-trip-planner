from marshmallow import Schema, fields, post_load
from Models.weather import Weather
from Schemas.weather_state_schema import WeatherStateSchema

class WeatherSchema(Schema):
    """ 
    Weather Schema
    used for loading/dumping Weather entities
    """

    day_id   = fields.Integer(allow_none=False)
    model = fields.String(allow_none=False)
    weather_states = fields.List(fields.Nested(WeatherStateSchema), allow_none=True)
    
    @post_load
    def make_weather(self, data, **kwargs):
        return Weather(**data)