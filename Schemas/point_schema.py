from marshmallow import Schema, fields, post_load
from Models.point import Point
from app import db
from Models.point_has_image import PointHasImage

class ItemSchema(Schema):
    """ 
    Point Schema
    used for loading/dumping Point entities
    """

    id = fields.Integer(allow_none=True)
    category =fields.String(allow_none=False)
    checked=fields.Boolean(allow_none=True)
    name=fields.String(allow_none=False)

    @post_load
    def make_point(self, data, **kwargs):
        if data['image']:
            self.addImage(**data)
        return Point(**data)
    
    def addImage(data):
        point_with_image = PointHasImage(data['id'], data['image_id'])
        db.session.add(point_with_image)
        db.session.commit()
        