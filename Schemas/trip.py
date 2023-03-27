from marshmallow import Schema, fields, post_load
from Models.trip import Trip


class TripSchema(Schema):
    """ 
    Trip Schema
    used for loading/dumping Trip entities
    """

    id   = fields.Integer(allow_none=False)
    inventory = fields.Integer(allow_none=False)
    itinerary = fields.Integer(allow_none=False)


    @post_load
    def make_trip(self, data, **kwargs):
        return Trip(**data)