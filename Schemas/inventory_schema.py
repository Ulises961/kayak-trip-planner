from marshmallow import Schema, fields, post_load
from Models.inventory import Inventory
from Models.item import Item

class InventorySchema(Schema):
    """ 
    Inventory Schema
    used for loading/dumping Inventory entities
    """

    id = fields.Integer(allow_none=True)
    trii_id =fields.Integer(allow_none=False)
    items=fields.List(Item)


    @post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)