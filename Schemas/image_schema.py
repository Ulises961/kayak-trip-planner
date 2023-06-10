from marshmallow import Schema, fields, post_load
from Models.image import Image


class ImageSchema(Schema):
    """ 
    Image Schema
    used for loading/dumping Image entities
    """

    id = fields.Integer(allow_none=True)
    size =fields.Float(allow_none=False)
    name=fields.String(allow_none=False)
    location=fields.String(allow_none=False)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)