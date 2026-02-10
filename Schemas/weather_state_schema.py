from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.weather_state import WeatherState
import bleach
import re


class WeatherStateSchema(Schema):
    """ 
    Weather State Schema
    used for loading/dumping Weather State entities
    """

    day_id = fields.Integer(allow_none=False, required=True)
    time = fields.Time('%H:%M:%S', allow_none=False, required=True)
    temperature = fields.Float(allow_none=True, validate=lambda x: x is None or (-90 <= x <= 60))
    precipitation = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 500))
    wind_direction = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 360))
    wind_force = fields.Float(allow_none=True, validate=lambda x: x is None or (0 <= x <= 200))
    cloud = fields.String(allow_none=True, validate=lambda x: x is None or len(x.strip()) <= 50)

    @validates('temperature')
    def validate_temperature(self, value):
        """Validate temperature is within reasonable range (Celsius)."""
        if value is not None:
            if value < -90:
                raise ValidationError("Temperature cannot be below -90°C")
            if value > 60:
                raise ValidationError("Temperature cannot exceed 60°C")
    
    @validates('precipitation')
    def validate_precipitation(self, value):
        """Validate precipitation is within reasonable range (mm)."""
        if value is not None:
            if value < 0:
                raise ValidationError("Precipitation cannot be negative")
            if value > 500:
                raise ValidationError("Precipitation cannot exceed 500mm")
    
    @validates('wind_direction')
    def validate_wind_direction(self, value):
        """Validate wind direction is a valid compass bearing."""
        if value is not None:
            if value < 0 or value > 360:
                raise ValidationError("Wind direction must be between 0 and 360 degrees")
    
    @validates('wind_force')
    def validate_wind_force(self, value):
        """Validate wind force is within reasonable range (km/h)."""
        if value is not None:
            if value < 0:
                raise ValidationError("Wind force cannot be negative")
            if value > 200:
                raise ValidationError("Wind force cannot exceed 200 km/h")
    
    @validates('cloud')
    def validate_cloud(self, value):
        """Validate and sanitize cloud description."""
        if value is not None:
            # Sanitize HTML/script tags
            sanitized = bleach.clean(value.strip(), tags=[], strip=True)
            if len(sanitized) > 50:
                raise ValidationError("Cloud description cannot exceed 50 characters")
            if re.search(r'[<>"\';]', sanitized):
                raise ValidationError("Cloud description contains invalid characters")


    @post_load
    def make_weather_state(self, data, **kwargs):
        return WeatherState(**data)