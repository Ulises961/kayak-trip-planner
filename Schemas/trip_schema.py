from marshmallow import Schema, fields, post_load
from Models.trip import Trip
from Schemas.itinerary_shema import ItinerarySchema
from Schemas.inventory_schema import InventorySchema

class TripSchema(Schema):
    """ 
    Trip Schema
    used for loading/dumping Trip entities
    """
    
    id   = fields.Integer(allow_none=True)
    inventory = fields.Nested(InventorySchema(exclude=['trip_id']))
    itinerary = fields.Nested(ItinerarySchema(exclude=['trip_id']))


    @post_load
    def make_trip(self, data, **kwargs):
        return Trip(**data)