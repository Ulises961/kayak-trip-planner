from marshmallow import Schema, fields, post_load
from Models.point import Point
from Api.database import db
from Models.point_has_image import PointHasImage
from Schemas.image_schema import ImageSchema


class PointSchema(Schema):
    """ 
    Point Schema
    used for loading/dumping Point entities
    """

    id = fields.Integer(allow_none=True)
    category = fields.String(allow_none=False)
    checked = fields.Boolean(allow_none=True)
    name = fields.String(allow_none=False)
    images = fields.Nested(ImageSchema, allow_none=True)

    @post_load
    def make_point(self, data, **kwargs):
        return Point(**data)
