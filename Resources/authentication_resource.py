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

# It will print the name of this module when the main app is running

log = logging.getLogger(__name__)
api = Blueprint("auth", __name__)


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
    post_data = request.get_json()
    log.info(f"Post data {post_data}")
    response_object = {"status": "fail", "message": "Invalid payload"}
    if not post_data:
        return jsonify(response_object), HTTPStatus.BAD_REQUEST

    mail = post_data.get("email")
    password = post_data.get("password")
    try:
        user = User.query.filter_by(mail=mail).first()
        if user and check_password_hash(user.pwd, password):
            auth_token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
                },
                current_app.config["SECRET_KEY"],
                "HS256",
            )
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in",
                    "auth_token": jwt.decode(
                        auth_token, current_app.config["SECRET_KEY"], ["HS256"]
                    ),
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
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload"}
    if not post_data:
        return jsonify(response_object), 400

    username = post_data.get("username")
    mail = post_data.get("mail")
   
    try:
        user = User.query.filter(
            or_(User.username == username, User.mail == mail)
        ).first()
        if not user:
            # add new user to db
            user_json = request.get_json()

            user = UserSchema().load(user_json)
            db.session.add(user)
            db.session.commit()
            new_user = User.query.filter(mail=mail)
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object["status"] = "success"
            response_object["message"] = "Successfully registered."
            response_object["auth_token"] = auth_token.decode()
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
