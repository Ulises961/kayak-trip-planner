import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_state_schema import SeaStateSchema
from Models.sea_state import SeaState
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/sea_state/<id>"

class SeaResource(Resource):

    def retrieveSeaStateById(id):
        sea_state = SeaState.query.filter_by('id', id).first()
        sea_state_json = SeaStateSchema.dump(sea_state)
        if not sea_state_json:
             raise NoResultFound()
        return sea_state_json
    
    def get(self, id=None):
        """
        SeaStateResource GET method. Retrieves the information related to the sea state with the passed id in the request
        """
        try:
            self.retrieveSeaStateById(id)
        except NoResultFound:
                abort(404, message=f"Sea State with id {id} not found in database")

    def post(self):
        """
        SeaStateResource POST method. Adds a new sea_state to the database.

        :return: Image, 201 HTTP status code.
        """
        sea_state = SeaStateSchema().load(request.get_json())

        try:
            db.session.add(sea_state)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this sea_state is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return sea_state, 201
