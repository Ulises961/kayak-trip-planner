import logging
from flask_restful import Resource, abort
from sqlalchemy.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import Blueprint, request
from Api.database import db
import jwt, datetime
from Services import UserService
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
        user_json = UserSchema().dump(user)
        if not user_json:
            raise NoResultFound()
        return user_json, 200
       
    except NoResultFound:
        abort(404, message=f"User with id {id} not found in database")
    except Exception as e:
        abort(500, message=f"Error: {e}")

def post():
    """
    UserResource POST method. Adds a new user to the database.

    :return: User, 201 HTTP status code.
    """
    try:
        user_json= request.get_json()
        
        user = UserSchema().load(user_json)
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        logger.error(
            f"Missing parameters. Error: {e}")
        db.session.rollback()
        abort(500, message=f"Error:{e}")

    else:
        return UserSchema().dump(user), 201


def put():
    """
    UserResource POST method. Updates an existing user.

    :return: User, 201 HTTP status code.
    """

    try:
        updated_user=UserSchema().load(request.get_json())
        db.session.merge(updated_user)
        db.session.commit()
        updated_user = User.query.filter_by(id = updated_user.id).first()
        logger.info(
            f"User: {updated_user}"
        )
        return UserSchema().dump(updated_user), 201
        
    except Exception as e:
        logger.error(
            f"Error: {e}")
        db.session.rollback()

        abort(500, message=f"Error:{e}")

def delete():
    try:
        id = request.args.get('id')
        logger.info(f"Deleting day {id} ")

        user_to_delete = __retrieveUserById(id)
        db.session.delete(user_to_delete)
        db.session.commit()
        logger.info(f"User with id {id} successfully deleted")
        return "Deletion successful", 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(
            f"Error: {e}")
        abort(
            500, message=f"Error: {e}")

