import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.user_schema import UserSchema
from Models.user import User
from flask import request, jsonify, current_app, make_response
from flask_bcrypt import check_password_hash
from Api.database import db
import jwt, datetime

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

USER_ENDPOINT = "/api/user"


class UserResource(Resource):

    def __retrieveUserById(self,id):
        return User.query.filter_by(id=id).first()

    def get(self):
        """
        UserResource GET method. Retrieves the information related to the user with the passed id in the request
        """
        try:
            id = request.args.get('id')
            if id:
                logger.info(
                    f"Retrieving user with id {id}")
                            
                user = self.__retrieveUserById(id)
                user_json = UserSchema().dump(user)
                if not user_json:
                    raise NoResultFound()
                return user_json, 200
            else:
                logger.info(
                    f"Retrieving all users from db")
        
                users = User.query.all()
                users_json = [UserSchema().dump(user) for user in users], 200
                if len(users_json) == 0:
                    abort(404, message=f"No users in db")
                return users_json, 200
        except NoResultFound:
            abort(404, message=f"User with id {id} not found in database")
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
            logger.error(
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

    def delete(self):
        try:
            id = request.args.get('id')
            logger.info(f"Deleting day {id} ")

            user_to_delete = self.__retrieveUserById(id)
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

    def login(self):
        auth = request.get_json()

        if not auth or not auth["email"] or not auth["password"]:
            return make_response('could not verify', 401, {'Authentication': 'login required"'})

        user = User.query.filter_by(email=auth["email"]).first()

        if check_password_hash(auth["password"], user.password):
            token = jwt.encode(
                {
                    'public_id': user.public_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                },
                current_app.config['SECRET_KEY'],
                "HS256"
            )

            return jsonify({'token': token})

        return make_response('could not verify',  401, {'Authentication': '"login required"'})