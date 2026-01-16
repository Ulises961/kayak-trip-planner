import logging
from flask_restful import Resource
from flask import request
from Schemas.trip_schema import TripSchema
from Services.trip_service import TripService

logger = logging.getLogger(__name__)

TRIP_ENDPOINT = "/api/trip"

class TripResource(Resource):
    """RESTful resource for Trip operations."""
    
    def get(self):
        """
        TripResource GET method. Retrieves trip(s) by ID or all trips.
        
        Returns:
            JSON response with trip data and 200 status code
        """
        id = request.args.get('id')
        if id:
            logger.info(f"Retrieving trip with id {id}")
            trip = TripService.get_trip_by_id(int(id))
            return TripSchema().dump(trip), 200
        else:
            logger.info("Retrieving all trips in db")
            trips = TripService.get_all_trips()
            return [TripSchema().dump(trip) for trip in trips], 200
        
        
    def post(self):
        """
        TripResource POST method. Adds a new trip to the database.

        Returns:
            JSON response with created trip and 201 status code
        """
        trip_data = request.get_json()
        trip = TripService.create_trip(trip_data)
        return TripSchema().dump(trip), 201

    def put(self):
        """
        TripResource PUT method. Updates an existing trip.
        
        Returns:
            JSON response with updated trip and 200 status code
        """
        logger.info(f"Update trip {request.get_json()} in db")
        trip_data = request.get_json()
        trip = TripService.update_trip(trip_data)
        return TripSchema().dump(trip), 200

    def delete(self):
        """
        TripResource DELETE method. Deletes a trip by ID.
        
        Returns:
            Success message and 200 status code
        """
        id = request.args.get('id')
        logger.info(f"Deleting trip {id}")
        TripService.delete_trip(int(id))
        return {"message": "Deletion successful"}, 200
