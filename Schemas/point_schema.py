from marshmallow import Schema, fields, post_load
from Models.point import Point, PointType
from Api.database import db
from Schemas.image_schema import ImageSchema


class PointSchema(Schema):
    """ 
    Point Schema
    used for loading/dumping Point entities
    """
    id = fields.Integer(allow_none=False)
    gps = fields.Float(allow_none=True)
    notes = fields.String(allow_none=True)
    type = fields.Enum(PointType, by_value=True)
    day_id = fields.Integer(allow_none=True)
    previous = fields.Nested(lambda: PointSchema(
    ), allow_none=True, exclude=("previous", "next", "nearby"))
    next = fields.Nested(lambda: PointSchema(), allow_none=True,
                         exclude=("previous", "next", "nearby"))
    nearby = fields.List(fields.Nested(lambda: PointSchema(
    ), allow_none=True, exclude=("previous", "next", "nearby")))
    images = fields.List(fields.Nested(ImageSchema, allow_none=True))

    @post_load
    def make_point(self, data, **kwargs):
        return Point(**data)
