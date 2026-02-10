from marshmallow import Schema, fields, post_load, validates, ValidationError, EXCLUDE
from Models.point import Point, PointType
from Api.database import db
from Schemas.image_schema import ImageSchema
import bleach
import re


class PointSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    """ 
    Point Schema
    used for loading/dumping Point entities
    """
    id = fields.Integer(allow_none=True)
    latitude = fields.Float(allow_none=True, validate=lambda x: x is None or (-90 <= x <= 90))
    longitude = fields.Float(allow_none=True, validate=lambda x: x is None or (-180 <= x <= 180))
    notes = fields.String(allow_none=True, validate=lambda x: x is None or len(x.strip()) <= 5000)
    type = fields.Enum(PointType, by_value=True, required=True)
    day_id = fields.Integer(allow_none=True)
    next = fields.Nested(lambda: PointSchema(), allow_none=True,
                         exclude=("next", "nearby"))
    nearby = fields.List(fields.Nested(lambda: PointSchema(
    ), allow_none=True, exclude=("next", "nearby")))
    images = fields.List(fields.Nested(ImageSchema, allow_none=True))

    @validates('type')
    def validate_type(self, value,  **kwargs):
        """Validate that point type is one of the allowed values."""
        valid_types_values = [t.value for t in PointType]
        valid_types =  [t for t in PointType]
        if value not in valid_types:
            raise ValidationError(
                f"Invalid point type. Must be one of: {', '.join(valid_types_values)}"
            )
    
    @validates('latitude')
    def validate_latitude(self, value,  **kwargs):
        """Validate latitude coordinates if provided."""
        if value is not None:
            if value < -90 or value > 90:
                raise ValidationError(
                    "Latitude must be between -90 and 90"
                )
    
    @validates('longitude')
    def validate_longitude(self, value,  **kwargs):
        """Validate longitude coordinates if provided."""
        if value is not None:
            if value < -180 or value > 180:
                raise ValidationError(
                    "Longitude must be between -180 and 180"
                )
    
    @validates('notes')
    def validate_notes(self, value,  **kwargs):
        """Validate and sanitize notes."""
        if value is not None:
            # Sanitize HTML but allow basic formatting
            sanitized = bleach.clean(
                value.strip(),
                tags=['p', 'br', 'strong', 'em', 'u'],
                strip=True
            )
            if len(sanitized) > 5000:
                raise ValidationError("Notes cannot exceed 5000 characters")

    @post_load
    def make_point(self, data, **kwargs):
        return Point(**data)
