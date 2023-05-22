from marshmallow import Schema, fields, post_load
from Models.day import Day
from Schemas.point_schema import PointSchema
from Schemas.sea_schema import SeaSchema
from Schemas.weather_schema import WeatherSchema

class DaySchema(Schema):
    """ 
    Day Schema
    used for loading/dumping Day entities
    """

    day_number = fields.Integer(allow_none=False)
    itinerary_id = fields.Integer(allow_none=False)
    date=fields.Date('%Y-%m-%d',allow_none=False)
    points=fields.List(fields.Nested(PointSchema), allow_none = True)
    sea=fields.Nested(SeaSchema, allow_none = True)
    weather=fields.Nested(WeatherSchema, allow_none = True)

    @post_load
    def make_day(self, data, **kwargs): 
            return Day(**data)