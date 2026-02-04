from marshmallow import Schema, fields, post_dump, post_load, pre_dump, pre_load
from Models.inventory import Inventory
from Models.user import User
from Schemas.item_schema import ItemSchema
from Api.database import db
from sqlalchemy.exc import NoResultFound

class InventorySchema(Schema):
    """ 
    Inventory Schema
    used for loading/dumping Inventory entities
    """

    id = fields.Integer(allow_none=True)
    trip_id =fields.Integer(allow_none=True)
    items=fields.List(fields.Nested(ItemSchema), allow_none=True)
    user_id=fields.Integer(allow_none=True)

    @pre_load
    def load_user_id(self, data, **kwargs):
        """Convert public_id to internal user.id before loading"""
        if 'user_id' in data:
            user = db.session.query(User).filter_by(public_id=data['user_id']).first()
            if not user:
                raise NoResultFound(f"User with public_id {data['user_id']} not found")
            data['user_id'] = user.id
        return data
    
    @post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)
    
    @post_dump
    def dump_user_id(self, data, **kwargs):
        """Convert internal user.id back to public_id after dumping"""
        user = db.session.query(User).filter_by(id=data['user_id']).first()
        if user:
            data['user_id'] = user.public_id
        return data
    