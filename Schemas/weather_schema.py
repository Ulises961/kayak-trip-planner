from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.weather import Weather
from Schemas.weather_state_schema import WeatherStateSchema
import bleach
import re

class WeatherSchema(Schema):
    """ 
    Weather Schema
    used for loading/dumping Weather entities
    """

    day_id = fields.Integer(allow_none=False, required=True)
    model = fields.String(allow_none=False, required=True, validate=lambda x: 1 <= len(x.strip()) <= 100)
    weather_states = fields.List(fields.Nested(WeatherStateSchema), allow_none=True, validate=lambda x: x is None or len(x) <= 24)

    @validates('model')
    def validate_model(self, value):
        """Validate and sanitize weather model name."""
        if not value or not value.strip():
            raise ValidationError("Weather model cannot be empty")
        # Sanitize HTML/script tags
        sanitized = bleach.clean(value.strip(), tags=[], strip=True)
        if len(sanitized) > 100:
            raise ValidationError("Weather model name cannot exceed 100 characters")
        if re.search(r'[<>"\';]', sanitized):
            raise ValidationError("Weather model contains invalid characters")
    
    @validates('weather_states')
    def validate_weather_states(self, value):
        """Validate weather states list doesn't exceed 24 entries (hourly)."""
        if value is not None and len(value) > 24:
            raise ValidationError("Weather states cannot have more than 24 entries per day")
    
    @post_load
    def make_weather(self, data, **kwargs):
        return Weather(**data)