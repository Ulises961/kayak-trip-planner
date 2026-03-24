from flask import g
from marshmallow import Schema, fields, post_dump, post_load, validates, ValidationError
from Models.item import Item, ItemCategoryType
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound
import bleach
import re

from Schemas.base_schema import BaseSchema

class ItemSchema(BaseSchema):
    """ 
    Item Schema
    used for loading/dumping Item entities
    """
    category = fields.Enum(ItemCategoryType, by_value=True, required=True)
    checked = fields.Boolean(allow_none=True)
    name = fields.String(allow_none=False, required=True, validate=lambda x: 1 <= len(x.strip()) <= 255)
    user_id = fields.UUID(allow_none=False, required=True)

    @validates('name')
    def validate_name(self, value, **kwargs):
        """Validate and sanitize item name."""
        if not value or not value.strip():
            raise ValidationError("Item name cannot be empty")
        if len(value) > 255:
            raise ValidationError("Item name cannot exceed 255 characters")
        # Check for potentially malicious patterns
        if re.search(r'[<>"\';]', value):
            raise ValidationError("Item name contains invalid characters")
    
    @validates('category')
    def validate_category(self, value:str, **kwargs):
        """Validate category is a valid enum value."""
        if value not in [cat for cat in ItemCategoryType]:
            raise ValidationError(
                f"Invalid category. Must be one of: {', '.join([cat.value for cat in ItemCategoryType])}"
            )

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)
    