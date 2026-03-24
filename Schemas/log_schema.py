from flask import g
from marshmallow import Schema, fields, post_load, post_dump, pre_load, validates, ValidationError
import uuid
from Models.log import Log
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound
import bleach

from Schemas.base_schema import BaseSchema


class LogSchema(BaseSchema):
    """ 
    Log Schema
    used for loading/dumping Log entities
    """
    hours = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 24))
    avg_sea = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 10))
    user_id = fields.UUID(allow_none=False, required=True) 


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
