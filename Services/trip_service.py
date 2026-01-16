"""
Trip Service - Business logic for trip operations.
"""
import logging
from typing import List, Optional
from sqlalchemy.exc import NoResultFound

from Models.trip import Trip
from Schemas.trip_schema import TripSchema
from Api.database import db

logger = logging.getLogger(__name__)


class TripService:
    """Service class for Trip-related business logic."""
    
    @staticmethod
    def get_trip_by_id(trip_id: int) -> Optional[Trip]:
        """
        Retrieve a trip by its ID.
        
        Args:
            trip_id: The ID of the trip to retrieve
            
        Returns:
            Trip object if found
            
        Raises:
            NoResultFound: If trip doesn't exist
        """
        trip = Trip.query.filter_by(id=trip_id).first()
        if not trip:
            logger.warning(f"Trip with id {trip_id} not found")
            raise NoResultFound(f"Trip {trip_id} not found in database")
        return trip
    
    @staticmethod
    def get_all_trips() -> List[Trip]:
        """
        Retrieve all trips from the database.
        
        Returns:
            List of all Trip objects
            
        Raises:
            NoResultFound: If no trips exist
        """
        trips = Trip.query.all()
        if not trips:
            logger.warning("No trips found in database")
            raise NoResultFound("No trips found in database")
        return trips
    
    @staticmethod
    def create_trip(trip_data: dict) -> Trip:
        """
        Create a new trip.
        
        Args:
            trip_data: Dictionary containing trip information
            
        Returns:
            Created Trip object
            
        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info(f"Creating new trip")
        trip: Trip = TripSchema().load(trip_data)  # type: ignore
        db.session.add(trip)
        db.session.commit()
        
        # Refresh to get relationships
        db.session.refresh(trip)
        logger.info(f"Trip {trip.id} created successfully")
        return trip
    
    @staticmethod
    def update_trip(trip_data: dict) -> Trip:
        """
        Update an existing trip.
        
        Args:
            trip_data: Dictionary containing trip information with ID
            
        Returns:
            Updated Trip object
            
        Raises:
            ValidationError: If data is invalid
            NoResultFound: If trip doesn't exist
        """
        trip: Trip = TripSchema().load(trip_data)  # type: ignore
        
        # Verify trip exists
        existing_trip = TripService.get_trip_by_id(trip.id)
        if not existing_trip:
            raise NoResultFound(f"Trip {trip.id} not found")
        
        logger.info(f"Updating trip {trip.id}")
        db.session.merge(trip)
        db.session.commit()
        
        updated_trip = TripService.get_trip_by_id(trip.id)
        if not updated_trip:
            raise NoResultFound(f"Trip {trip.id} not found after update")
        logger.info(f"Trip {trip.id} updated successfully")
        return updated_trip
    
    @staticmethod
    def delete_trip(trip_id: int) -> None:
        """
        Delete a trip by its ID.
        
        Args:
            trip_id: The ID of the trip to delete
            
        Raises:
            NoResultFound: If trip doesn't exist
        """
        trip = TripService.get_trip_by_id(trip_id)
        logger.info(f"Deleting trip {trip_id}")
        db.session.delete(trip)
        db.session.commit()
        logger.info(f"Trip {trip_id} deleted successfully")
    
    @staticmethod
    def get_trips_by_user(user_id: int) -> List[Trip]:
        """
        Retrieve all trips for a specific user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of Trip objects for that user
        """
        from Models.user import User
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise NoResultFound(f"User {user_id} not found")
        
        trips = user.trips
        logger.info(f"Found {len(trips)} trips for user {user_id}")
        return trips
