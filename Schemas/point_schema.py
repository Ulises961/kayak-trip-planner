from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.point import Point, PointType
from Api.database import db
from Schemas.image_schema import ImageSchema


class PointSchema(Schema):
    """ 
    Point Schema
    used for loading/dumping Point entities
    """
    id = fields.Integer(allow_none=False)
    gps = fields.Float(allow_none=True)
    notes = fields.String(allow_none=True)
    type = fields.Enum(PointType, by_value=True)
    day_id = fields.Integer(allow_none=True)
    previous = fields.Nested(lambda: PointSchema(
    ), allow_none=True, exclude=("previous", "next", "nearby"))
    next = fields.Nested(lambda: PointSchema(), allow_none=True,
                         exclude=("previous", "next", "nearby"))
    nearby = fields.List(fields.Nested(lambda: PointSchema(
    ), allow_none=True, exclude=("previous", "next", "nearby")))
    images = fields.List(fields.Nested(ImageSchema, allow_none=True))

    @validates('type')
    def validate_type(self, value):
        """Validate that point type is one of the allowed values."""
        valid_types = [t.value for t in PointType]
        if value not in valid_types:
            raise ValidationError(
                f"Invalid point type. Must be one of: {', '.join(valid_types)}"
            )
    
    @validates('gps')
    def validate_gps(self, value):
        """Validate GPS coordinates if provided."""
        if value is not None:
            if value < -180 or value > 180:
                raise ValidationError(
                    "GPS coordinates must be between -180 and 180"
                )
    
    @validates('notes')
    def validate_notes(self, value):
        """Validate notes length."""
        if value is not None and len(value) > 5000:
            raise ValidationError(
                "Notes cannot exceed 5000 characters"
            )

    @post_load
    def make_point(self, data, **kwargs):
        return Point(**data)
