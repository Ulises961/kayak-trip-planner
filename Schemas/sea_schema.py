from marshmallow import Schema, fields, post_load
from Models.sea import Sea


class SeaSchema(Schema):
    """ 
    Sea Schema
    used for loading/dumping Sea entities
    """

    day_number   = fields.Integer(allow_none=False)
    itinerary_id = fields.Integer(allow_none=False)
    date         = fields.Date('dd-mm-yy',allow_none=False)
    moon_phase   = fields.String(allow_none=True)
    high_tide    = fields.Time('hh:mm',allow_none=True)
    low_tide     = fields.Time('hh:mm',allow_none=True)
    


    @post_load
    def make_sea(self, data, **kwargs):
        return Sea(**data)