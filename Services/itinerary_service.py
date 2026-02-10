"""
Itinerary Service - Business logic for itinerary operations.
"""
import logging
from typing import List, Optional, cast
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import selectinload
from Models.user_has_itinerary import user_has_itinerary
from Models.itinerary import Itinerary
from Models.user import User
from Schemas.itinerary_shema import ItinerarySchema
from Api.database import db

logger = logging.getLogger(__name__)


class ItineraryService:
    """Service class for Itinerary-related business logic."""

    @staticmethod
    def get_itinerary_by_id(itinerary_id: str) -> Itinerary:
        """
        Retrieve an itinerary by its public ID.

        Args:
            itinerary_id: The public ID of the itinerary to retrieve

        Returns:
            Itinerary object if found

        Raises:
            NoResultFound: If itinerary doesn't exist
        """
        itinerary = db.session.query(Itinerary).options(selectinload(Itinerary.days)).filter_by(public_id=itinerary_id).first()
        if not itinerary:
            logger.warning(f"Itinerary with id {itinerary_id} not found")
            raise NoResultFound(f"Itinerary {itinerary_id} not found in database")
        return itinerary

    @staticmethod
    def get_itineraries_by_user(user_id: str) -> List[Itinerary]:
        """
        Retrieve all itineraries for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of Itinerary objects
        """
        user = db.session.query(User).options(selectinload(User.itineraries)).filter_by(public_id=user_id).first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found in db")
        
        logger.info(f"Found {len(user.itineraries)} itineraries for user {user_id}")

        return user.itineraries

    @staticmethod
    def create_itinerary(itinerary_data: dict) -> Itinerary:
        """
        Create a new itinerary.

        Args:
            itinerary_data: Dictionary containing itinerary information

        Returns:
            Created Itinerary object

        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info("Creating new itinerary")
        itinerary = cast(Itinerary, ItinerarySchema().load(itinerary_data))
        db.session.add(itinerary)
        db.session.commit()

        db.session.refresh(itinerary)
        logger.info(f"Itinerary {itinerary.id} created successfully")
        return itinerary

    @staticmethod
    def update_itinerary(public_id: str, itinerary_data: dict) -> Itinerary:
        """
        Update an existing itinerary.

        Args:
            itinerary_id: The ID of the itinerary to update
            itinerary_data: Dictionary containing itinerary information

        Returns:
            Updated Itinerary object

        Raises:
            ValidationError: If data is invalid
            NoResultFound: If itinerary doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Verify itinerary exists
        existing_itinerary = ItineraryService.get_itinerary_by_id(public_id)
        
        if not existing_itinerary:
            raise NoResultFound(f"Itinerary with id {public_id} not found")
        
        logger.info(f"Updating itinerary {public_id}")

        try:
            # Load and validate the new data (schema will resolve public_id to db id)
            updated_itinerary = cast(Itinerary, ItinerarySchema().load(itinerary_data))

            # Update scalar fields
            existing_itinerary.is_public = updated_itinerary.is_public
            existing_itinerary.total_miles = updated_itinerary.total_miles
            existing_itinerary.expected_total_miles = updated_itinerary.expected_total_miles
            
            # Delete old days and expunge them from session to avoid conflicts
            for day in list(existing_itinerary.days):
                db.session.delete(day)
            db.session.flush()
            
           # Add new days
            logger.info(f"Adding {len(updated_itinerary.days)} new days")
            for day in updated_itinerary.days:
                logger.info(f"Adding day {day.day_number} with date {day.date}")
                day.itinerary_id = existing_itinerary.id
                existing_itinerary.days.append(day)
            
            db.session.commit()
            db.session.refresh(existing_itinerary)

            logger.info(f"Itinerary {public_id} updated successfully")
            return existing_itinerary

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error updating itinerary {public_id}: {e}")
            raise

    @staticmethod
    def delete_itinerary(public_id: str) -> None:
        """
        Delete an itinerary by its ID.

        Args:
            itinerary_id: The ID of the itinerary to delete

        Raises:
            NoResultFound: If itinerary doesn't exist
            IntegrityError: If itinerary has references that prevent deletion
        """
        itinerary = ItineraryService.get_itinerary_by_id(public_id)

        try:
            logger.info(f"Deleting itinerary {public_id}")
            db.session.delete(itinerary)
            db.session.commit()
            logger.info(f"Itinerary {public_id} deleted successfully")

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting itinerary {public_id}: {e}")
            raise IntegrityError(
                f"Cannot delete itinerary {public_id} due to existing references",
                params=None,
                orig=e
            )
