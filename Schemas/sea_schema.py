from marshmallow import Schema, fields, post_load
from Models.sea import Sea
from Schemas.sea_state_schema import SeaStateSchema

class SeaSchema(Schema):
    """ 
    Sea Schema
    used for loading/dumping Sea entities
    """

    day_number   = fields.Integer(allow_none=False)
    itinerary_id = fields.Integer(allow_none=False)
    date         = fields.Date('%Y-%m-%d',allow_none=False)
    moon_phase   = fields.String(allow_none=True)
    high_tide    = fields.Time('%H:%M',allow_none=True)
    low_tide     = fields.Time('%H:%M',allow_none=True)
    sea_states  =  fields.List(fields.Nested(SeaStateSchema),allow_none=True)
    


    @post_load
    def make_sea(self, data, **kwargs):
        return Sea(**data)