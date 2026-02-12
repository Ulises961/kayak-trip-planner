from typing import Any, Dict, Optional, cast
from Models.image import Image
from Models.user import User
from Api.database import db
from sqlalchemy.exc import NoResultFound, IntegrityError
from flask_bcrypt import generate_password_hash
import logging

from Schemas.image_schema import ImageSchema

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def get_user_by_id(id: str) -> User:
        user: Optional[User] = db.session.query(User).filter_by(public_id=id).first()
        if not user:
            raise NoResultFound(f"User with id {id} not found in db")
        return user
    
    @staticmethod
    def update_user(id: str, user_json: Dict[str, Any]) -> User:
        """
        Update an existing user.
        
        Args:
            id: The ID of the user to update
            user_json: Dictionary containing user data to update
            
        Returns:
            Updated User object
            
        Raises:
            NoResultFound: If user doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Verify user exists
        saved_user = db.session.query(User).filter_by(public_id=id).first()
        if not saved_user:
            raise NoResultFound(f"User with id {id} not found in db")
        
        try:
            # Update fields directly on the existing user object
            if 'mail' in user_json:
                saved_user.mail = user_json['mail']
            if 'name' in user_json:
                saved_user.name = user_json['name']
            if 'surname' in user_json:
                saved_user.surname = user_json['surname']
            if 'phone' in user_json:
                saved_user.phone = user_json['phone']
            if 'username' in user_json:
                saved_user.username = user_json['username']
            if 'pwd' in user_json:
                saved_user.pwd = generate_password_hash(user_json['pwd']).decode("UTF-8")
            if 'admin' in user_json:
                saved_user.admin = user_json['admin']
            if 'image' in user_json:
                if image:= user_json.get("image", None) is None:
                    saved_user.image = None
                else:
                    image = cast(Image, ImageSchema().load(user_json['image']))
                    saved_user.image = image
            db.session.commit()
            
            # Refresh to get latest state from database
            db.session.refresh(saved_user)
            return saved_user
            
        except IntegrityError as e:
            db.session.rollback()
            raise IntegrityError(f"Error while updating user with id {id}: {str(e)}", params=None, orig=e)
        
    @staticmethod
    def delete_user(id: str) -> None:
        """
        Delete a user by ID.
        
        Args:
            id: The ID of the user to delete
            
        Raises:
            NoResultFound: If user doesn't exist
            IntegrityError: If user has foreign key references that prevent deletion
        """
        saved_user = db.session.query(User).filter_by(public_id=id).first()
        if not saved_user:
            raise NoResultFound(f"User with id {id} not found")
        
        try:
            db.session.delete(saved_user)
            db.session.commit()
            logger.info(f"User with id {id} deleted successfully")
            
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting user {id}: {e}")
            raise IntegrityError(
                f"Cannot delete user {id} due to existing references", 
                params=None, 
                orig=e
            )
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Unexpected error deleting user {id}")
            raise