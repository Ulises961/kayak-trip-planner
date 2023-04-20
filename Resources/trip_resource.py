import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.trip_schema import TripSchema
from Models.trip import Trip
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/trip/<id>"

class TripResource(Resource):

    def retrieveTripById(id):
        trip = Trip.query.filter_by('id', id).first()
        trip_json = TripSchema.dump(trip)
        if not trip_json:
             raise NoResultFound()
        return trip_json
    
    def get(self, id=None):
        """
        TripResource GET method. Retrieves the information related to a trip with the passed id in the request
        """
        try:
            self.retrieveTripById(id)
        except NoResultFound:
                abort(404, message=f"Trip with id {id} not found in database")
    
    def post(self):
        """
        TripResource POST method. Adds a new trip to the database.

        :return: Trip, 201 HTTP status code.
        """
        trip = TripSchema().load(request.get_json())

        try:
            db.session.add(trip)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this trip is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return trip, 201
