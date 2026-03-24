"""
Log Service - Business logic for log operations.
"""
import logging
from typing import List, cast
from uuid import UUID
from flask import g
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import selectinload

from Models.log import Log
from Models.user import User
from Schemas.log_schema import LogSchema
from Api.database import db

logger = logging.getLogger(__name__)


class LogService:
    """Service class for Log-related business logic."""

    @staticmethod
    def get_log_by_id(id: str) -> Log:
        """
        Retrieve a log by its ID.

        Args:
            log_id: The ID of the log to retrieve

        Returns:
            Log object if found

        Raises:
            NoResultFound: If log doesn't exist
        """
        log = db.session.query(Log).filter_by(id=UUID(id)).first()
        if not log:
            logger.warning(f"Log with id {id} not found")
            raise NoResultFound(f"Log {id} not found in database")
        return log

    @staticmethod
    def get_logs_by_user(user_id: str) -> List[Log]:
        """
        Retrieve all logs created by a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of Log objects
        """
        user = db.session.query(User).options(selectinload(User.logs)).filter_by(id=UUID(user_id)).first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found in db")
        logger.info(f"Found {len(user.logs)} logs for user {user_id}")
        return user.logs

    @staticmethod
    def create_log(log_data: dict) -> Log:
        """
        Create a new log.

        Args:
            log_data: Dictionary containing log information

        Returns:
            Created Log object

        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info("Creating new log")
        log_data.setdefault("user_id", g.current_user_id)
        log = cast(Log, LogSchema().load(log_data))
        db.session.add(log)
        db.session.commit()

        db.session.refresh(log)
        logger.info(f"Log {log.id} created successfully")
        return log

    @staticmethod
    def update_log(id: str, log_data: dict) -> Log:
        """
        Update an existing log.

        Args:
            log_id: The ID of the log to update
            log_data: Dictionary containing log information

        Returns:
            Updated Log object

        Raises:
            ValidationError: If data is invalid
            NoResultFound: If log doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Verify log exists
        existing_log = LogService.get_log_by_id(id)
        if not existing_log:
            raise NoResultFound(f"Log with id {id} not found")
        logger.info(f"Updating log {id}")

        updated_log = LogSchema().load(log_data)

        try:
            merged_log = cast(Log, db.session.merge(updated_log))
            db.session.commit()
            db.session.refresh(merged_log)

            logger.info(f"Log {id} updated successfully")
            return merged_log

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error updating log {id}: {e}")
            raise

    @staticmethod
    def delete_log(id: str) -> None:
        """
        Delete a log by its ID.

        Args:
            log_id: The ID of the log to delete

        Raises:
            NoResultFound: If log doesn't exist
            IntegrityError: If log has references that prevent deletion
        """
        log = LogService.get_log_by_id(id)

        try:
            logger.info(f"Deleting log {id}")
            db.session.delete(log)
            db.session.commit()
            logger.info(f"Log {id} deleted successfully")

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting log {id}: {e}")
            raise IntegrityError(
                f"Cannot delete log {id} due to existing references",
                params=None,
                orig=e
            )

    @staticmethod
    def endorse_log(id: str, user_id: str) -> None:
        """
        Endorse a log entry.

        Args:
            log_id: The ID of the log to endorse
            user_id: The ID of the user endorsing the log

        Raises:
            NoResultFound: If log doesn't exist
        """
        from Models.user import User

        log = LogService.get_log_by_id(id)
        user = db.session.query(User).filter_by(id=UUID(user_id)).first()

        if not user:
            raise NoResultFound(f"User {user_id} not found")

        if user not in log.user_endorsed_logs:
            log.user_endorsed_logs.append(user)
            db.session.commit()
            logger.info(f"User {user_id} endorsed log {id}")
        else:
            logger.info(f"User {user_id} already endorsed log {id}")

    @staticmethod
    def unendorse_log(id: str, user_id: str) -> None:
        """
        Remove endorsement from a log entry.

        Args:
            log_id: The ID of the log to unendorse
            user_id: The ID of the user removing endorsement

        Raises:
            NoResultFound: If log doesn't exist
        """

        log = LogService.get_log_by_id(id)
        user = db.session.query(User).filter_by(id=UUID(user_id)).first()
        
        if not user:
            raise NoResultFound(f"User {user_id} not found")

        if user in log.user_endorsed_logs:
            log.user_endorsed_logs.remove(user)
            db.session.commit()
            logger.info(f"User {user_id} removed endorsement from log {id}")
        else:
            logger.info(f"User {user_id} hasn't endorsed log {id}")
    
    @staticmethod
    def get_endorsed_logs(user_id: str) -> List[Log]:
        """
        Retrieve all logs created by a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of Log objects
        """
        user = db.session.query(User).options(selectinload(User.endorsed_logs)).filter_by(id=UUID(user_id)).first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found in db")
        logger.info(f"Found {len(user.endorsed_logs)} logs for user {user_id}")
        return user.endorsed_logs
