import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db
from sqlalchemy.exc import ProgrammingError
# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

USER_ENDPOINT = "/api/user"


class UserResource(Resource):

    def __retrieveUserById(self,id):
        user = User.query.filter_by(id=id).first()
        user_json = UserSchema().dump(user)
        if not user_json:
            raise NoResultFound()
        return user_json

    def get(self):
        """
        UserResource GET method. Retrieves the information related to the user with the passed id in the request
        """

        id = request.args.get('id')
        if id:
            logger.info(
                f"Retrieving user with id {id}")
            try:
                user_json = self.__retrieveUserById(id)
                return user_json, 200
            except NoResultFound:
                abort(404, message=f"User with id {id} not found in database")
        else:
            logger.info(
                f"Retrieving all users from db")
            try:
                users = User.query.all()
                users_json = [UserSchema().dump(user) for user in users], 200
                if len(users_json) == 0:
                    abort(404, message=f"No users in db")
                return users_json, 200
            except Exception as e:
                abort(500, message=f"Error: {e}")

    def post(self):
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
            logger.warning(
                f"Missing parameters. Error: {e}")
            db.session.rollback()
            abort(500, message=f"Error:{e}")

        else:
            return UserSchema().dump(user), 201
    
    def put(self):
        """
        UserResource POST method. Updates an existing user.

        :return: User, 201 HTTP status code.
        """
        user = None
        updated_user=UserSchema().load(request.get_json())

        try:
            updated_user=UserSchema().load(request.get_json())
            user =  User.query.filter_by(id =updated_user.id).first()
            updated_user = UserSchema().load(request.get_json(),instance=user)
            db.session.add(updated_user)
            db.session.commit()

            updated_user = User.query.filter_by(id = updated_user.id).first()
            logger.warning(
                f"User: {user}"
            )
            return UserSchema().dump(updated_user), 201
            
        except Exception as e:
            logger.warning(
                f"Error: {e}")
            db.session.rollback()

            abort(500, message=f"Error:{e}")

    def delete(self):
        try:
            id = request.args.get('id')
            logger.info(f"Deleting day {id} ")

            userToDelete = User.query.filter_by(
                id=id).first()
            db.session.delete(userToDelete)
            db.session.commit()
            logger.info(f"User with id {id} successfully deleted")
            return "Deletion successful", 200
        
        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
