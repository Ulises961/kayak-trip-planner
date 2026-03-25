import logging

from flask import Blueprint, request, jsonify, abort
from http import HTTPStatus
from sqlalchemy.exc import NoResultFound

from Services.auth_service import AuthService
from Services.user_service import UserService
from Services.Middleware.auth_middleware import JWTService

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
        user = AuthService.authenticate_user(mail, username, password)

        if user:
            access_token = JWTService.generate_access_token(str(user.id), user.mail, user.admin)
            refresh_token = JWTService.generate_refresh_token(str(user.id))

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

    user = AuthService.register_user(user_json)

    auth_token = JWTService.generate_access_token(str(user.id), user.mail, user.admin)
    refresh_token = JWTService.generate_refresh_token(str(user.id))

    response_object = {
        "status": "success",
        "message": "Successfully registered.",
        "access_token": auth_token,
        "refresh_token": refresh_token
    }
    return jsonify(response_object), HTTPStatus.CREATED


@api.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        abort(HTTPStatus.BAD_REQUEST, description="Missing refresh token")

    data = JWTService.verify_token(refresh_token, "refresh")

    if not data:
        abort(HTTPStatus.UNAUTHORIZED, description="Invalid token")

    try:
        user = UserService.get_user_by_id(data["user_id"])
    except NoResultFound:
        abort(HTTPStatus.UNAUTHORIZED, description="Login attempt with non-existent user")

    access_token = JWTService.generate_access_token(str(user.id), user.mail, user.admin)

    response_object = {
        "status": "success",
        "access_token": access_token
    }
    return jsonify(response_object), HTTPStatus.OK
