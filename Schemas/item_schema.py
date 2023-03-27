from marshmallow import Schema, fields, post_load
from Models.item import Item


class ItemSchema(Schema):
    """ 
    Item Schema
    used for loading/dumping Item entities
    """

    id = fields.Integer(allow_none=True)
    category =fields.String(allow_none=False)
    checked=fields.Boolean(allow_none=True)
    name=fields.String(allow_none=False)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)