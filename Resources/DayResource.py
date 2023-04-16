import logging
import json
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from Schemas.day_schema import DaySchema
from Models.day import Day
from flask import request

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/day/<id>"

class DayResource(Resource):

    def retrieveDayByItineraryId(itineraryId):
            itinerary = request.args.get("itinerary")
            logger.info(f"Retrieving days with itinerary id={itinerary}")
            try:
                days = Day.query.filter_by('itinerary', itinerary).all()
            except Exception:
                logger.error(Exception.message)
            logger.info(f"Days successfully retrieved")

            return [DaySchema.dump(day) for day in days], 200
    
    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        if not id:
            if request.args.get('itinerary'):
                 return self.retrieveDayByItineraryId(request.args.get('itinerary'))
            else: 
                 return json.dumps({'message': "Missing itinerary parameter"},400)
        else:
            day = Day.query.filter_by('id', id).first()
            return DaySchema.dump(day)
        
