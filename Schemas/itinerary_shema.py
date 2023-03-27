from marshmallow import Schema, fields, post_load
from Models.itinerary import Itinerary
from Models.day import Day

class ItinerarySchema(Schema):
    """ 
    Itinerary Schema
    used for loading/dumping Itinerary entities
    """

    id = fields.Integer(allow_none=True)
    is_public=fields.Booleean(allow_none=False)
    total_miles =fields.float(allow_none=False)
    expected_total_miles=fields.float(allow_none=True)
    days=fields.List(Day)
    trip_id=fields.Integer(allow_none=False)

    @post_load
    def make_itinerary(self, data, **kwargs):
        return Itinerary(**data)