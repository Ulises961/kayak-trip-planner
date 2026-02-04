from marshmallow import Schema, fields, post_dump, post_load, pre_load
from Models.item import Item, ItemCategoryType
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound

class ItemSchema(Schema):
    """ 
    Item Schema
    used for loading/dumping Item entities
    """

    id = fields.Integer(allow_none=True)
    category = fields.Enum(ItemCategoryType, by_value=True)
    checked = fields.Boolean(allow_none=True)
    name = fields.String(allow_none=False)
    user_id = fields.Integer(allow_none=False)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

    @pre_load
    def load_user_id(self, data, **kwargs):
        """Convert public_id to internal user.id before loading"""
        user = db.session.query(User).filter_by(public_id=data['user_id']).first()
        if not user:
            raise NoResultFound(f"User with public_id {data['user_id']} not found")
        data['user_id'] = user.id
        return data
    
      
    @post_dump
    def dump_user_id(self, data, **kwargs):
        """Convert internal user.id back to public_id after dumping"""
        user = db.session.query(User).filter_by(id=data['user_id']).first()
        if user:
            data['user_id'] = user.public_id
        return data
    