import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

USER_ENDPOINT = "/api/user/<id>"

class UserResource(Resource):

    def retrieveUserStateById(id):
        user = User.query.filter_by('id', id).first()
        user_json = UserSchema.dump(user)
        if not user_json:
             raise NoResultFound()
        return user_json
    
    def get(self, id=None):
        """
        UserResource GET method. Retrieves the information related to the user with the passed id in the request
        """
        try:
            self.retrieveUserStateById(id)
        except NoResultFound:
                abort(404, message=f"User with id {id} not found in database")
    
    def post(self):
        """
        UserResource POST method. Adds a new user to the database.

        :return: User, 201 HTTP status code.
        """
        user = UserSchema().load(request.get_json())

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this user is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return user, 201
