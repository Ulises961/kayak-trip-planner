"""
Itinerary Service - Business logic for itinerary operations.
"""
import logging
from typing import List, Optional, cast
from sqlalchemy.exc import NoResultFound, IntegrityError

from Models.itinerary import Itinerary
from Schemas.itinerary_shema import ItinerarySchema
from Api.database import db

logger = logging.getLogger(__name__)


class ItineraryService:
    """Service class for Itinerary-related business logic."""

    @staticmethod
    def get_itinerary_by_id(itinerary_id: int) -> Itinerary:
        """
        Retrieve an itinerary by its ID.

        Args:
            itinerary_id: The ID of the itinerary to retrieve

        Returns:
            Itinerary object if found

        Raises:
            NoResultFound: If itinerary doesn't exist
        """
        itinerary = db.session.get(Itinerary, itinerary_id)
        if not itinerary:
            logger.warning(f"Itinerary with id {itinerary_id} not found")
            raise NoResultFound(f"Itinerary {itinerary_id} not found in database")
        return itinerary

    @staticmethod
    def get_itineraries_by_user(user_id: int) -> List[Itinerary]:
        """
        Retrieve all itineraries for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of Itinerary objects
        """
        itineraries = db.session.query(Itinerary).filter_by(user_id=user_id).all()
        logger.info(f"Found {len(itineraries)} itineraries for user {user_id}")
        return itineraries

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
    def update_itinerary(itinerary_id: int, itinerary_data: dict) -> Itinerary:
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
        existing_itinerary = ItineraryService.get_itinerary_by_id(itinerary_id)
        if not existing_itinerary:
            raise NoResultFound(f"Itinerary with id {itinerary_id} not found")
        logger.info(f"Updating itinerary {itinerary_id}")

        updated_itinerary = ItinerarySchema().load(itinerary_data)

        try:
            merged_itinerary = cast(Itinerary, db.session.merge(updated_itinerary))
            db.session.commit()
            db.session.refresh(merged_itinerary)

            logger.info(f"Itinerary {itinerary_id} updated successfully")
            return merged_itinerary

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error updating itinerary {itinerary_id}: {e}")
            raise

    @staticmethod
    def delete_itinerary(itinerary_id: int) -> None:
        """
        Delete an itinerary by its ID.

        Args:
            itinerary_id: The ID of the itinerary to delete

        Raises:
            NoResultFound: If itinerary doesn't exist
            IntegrityError: If itinerary has references that prevent deletion
        """
        itinerary = ItineraryService.get_itinerary_by_id(itinerary_id)

        try:
            logger.info(f"Deleting itinerary {itinerary_id}")
            db.session.delete(itinerary)
            db.session.commit()
            logger.info(f"Itinerary {itinerary_id} deleted successfully")

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting itinerary {itinerary_id}: {e}")
            raise IntegrityError(
                f"Cannot delete itinerary {itinerary_id} due to existing references",
                params=None,
                orig=e
            )
