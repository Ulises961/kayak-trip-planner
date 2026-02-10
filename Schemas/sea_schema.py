from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.sea import Sea
from Schemas.sea_state_schema import SeaStateSchema
import bleach
import re

class SeaSchema(Schema):
    """ 
    Sea Schema
    used for loading/dumping Sea entities
    """

    day_id = fields.Integer(allow_none=False, required=True)
    moon_phase = fields.String(allow_none=True, validate=lambda x: x is None or len(x.strip()) <= 50)
    high_tide = fields.Time('%H:%M', allow_none=True)
    low_tide = fields.Time('%H:%M', allow_none=True)
    sea_states = fields.List(fields.Nested(SeaStateSchema), allow_none=True, validate=lambda x: x is None or len(x) <= 24)

    @validates('moon_phase')
    def validate_moon_phase(self, value):
        """Validate and sanitize moon phase."""
        if value is not None:
            # Sanitize HTML/script tags
            sanitized = bleach.clean(value.strip(), tags=[], strip=True)
            if len(sanitized) > 50:
                raise ValidationError("Moon phase description cannot exceed 50 characters")
            if re.search(r'[<>"\';]', sanitized):
                raise ValidationError("Moon phase contains invalid characters")
    
    @validates('sea_states')
    def validate_sea_states(self, value):
        """Validate sea states list doesn't exceed 24 entries (hourly)."""
        if value is not None and len(value) > 24:
            raise ValidationError("Sea states cannot have more than 24 entries per day")
    


    @post_load
    def make_sea(self, data, **kwargs):
        return Sea(**data)