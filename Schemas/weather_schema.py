from marshmallow import Schema, fields, post_load
from Models.weather import Weather


class WeatherSchema(Schema):
    """ 
    Weather Schema
    used for loading/dumping Weather entities
    """

    day_number   = fields.Integer(allow_none=False)
    itinerary_id = fields.Integer(allow_none=False)
    date = fields.Date('dd-mm-yyyy',allow_none=False)
    time = fields.Time('hh:mm:ss',allow_none=False)
    model = fields.String(allow_none=False)
    
    @post_load
    def make_weather(self, data, **kwargs):
        return Weather(**data)