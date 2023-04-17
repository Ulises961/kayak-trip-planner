from marshmallow import Schema, fields, post_load
from Models.day import Day
from Models.point import Point
from Schemas.sea_schema import SeaSchema
from Schemas.weather_schema import WeatherSchema

class DaySchema(Schema):
    """ 
    Day Schema
    used for loading/dumping Day entities
    """

    day_number = fields.Integer(allow_none=False)
    position =fields.Integer(allow_none=False)
    date=fields.Date('dd-mm-yyyy',allow_none=False)
    points=fields.List(fields.Nested(Point))
    sea=fields.Nested(SeaSchema)
    weather=fields.Nested(WeatherSchema)

    @post_load
    def make_day(self, data, **kwargs):
        return Day(**data)