from typing import Optional
import logging

from flask_bcrypt import check_password_hash
from sqlalchemy.exc import NoResultFound, IntegrityError

from Models.user import User
from Api.database import db
from Schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def authenticate_user(mail: str, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by credentials.

        Args:
            mail: User's email address
            username: User's username
            password: Plain-text password to verify

        Returns:
            User object if credentials are valid, None if password doesn't match

        Raises:
            NoResultFound: If no user exists with the given mail/username
        """
        user = db.session.query(User).filter_by(mail=mail, username=username).first()
        if not user:
            raise NoResultFound(f"User with mail {mail} not found")
        if check_password_hash(user.pwd, password):
            return user
        return None

    @staticmethod
    def register_user(user_json: dict) -> User:
        """
        Register a new user.

        Args:
            user_json: Dictionary containing user registration data

        Returns:
            The newly created and verified User object

        Raises:
            IntegrityError: If a user with the same username or mail already exists
            ValueError: If user was not correctly persisted after creation
        """
        username = user_json.get("username")
        mail = user_json.get("mail")

        existing = db.session.query(User).filter(
            (User.username == username) | (User.mail == mail)
        ).first()
        if existing:
            raise IntegrityError(statement="User already present", params=None, orig=Exception())

        user = UserSchema().load(user_json)
        db.session.add(user)
        db.session.commit()

        user = db.session.query(User).filter_by(mail=mail).first()
        if not user:
            raise ValueError("User generated incorrectly")

        logger.info(f"New user registered: {user.username}")
        return user
