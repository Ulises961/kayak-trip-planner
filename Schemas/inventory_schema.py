from flask import g
from marshmallow import Schema, fields, post_dump, post_load, validates, ValidationError
from Models.inventory import Inventory
from Models.user import User
from Schemas.base_schema import BaseSchema
from Schemas.item_schema import ItemSchema

class InventorySchema(BaseSchema):
    """ 
    Inventory Schema
    used for loading/dumping Inventory entities
    """

    trip_id = fields.UUID(allow_none=True)
    items = fields.List(fields.Nested(ItemSchema), allow_none=True, validate=lambda x: x is None or len(x) <= 1000)
    user_id = fields.UUID(allow_none=False, required=True)

    @validates('items')
    def validate_items(self, value, **kwargs):
        """Validate items list doesn't exceed reasonable limits."""
        if value is not None and len(value) > 1000:
            raise ValidationError("Inventory cannot contain more than 1000 items")

    @post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)
    