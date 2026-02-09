from marshmallow import Schema, fields, post_load, post_dump, validates, ValidationError, pre_load
from Models.user import User
from Schemas.log_schema import LogSchema
from Schemas.image_schema import ImageSchema
import re
import bleach

class UserSchema(Schema):
    """ 
    User Schema
    used for loading/dumping User entities
    """

    # Internal DB id - never exposed in API
    # public_id exposed as 'id' in API via data_key
    public_id = fields.String(data_key='id', dump_only=True)
    mail = fields.Email(required=True, validate=lambda x: len(x) <= 255)
    pwd = fields.String(required=True, load_only=True, validate=lambda x: len(x) >= 8)
    phone = fields.String(required=True, validate=lambda x: len(x) <= 20)  
    username = fields.String(required=True, validate=lambda x: 3 <= len(x.strip()) <= 50)  
    name = fields.String(required=True, validate=lambda x: 1 <= len(x.strip()) <= 100)  
    surname = fields.String(allow_none=True, validate=lambda x: x is None or len(x.strip()) <= 100)  
    trips = fields.List(fields.Nested('TripSchema', allow_none=True))  
    itineraries = fields.List(fields.Nested('ItinerarySchema', allow_none=True))  
    inventories = fields.List(fields.Nested('InventorySchema', allow_none=True))  
    items = fields.List(fields.Nested('ItemSchema', allow_none=True))  
    endorsed_logs = fields.List(fields.Nested(LogSchema), allow_none=True)  
    logs = fields.List(fields.Nested(LogSchema), allow_none=True )
    image = fields.Nested(ImageSchema, allow_none=True)
    admin = fields.Bool(allow_none=True)

    @pre_load
    def handle_id_input(self, data, **kwargs):
        """Convert 'id' from API to 'public_id' for model."""
        if 'id' in data:
            data['public_id'] = data.pop('id')
        return data

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
            if len(value) > 20:
                raise ValidationError("Phone number cannot exceed 20 characters")
            # Remove common separators
            cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
            if not cleaned.isdigit():
                raise ValidationError("Phone number must contain only digits")
            if len(cleaned) < 7 or len(cleaned) > 15:
                raise ValidationError("Phone number must be between 7 and 15 digits")
    
    
    @validates('name')
    def validate_name(self, value, **kwargs):
        """Validate and sanitize name."""
        if value is not None:
            # Sanitize HTML/script tags
            sanitized = bleach.clean(value.strip(), tags=[], strip=True)
            if not sanitized:
                raise ValidationError("Name cannot be empty")
            if len(sanitized) > 100:
                raise ValidationError("Name cannot exceed 100 characters")
            if re.search(r'[<>"\';\[\]{}]', sanitized):
                raise ValidationError("Name contains invalid characters")
    
    @validates('surname')
    def validate_surname(self, value, **kwargs):
        """Validate and sanitize surname."""
        if value is not None:
            # Sanitize HTML/script tags
            sanitized = bleach.clean(value.strip(), tags=[], strip=True)
            if len(sanitized) > 100:
                raise ValidationError("Surname cannot exceed 100 characters")
            if re.search(r'[<>"\';\[\]{}]', sanitized):
                raise ValidationError("Surname contains invalid characters")
    
    @validates('mail')
    def validate_mail(self, value, **kwargs):
        """Validate email format and length."""
        if value is not None:
            if len(value) > 255:
                raise ValidationError("Email cannot exceed 255 characters")
            # Additional email validation
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(value):
                raise ValidationError("Invalid email format")
    
    @validates('pwd')
    def validate_pwd(self, value, **kwargs):
        """Validate password strength."""
        if value is not None:
            if len(value) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            if len(value) > 128:
                raise ValidationError("Password cannot exceed 128 characters")
            # Check for at least one letter and one number
            if not re.search(r'[a-zA-Z]', value) or not re.search(r'[0-9]', value):
                raise ValidationError("Password must contain at least one letter and one number")
           # Check for at least one special character
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                raise ValidationError("Password must contain at least one special character")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)