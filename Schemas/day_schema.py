from marshmallow import Schema, fields, post_load, pre_load, validates, ValidationError
from Models.day import Day
from Schemas.point_schema import PointSchema
from Schemas.sea_schema import SeaSchema
from Schemas.weather_schema import WeatherSchema
from datetime import datetime, timedelta

class DaySchema(Schema):
    """ 
    Day Schema
    used for loading/dumping Day entities
    """
    id = fields.Integer(dump_only=True)  # ID is auto-generated, not loaded
    day_number = fields.Integer(allow_none=False, required=True, validate=lambda x: 1 <= x <= 365)
    itinerary_id = fields.Integer(allow_none=True)
    date = fields.Date('%Y-%m-%d', allow_none=False, required=True)
    points = fields.List(fields.Nested(PointSchema), allow_none=True, validate=lambda x: x is None or len(x) <= 100)
    sea = fields.Nested(SeaSchema, allow_none=True)
    weather = fields.Nested(WeatherSchema, allow_none=True)

    @pre_load
    def remove_id(self, data, **kwargs):
        """Remove id field if present - it's auto-generated."""
        if 'id' in data:
            data.pop('id')
        return data

    @validates('day_number')
    def validate_day_number(self, value,  **kwargs):
        """Validate day number is within reasonable range."""
        if value < 1:
            raise ValidationError("Day number must be at least 1")
        if value > 365:
            raise ValidationError("Day number cannot exceed 365")
    
    @validates('date')
    def validate_date(self, value,  **kwargs):
        """Validate date is not too far in the past or future."""
        if value:
            min_date = datetime.now().date() - timedelta(days=365*10)  # 10 years ago
            max_date = datetime.now().date() + timedelta(days=365*10)  # 10 years ahead
            if value < min_date:
                raise ValidationError("Date cannot be more than 10 years in the past")
            if value > max_date:
                raise ValidationError("Date cannot be more than 10 years in the future")
    
    @validates('points')
    def validate_points(self, value,  **kwargs):
        """Validate points list doesn't exceed reasonable limits."""
        if value is not None and len(value) > 100:
            raise ValidationError("A day cannot have more than 100 points")

    @post_load
    def make_day(self, data, **kwargs): 
            return Day(**data)