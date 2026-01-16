from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.user import User
from Schemas.log_schema import LogSchema
from Schemas.trip_schema import TripSchema
from Schemas.image_schema import ImageSchema
import re

class UserSchema(Schema):
    """ 
    User Schema
    used for loading/dumping User entities
    """

    id   = fields.Integer(allow_none=False)
    public_id = fields.String(allow_none=False)
    mail = fields.Email(allow_none=True)
    pwd = fields.String(allow_none=True)
    phone = fields.String(allow_none=True)  
    username = fields.String(allow_none=True)  
    name = fields.String(allow_none=True)  
    surname = fields.String(allow_none=True)  
    trip = fields.Nested(TripSchema, allow_none=True)  
    endorsed_logs = fields.List(fields.Nested(LogSchema), allow_none=True)  
    logs = fields.List(fields.Nested(LogSchema), allow_none=True )
    image = fields.Nested(ImageSchema, allow_none=True)
    admin = fields.Bool(allow_none=True)

    @validates('username')
    def validate_username(self, value, **kwargs):
        """Validate username format and length."""
        if value is not None:
            if len(value) < 3:
                raise ValidationError("Username must be at least 3 characters long")
            if len(value) > 50:
                raise ValidationError("Username cannot exceed 50 characters")
            if not re.match(r'^[a-zA-Z0-9_-]+$', value):
                raise ValidationError(
                    "Username can only contain letters, numbers, underscores, and hyphens"
                )
    
    @validates('phone')
    def validate_phone(self, value, **kwargs):
        """Validate phone number format."""
        if value is not None:
            # Remove common separators
            cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
            if not cleaned.isdigit():
                raise ValidationError("Phone number must contain only digits")
            if len(cleaned) < 7 or len(cleaned) > 15:
                raise ValidationError("Phone number must be between 7 and 15 digits")
    
    @validates('pwd')
    def validate_password(self, value, **kwargs):
        """Validate password strength."""
        if value is not None:
            if len(value) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            if len(value) > 128:
                raise ValidationError("Password cannot exceed 128 characters")
    
    @validates('name')
    def validate_name(self, value, **kwargs):
        """Validate name length."""
        if value is not None:
            if len(value) < 1:
                raise ValidationError("Name cannot be empty")
            if len(value) > 100:
                raise ValidationError("Name cannot exceed 100 characters")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)