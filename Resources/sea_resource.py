import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_schema import SeaSchema
from Models.sea import Sea
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

SEA_ENDPOINT = "/api/sea/<id>"

class SeaResource(Resource):

    def retrieveSeaById(id):
        sea = Sea.query.filter_by('id', id).first()
        sea_json = SeaSchema.dump(sea)
        if not sea_json:
             raise NoResultFound()
        return sea_json
    
    def get(self, id=None):
        """
        SeaResource GET method. Retrieves the information related to the sea with the passed id in the request
        """
        try:
            self.retrieveSeaById(id)
        except NoResultFound:
                abort(404, message=f"Sea with id {id} not found in database")
    
    def post(self):
        """
        SeaResource POST method. Adds a new sea to the database.

        :return: Sea, 201 HTTP status code.
        """
        sea = SeaSchema().load(request.get_json())

        try:
            db.session.add(sea)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this sea is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return sea, 201
