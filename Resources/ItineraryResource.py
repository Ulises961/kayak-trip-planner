import logging
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.itinerary_shema import ItinerarySchema
from Models.itinerary import Itinerary
from flask import request

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/itinerary/<id>"

class ItineraryResource(Resource):

    def retrieveItineraryById(id):
        itinerary = Itinerary.query.filter_by('id', id).first()
        day_json = ItinerarySchema.dump(itinerary)
        if not day_json:
             raise NoResultFound()
        return day_json
    
    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the itinerary with the passed id in the request
        """
        try:
            self.retrieveItineraryById(id)
        except NoResultFound:
                abort(404, message=f"Itinerary with id {id} not found in database")
        