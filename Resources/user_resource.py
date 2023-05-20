import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

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
            except IntegrityError:
                abort(500, message=f"Error while retrieving users")

    def post(self):
        """
        UserResource POST method. Adds a new user to the database.

        :return: User, 201 HTTP status code.
        """
        try:
            user = UserSchema().load(request.get_json())
            db.session.add(user)
            db.session.commit()

        except TypeError as e:
            logger.warning(
                f"Missing parameters. Error: {e}")
            abort(500, message="Missing parameters")
        
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this user is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return UserSchema().dump(user), 201
    
    def put(self):
        """
        UserResource POST method. Updates an existing user.

        :return: User, 201 HTTP status code.
        """
        try:
            updateData = UserSchema().load(request.get_json())
            user = User.query.filter_by(id = updateData.id)
            user = user.update(updateData)
            db.session.add(user)
            db.session.commit()
            
        except TypeError as e:
            logger.warning(
                f"Missing parameters. Error: {e}")
            abort(500, message="Missing parameters")

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error: {e}"
            )
            abort(500, message="Unexpected Error!")

        finally: return UserSchema().dump(user), 201

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
        
        except Exception | ValueError as e:
            abort(
                500, message=f"Error while performing deletion,\nDetail: {e}")
