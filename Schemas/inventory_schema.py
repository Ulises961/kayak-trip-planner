from marshmallow import Schema, fields, post_load
from Models.inventory import Inventory
from Schemas.item_schema import ItemSchema

class InventorySchema(Schema):
    """ 
    Inventory Schema
    used for loading/dumping Inventory entities
    """

    id = fields.Integer(allow_none=True)
    trip_id =fields.Integer(allow_none=True)
    items=fields.List(fields.Nested(ItemSchema), allow_none=True)
    user_id=fields.Integer(allow_none=False)

    @post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)