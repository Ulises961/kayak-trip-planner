import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/user/<id>"

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
        