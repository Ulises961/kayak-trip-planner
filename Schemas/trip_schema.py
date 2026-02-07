from marshmallow import Schema, fields, post_load, post_dump, pre_load, validates, ValidationError
from Models.trip import Trip
from Schemas.itinerary_shema import ItinerarySchema
from Schemas.inventory_schema import InventorySchema
import uuid


class TripSchema(Schema):
    """ 
    Trip Schema
    used for loading/dumping Trip entities
    """
    # Expose public_id as 'id' in API via data_key
    public_id = fields.String(data_key='id', dump_only=True)
    inventory = fields.Nested(InventorySchema(exclude=['trip_id']), allow_none=True)
    itinerary = fields.Nested(ItinerarySchema(exclude=['trip_id']), allow_none=True)
    pending_travellers = fields.Nested('UserSchema', exclude=['pwd', 'trips', 'itineraries', 'inventories', 'items', 'endorsed_logs', 'logs'], many=True, allow_none=True)
    travellers = fields.Nested('UserSchema', exclude=['pwd', 'trips', 'itineraries', 'inventories', 'items', 'endorsed_logs', 'logs'], many=True, allow_none=True, validate=lambda x: x is None or len(x) <= 50)
    is_draft = fields.Boolean(allow_none=True)

    @pre_load
    def handle_id_input(self, data, **kwargs):
        """Convert 'id' from API to 'public_id' for model."""
        if 'id' in data:
            data['public_id'] = data.pop('id')
        return data

    @validates('travellers')
    def validate_travellers(self, value, **kwargs):
        """Validate travellers list doesn't exceed reasonable limits."""
        if value is not None and len(value) > 50:
            raise ValidationError("A trip cannot have more than 50 travellers")
    
    @post_load
    def make_trip(self, data, **kwargs):
        return Trip(**data)
    
