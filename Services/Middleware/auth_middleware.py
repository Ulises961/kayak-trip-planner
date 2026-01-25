from functools import wraps
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Dict
import os
from flask import current_app,abort, g, request
from Models.user import User


class JWTService:

    @staticmethod
    def generate_token(payload: Dict[str, Any]) -> str:
        secret_key = current_app.config['JWT_SECRET_KEY']
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def generate_access_token(user_id: str, email: str, is_admin: bool) -> str:
        """Generates a JWT token with an expiration time."""
        payload = {
            'user_id': user_id,
            'email': email,
            'is_admin': is_admin,
            'token_type': 'access',
            'iat': datetime.now(timezone.utc),
            'exp':  datetime.now(timezone.utc) + timedelta(minutes=15) 
        }
        return JWTService.generate_token(payload)    

    @staticmethod
    def generate_refresh_token(user_id: str)-> str:
        payload = {
            'user_id': user_id,
            'token_type': 'refresh',
            'iat': datetime.now(timezone.utc),
            'exp':  datetime.now(timezone.utc) + timedelta(days=30)
        }

        return JWTService.generate_token(payload)

    @staticmethod
    def decode_token(token: str) -> Dict:
        """Decodes a JWT token and returns the payload if valid."""
        secret_key = current_app.config['JWT_SECRET_KEY']
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
        
    @staticmethod
    def refresh_token(refresh_token: str) -> str:
        """Refreshes a JWT token by generating a new one with extended expiration."""
        payload = JWTService.decode_token(refresh_token)
        if not payload:
            raise ValueError("Invalid token, cannot refresh")
        if payload['token_type'] != 'access':
            raise ValueError("Only access tokens can be refreshed")
        
        user = User.query.get(payload['user_id'])

        if not user:
            raise ValueError("User not found")
        return JWTService.generate_access_token(user.user_id, user.email, user.is_admin)
    
    @staticmethod
    def verify_token(token: str, token_type: str = 'access') -> Optional[Dict]:
        """
        Verify token and check its type.
        
        Args:
            token: JWT token string
            token_type: Expected token type ('access' or 'refresh')
            
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = JWTService.decode_token(token)
            if not payload:
                raise ValueError("Failed token decoding")
            
            if payload.get('token_type') != token_type:
                return None
                
            return payload
        except ValueError:
            return None
        
    @staticmethod
    def authenticate_admin(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return abort(HTTPStatus.FORBIDDEN)
            auth_token = auth_header.split(" ")[1]
            data = JWTService.verify_token(auth_token)
            if not data:
                return abort(HTTPStatus.UNAUTHORIZED)
            user = User.query.filter_by(id=data["user_id"]).first()

            if not (user and user.active and user.admin):
                return abort(HTTPStatus.UNAUTHORIZED)
            return f(user, *args, **kwargs)

        return decorated_function
    
    @staticmethod
    def authenticate_restful(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            auth_header = request.headers.get("Authorization", None)
            if not auth_header:
                    abort(HTTPStatus.FORBIDDEN, description="Valid token missing") 
            try:
                    data = JWTService.verify_token(auth_header)
                    if not data:
                        abort(401, description="Invalid token")
                    
                    user = User.query.filter_by(public_id=data["user_id"]).first()
                
                    if not user or not user.active:
                        return abort(HTTPStatus.UNAUTHORIZED)

                    g.current_user_id = user.public_id
                    g.current_user_mail = user.mail

            except:
                raise ValueError("Invalid token")
        
            return f(*args, **kwargs)
        return decorator

   
    
