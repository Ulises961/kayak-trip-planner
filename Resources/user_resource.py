from http import HTTPStatus
from http.client import HTTPException
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import Blueprint, jsonify, request, abort
from Api.database import db
import jwt, datetime
from Services.user_service import UserService
from Services.Middleware.auth_middleware import JWTService
# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

USER_ENDPOINT = "/api/user"
user_api = Blueprint('user', __name__, url_prefix=USER_ENDPOINT)

@user_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
def get(id:int):
    """
    UserResource GET method. Retrieves the information related to the user with the passed id in the request
    """
    try:
        logger.info(
            f"Retrieving user with id {id}")
                    
        user = UserService.get_user_by_id(id)
        return jsonify(UserSchema().dump(user)), HTTPStatus.OK
    
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"User with id {id} not found in database")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@user_api.route("/<int:id>/update")
@JWTService.authenticate_restful
def update_user(id: int):
    """
    UserResource POST method. Updates an existing user.

    :return: User, 201 HTTP status code.
    """

    try:
        user = UserService.update_user(id, request.get_json())
        return jsonify(UserSchema().dump(user)), HTTPStatus.OK
    
    except HTTPException:
        raise
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description=f"Error updating user with id {id}")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error:{e}")

@user_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
def delete(id: int):
    try:
        UserService.delete_user(id)       
        return "Deletion successful", 200
    
    except HTTPException:
        raise
    except ValueError:
        abort(HTTPStatus.CONFLICT, description=f"Error deleting user with id {id}")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error:{e}")