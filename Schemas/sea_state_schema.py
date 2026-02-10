from marshmallow import Schema, fields, post_load, validates, ValidationError
from Models.sea_state import SeaState
from Models.day import Day

class SeaStateSchema(Schema):
    """ 
    Sea State Schema
    used for loading/dumping Sea State entities
    """

    day_id = fields.Integer(allow_none=True)
    time = fields.Time('%H:%M:%S', allow_none=True)
    wave_height = fields.Float(allow_none=False, required=True, validate=lambda x: 0 <= x <= 30)
    wave_direction = fields.Float(allow_none=False, required=True, validate=lambda x: 0 <= x <= 360)
    swell_direction = fields.Float(allow_none=False, required=True, validate=lambda x: 0 <= x <= 360)
    swell_period = fields.Float(allow_none=False, required=True, validate=lambda x: 0 <= x <= 30)

    @validates('wave_height')
    def validate_wave_height(self, value):
        """Validate wave height is within reasonable range."""
        if value < 0:
            raise ValidationError("Wave height cannot be negative")
        if value > 30:
            raise ValidationError("Wave height cannot exceed 30 meters")
    
    @validates('wave_direction')
    def validate_wave_direction(self, value):
        """Validate wave direction is a valid compass bearing."""
        if value < 0 or value > 360:
            raise ValidationError("Wave direction must be between 0 and 360 degrees")
    
    @validates('swell_direction')
    def validate_swell_direction(self, value):
        """Validate swell direction is a valid compass bearing."""
        if value < 0 or value > 360:
            raise ValidationError("Swell direction must be between 0 and 360 degrees")
    
    @validates('swell_period')
    def validate_swell_period(self, value):
        """Validate swell period is within reasonable range."""
        if value < 0:
            raise ValidationError("Swell period cannot be negative")
        if value > 30:
            raise ValidationError("Swell period cannot exceed 30 seconds")


    @post_load
    def make_sea_state(self, data, **kwargs):
        return SeaState(**data)