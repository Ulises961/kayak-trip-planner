from marshmallow import Schema, fields, post_load, post_dump, pre_load
import uuid
from Models.log import Log
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound


class LogSchema(Schema):
    """ 
    Log Schema
    used for loading/dumping Log entities
    """

    id = fields.Integer(allow_none=True, dump_only=True)
    public_id = fields.String(load_only=True)
    hours = fields.Float(allow_none=True)
    avg_sea = fields.Float(allow_none=True)
    user_id = fields.Integer(allow_none=False)

    @pre_load
    def load_private_ids(self, data, **kwargs):
        """Convert public_id to internal user.id before loading"""
        if 'user_id' in data:
            user = db.session.query(User).filter_by(public_id=data['user_id']).first()
            if not user:
                raise NoResultFound(f"User with public_id {data['user_id']} not found")
            data['user_id'] = user.id
        if "id" in data:
            log = db.session.query(Log).filter_by(public_id=data['id']).first()
            if not log:
                raise NoResultFound(f"Log with id {data['id']} not found")
            data['id'] = log.id
        return data

    @post_load
    def make_log(self, data, **kwargs):
        # Generate public_id if not present
        if 'public_id' not in data:
            data['public_id'] = str(uuid.uuid4())
        
        return Log(**data)

    @post_dump
    def dump_user_id(self, data, **kwargs):
        """Convert internal user.id back to public_id after dumping"""
        if 'user_id' in data and data['user_id']:
            user = db.session.query(User).filter_by(id=data['user_id']).first()
            if user:
                data['user_id'] = user.public_id
        data['id'] = data["public_id"]

        return data