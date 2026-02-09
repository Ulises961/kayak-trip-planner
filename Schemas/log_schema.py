from flask import g
from marshmallow import Schema, fields, post_load, post_dump, pre_load, validates, ValidationError
import uuid
from Models.log import Log
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound
import bleach


class LogSchema(Schema):
    """ 
    Log Schema
    used for loading/dumping Log entities
    """

    # Expose public_id as 'id' in API via data_key
    public_id = fields.String(data_key='id', dump_only=True, load_default=(uuid.uuid4()))
    hours = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 24))
    avg_sea = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 10))
    user_id = fields.Integer(allow_none=False, required=True) 

    @pre_load
    def handle_id_input(self, data, **kwargs):
        """Convert 'id' from API to 'public_id"""
        if 'id' in data:
            data['public_id'] = data.pop('id')
        return data

    @pre_load
    def load_private_ids(self, data, **kwargs):
        """Convert public_id to internal user.id before loading"""
        data['user_id'] = g.current_user_id
        return data

    @validates('hours')
    def validate_hours(self, value, **kwargs):
        """Validate hours is within reasonable range."""
        if value is not None:
            if value < 0:
                raise ValidationError("Hours cannot be negative")
            if value > 24:
                raise ValidationError("Hours cannot exceed 24")
    
    @validates('avg_sea')
    def validate_avg_sea(self, value, **kwargs):
        """Validate average sea state is within valid range."""
        if value is not None:
            if value < 0:
                raise ValidationError("Sea state cannot be negative")
            if value > 10:
                raise ValidationError("Sea state cannot exceed 10 (Douglas scale)")

    @post_load
    def make_log(self, data, **kwargs):
        return Log(**data)

    @post_dump
    def dump_public_ids(self, data, **kwargs):
        """Convert internal user ID back to public_id after dumping"""
        # Map public_id to id field for API
        if 'user_id' in data:
            data['user_id'] = g.current_user_public_id
        return data