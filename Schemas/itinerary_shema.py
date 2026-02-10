from flask import g
from marshmallow import Schema, fields, post_dump, post_load, pre_load, validates, ValidationError
from Models.itinerary import Itinerary
from Models.trip import Trip
from Schemas.day_schema import DaySchema
from Api.database import db
from sqlalchemy.exc import NoResultFound


class ItinerarySchema(Schema):
    """
    Itinerary Schema
    used for loading/dumping Itinerary entities
    """
    
    # Expose public_id as 'id' in API via data_key
    public_id = fields.String(data_key='id', dump_only=True)
    id = fields.Integer(load_only=True)  # Internal database ID for relationships
    is_public = fields.Boolean(load_default=False)
    total_miles = fields.Float(validate=lambda x: 0 <= x <= 50000, load_default=0)
    expected_total_miles = fields.Float(
        allow_none=True, validate=lambda x: x is None or (0 <= x <= 50000)
    )
    days = fields.List(
        fields.Nested(DaySchema),
        allow_none=True,
        metadata={"exclude": ["itinerary_id"]},
        validate=lambda x: x is None or len(x) <= 365,
    )
    trip_id = fields.Integer(allow_none=True, required=False)
    user_id = fields.Integer(allow_none=True)

    @validates("total_miles")
    def validate_total_miles(self, value, **kwargs):
        """Validate total miles is within reasonable range."""
        if value < 0:
            raise ValidationError("Total miles cannot be negative")
        if value > 50000:
            raise ValidationError("Total miles cannot exceed 50,000")

    @validates("expected_total_miles")
    def validate_expected_total_miles(self, value, **kwargs):
        """Validate expected total miles is within reasonable range."""
        if value is not None:
            if value < 0:
                raise ValidationError("Expected total miles cannot be negative")
            if value > 50000:
                raise ValidationError("Expected total miles cannot exceed 50,000")

    @validates("days")
    def validate_days(self, value, **kwargs):
        """Validate days list doesn't exceed reasonable limits."""
        if value is not None and len(value) > 365:
            raise ValidationError("Itinerary cannot have more than 365 days")

    @pre_load
    def preprocess_data(self, data, **kwargs):
        """Resolve public_id to database id and resolve trip_id."""
        # If 'id' is provided (public_id), resolve it to database id
        if 'id' in data:
            itinerary = db.session.query(Itinerary).filter_by(public_id=data['id']).first()
            if itinerary:
                data['id'] = itinerary.id  # Replace public_id with database id
            else:
                # If not found, remove it (for new itineraries)
                data.pop('id')
        
        # Resolve trip public_id to internal id
        if "trip_id" in data:
            trip = db.session.query(Trip).filter_by(public_id=data["trip_id"]).first()
            if not trip:
                raise NoResultFound(f"No Trip with id {data['trip_id']} found")
            data["trip_id"] = trip.id

        if "user_id" in data:
            data["user_id"] = g.current_user_id
        
        return data

    @post_load
    def make_itinerary(self, data, **kwargs):
        return Itinerary(**data)
    
    @post_dump
    def mask_user_id(self, data, **kwargs):
        data['user_id'] = g.current_user_public_id
        return data
    
    @post_dump
    def mask_trip_id(self, data, **kwargs):
        if "trip_id" in data:
            trip = db.session.get(Trip, data["trip_id"])
            if not trip:
                raise NoResultFound("Error while serializing itinerary: Associated trip not found")
            data['trip_id'] = trip.public_id
        return data