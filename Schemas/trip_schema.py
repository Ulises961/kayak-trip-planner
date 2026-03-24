from marshmallow import Schema, fields, post_load, post_dump, pre_load, validates, ValidationError
from Models.trip import Trip
from Schemas.base_schema import BaseSchema
from Schemas.itinerary_shema import ItinerarySchema
from Schemas.inventory_schema import InventorySchema
import uuid


class TripSchema(BaseSchema):
    """ 
    Trip Schema
    used for loading/dumping Trip entities
    """
    # Expose id as 'id' in API via data_key
    inventory = fields.Nested(InventorySchema(exclude=['trip_id']), allow_none=True)
    itinerary = fields.Nested(ItinerarySchema(exclude=['trip_id']), allow_none=True)
    pending_travellers = fields.Nested('UserSchema', exclude=['pwd', 'trips', 'itineraries', 'inventories', 'items', 'endorsed_logs', 'logs'], many=True, allow_none=True)
    travellers = fields.Nested('UserSchema', exclude=['pwd', 'trips', 'itineraries', 'inventories', 'items', 'endorsed_logs', 'logs'], many=True, allow_none=True, validate=lambda x: x is None or len(x) <= 50)
    is_draft = fields.Boolean(allow_none=True)
    description = fields.String(allow_none=True)
    destination = fields.String(allow_none=True)
    date_from = fields.Date(allow_none=True)
    date_to = fields.Date(allow_none=True)
    

    @validates('travellers')
    def validate_travellers(self, value, **kwargs):
        """Validate travellers list doesn't exceed reasonable limits."""
        if value is not None and len(value) > 50:
            raise ValidationError("A trip cannot have more than 50 travellers")
    
    @post_load
    def make_trip(self, data, **kwargs):
        return Trip(**data)
    
