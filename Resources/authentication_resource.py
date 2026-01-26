import logging
import uuid

from Models.user import User
from flask import abort, request, jsonify
from flask_bcrypt import check_password_hash
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError, NoResultFound
from Schemas.user_schema import UserSchema
from Api.database import db

from Services.Middleware.auth_middleware import JWTService

# It will print the name of this module when the main app is running

logger = logging.getLogger(__name__)
api = Blueprint("auth", __name__)

@api.route("/api/auth/login", methods=["POST"])
def login_user():
    
    post_data = request.get_json()
    logger.info(f"Post data {post_data}")
    
    if not post_data:
        raise ValueError("Missing request body")

    mail = post_data.get("mail", None)
    username = post_data.get("username")
    password = post_data.get("pwd")
    
    try:
        user = User.query.filter_by(mail=mail, username= username).first()
        if not user:
            raise NoResultFound
        
        if user and check_password_hash(user.pwd, password):
            access_token = JWTService.generate_access_token(user.public_id, user.mail, user.admin)

            refresh_token = JWTService.generate_refresh_token(user.public_id)
            
            if access_token and refresh_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
                
                return jsonify(response_object), HTTPStatus.OK
        
        response_object = {
            "status": "fail",
            "message": "Invalid credentials",
        }

        return jsonify(response_object), HTTPStatus.UNAUTHORIZED

    except Exception as e:
        logger.error(e)
        raise e
    
@api.route("/api/auth/register", methods=["POST"])
def register_user():
    user_json = request.get_json()

    if not user_json:
        raise ValueError("Missing request body")
    
    username = user_json.get("username")
    mail = user_json.get("mail")

    user = User.query.filter(
        (User.username == username) | (User.mail == mail)
    ).first()
    
    if user:
        raise IntegrityError(statement="User already present", params= None, orig=Exception())
    
    else:
        # add new user to db
        user_json["public_id"] = str(uuid.uuid4())
        user = UserSchema().load(user_json)
        
        db.session.add(user)
        db.session.commit()
        
        #Check if user was correctly generated
        user = User.query.filter_by(mail=mail).first()
        if not user:
            raise ValueError("User generated incorrectly")
      

        logger.info(f"New user registered: {user.username}")

        # generate auth token
        auth_token = JWTService.generate_access_token(user.public_id, user.mail, user.admin)
        # generate refresh token
        refresh_token = JWTService.generate_refresh_token(user.public_id)
        response_object = {}
        response_object["status"] = "success"
        response_object["message"] = "Successfully registered."
        response_object["access_token"] = auth_token
        response_object["refresh_token"] = refresh_token

        return jsonify(response_object), 201

@api.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        abort(HTTPStatus.BAD_REQUEST, description="Missing refresh token")

    data = JWTService.verify_token(refresh_token, "refresh")

    if not data:
        abort(HTTPStatus.UNAUTHORIZED, description="Invalid token")

    user = User.query.filter_by(public_id=data["user_id"]).first()

    if not user:
        abort(HTTPStatus.UNAUTHORIZED, description="Login attempt with non-existent user")

    access_token = JWTService.generate_access_token(user.public_id, user.mail, user.admin)

    response_object = {
            "status": "success",
            "access_token": access_token
        }
    return jsonify(response_object), HTTPStatus.OK
