from marshmallow import Schema, fields, post_load
from Models.sea_state import SeaState
from Models.day import Day

class SeaStateSchema(Schema):
    """ 
    Sea State Schema
    used for loading/dumping Sea State entities
    """

    day_number = fields.Integer(allow_none=True)
    itinerary_id=fields.Integer(allow_none=False)
    date =fields.Date('dd-mm-yyyy',allow_none=False)
    time=fields.Time('hh:mm:ss',allow_none=True)
    wave_height=fields.Float(allow_none=False)
    wave_direction=fields.Float(allow_none=False)
    swell_direction=fields.Float(allow_none=False)
    swell_period=fields.Float(allow_none=False)


    @post_load
    def make_sea_state(self, data, **kwargs):
        return SeaState(**data)