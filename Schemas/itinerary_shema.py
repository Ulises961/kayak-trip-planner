from marshmallow import Schema, fields, post_load
from Models.itinerary import Itinerary
from Schemas.day_schema import DaySchema

class ItinerarySchema(Schema):
    """ 
    Itinerary Schema
    used for loading/dumping Itinerary entities
    """

    id = fields.Integer(allow_none=True)
    is_public=fields.Boolean(allow_none=False)
    total_miles =fields.Float(allow_none=False)
    expected_total_miles=fields.Float(allow_none=True)
    days=fields.List(fields.Nested(DaySchema), allow_none=True, metadata={"exclude":['itinerary_id']})
    trip_id=fields.Integer(allow_none=False)
    user_id=fields.Integer(allow_none=True)

    @post_load
    def make_itinerary(self, data, **kwargs):
        return Itinerary(**data)