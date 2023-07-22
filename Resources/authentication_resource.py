import logging

from Models.user import User
from flask import request, jsonify, current_app
from flask_bcrypt import check_password_hash
import jwt, datetime
from flask import Blueprint, request, jsonify
from Api.utils import authenticate_restful
from http import HTTPStatus
from sqlalchemy import exc, or_
from Schemas.user_schema import UserSchema
from Api.database import db
from functools import wraps

# It will print the name of this module when the main app is running

log = logging.getLogger(__name__)
api = Blueprint("auth", __name__)

def generate_auth_token(public_id):
    return jwt.encode(
        {
            "public_id": public_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
        },
        current_app.config["SECRET_KEY"],
        "HS256",
    )
    

def decode_auth_token(auth_token):
    return jwt.decode(
        auth_token, current_app.config["SECRET_KEY"], ["HS256"]
    )

def auth_token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       auth_token = None
       if 'x-access-tokens' in request.headers:
           auth_token = request.headers['x-access-tokens']
 
       if not auth_token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = decode_auth_token(auth_token)
           current_user = User.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(*args, **kwargs)
   return decorator

@api.route("/api/auth/ping", methods=["GET"])
@authenticate_restful
def check_token(resp):
    response_object = {"status": "success", "message": "Token valid"}
    return jsonify(response_object), HTTPStatus.OK


@api.route("/api/auth/status", methods=["GET"])
@authenticate_restful
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        "status": "success",
        "message": "success",
        "data": user.to_json(),
    }
    return jsonify(response_object), 200


@api.route("/api/auth/login", methods=["POST"])
def login_user():
    
    response_object = {"status": "fail", "message": "Invalid payload"}
    
    post_data = request.get_json()
    log.info(f"Post data {post_data}")
    
    if not post_data:
        return jsonify(response_object), HTTPStatus.BAD_REQUEST

    mail = post_data.get("email")
    password = post_data.get("password")
    
    try:
        user = User.query.filter_by(mail=mail).first()
        
        if user and check_password_hash(user.pwd, password):
            auth_token = generate_auth_token(user["public_id"])
            
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in",
                    "auth_token": auth_token,
                }
                
                return jsonify(response_object), HTTPStatus.OK
        else:
            response_object["message"] = "User does not exist"
            return jsonify(response_object), HTTPStatus.NOT_FOUND
        
    except Exception as e:
        log.error(e)
        response_object["message"] = "Try again."
        return jsonify(response_object), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/api/auth/logout", methods=["GET"])
@authenticate_restful
def logout_user(resp):
    log.info(resp)
    response_object = {"status": "success", "message": "Successfully logged out"}
    return jsonify(response_object), HTTPStatus.OK


@api.route("/api/auth/register", methods=["POST"])
def register_user():
    user_json = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload"}
    
    if not user_json:
        return jsonify(response_object), 400

    username = user_json.get("username")
    mail = user_json.get("mail")
   
    try:
        user = User.query.filter(
            (User.username == username) | (User.mail == mail)
        ).first()
        
        if not user:
            # add new user to db
            user = UserSchema().load(user_json)
            db.session.add(user)
            db.session.commit()
            
            #Check if user was correctly generated
            user = User.query.filter_by(mail=mail).first()
            
            print(f"\n\nTHIS IS THE USER {user}\n\n")
            print("\n\nMAKING ATTEMPT\n\n")
            
            # generate auth token
            auth_token = generate_auth_token(user.public_id)
            
            response_object["status"] = "success"
            response_object["message"] = "Successfully registered."
            response_object["auth_token"] = auth_token
            
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. That user already exists."
            return jsonify(response_object), 400
        
    except exc.IntegrityError as e:
        db.session.rollback()
        log.error(e)
        return jsonify(response_object), 400
    
    except ValueError as e:
        db.session.rollback()
        log.error(e)
        return jsonify(response_object), 400
