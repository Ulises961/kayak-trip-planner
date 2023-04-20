import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.itinerary_shema import ItinerarySchema
from Models.itinerary import Itinerary
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

ITINERARY_ENDPOINT = "/api/itinerary/<id>"

class ItineraryResource(Resource):

    def retrieveItineraryById(id):
        itinerary = Itinerary.query.filter_by('id', id).first()
        day_json = ItinerarySchema.dump(itinerary)
        if not day_json:
             raise NoResultFound()
        return day_json
    
    def get(self, id=None):
        """
        ItineraryResource GET method. Retrieves the information related to the itinerary with the passed id in the request
        """
        try:
            self.retrieveItineraryById(id)
        except NoResultFound:
                abort(404, message=f"Itinerary with id {id} not found in database")
    
    def post(self):
        """
        ItineraryResource POST method. Adds a new itinerary to the database.

        :return: Itinerary, 201 HTTP status code.
        """
        itinerary = ItinerarySchema().load(request.get_json())

        try:
            db.session.add(itinerary)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this itinerary is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return itinerary, 201
