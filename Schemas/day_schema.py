from marshmallow import Schema, fields, post_load
from Models.day import Day
from Schemas.point_schema import PointSchema
from Schemas.sea_schema import SeaSchema
from Schemas.weather_schema import WeatherSchema
from marshmallow_sqlalchemy import SQLAlchemySchema
from Api.database import db

class DaySchema(SQLAlchemySchema):
    """ 
    Day Schema
    used for loading/dumping Day entities
    """
    class Meta:
        model = Day
        load_instance = True
        sqla_session = db.session

    day_number = fields.Integer(allow_none=False)
    itinerary_id = fields.Integer(allow_none=False)
    date=fields.Date('%Y-%m-%d',allow_none=False)
    points=fields.List(fields.Nested(PointSchema), allow_none = True)
    sea=fields.Nested(SeaSchema, allow_none = True)
    weather=fields.Nested(WeatherSchema, allow_none = True)

