import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.trip_schema import TripSchema
from Models.trip import Trip
from Models.user import User
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

TRIP_ENDPOINT = "/api/trip"

class TripResource(Resource):

    def __retrieveTripById(id):
        trip = Trip.query.filter_by(id= id).first()
        trip_json = TripSchema().dump(trip)
        if not trip_json:
             raise NoResultFound()
        return trip_json, 200
    
    def get(self, id=None):
        """
        TripResource GET method. Retrieves the information related to a trip with the passed id in the request
        """
        if id:
            logger.info(f"Retrieving trip with id {id}")
            try:
                self.__retrieveTripById(id)
            except NoResultFound:
                    logger.error(f"Trip with id {id} not found in database")
                    abort(404, message=f"Trip with id {id} not found in database")

        else:
            logger.info(f"retrieving all Trips in db")
            try:
                trips = Trip.query.all()
                trips_json =  [TripSchema().dump(trip) for trip in trips]
                if len(trips_json) == 0:
                    abort(404, message=f"No trips in db")
                return trips_json, 200
            except IntegrityError:
                    abort(500, message=f"Error while retrieving trips")
        
    def post(self):
        """
        TripResource POST method. Adds a new trip to the database.

        :return: Trip, 201 HTTP status code.
        """

        try:
            trip = TripSchema().load(request.get_json())
            db.session.add(trip)
            db.session.commit()
            return TripSchema().dumps(trip), 201
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this trip is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        except TypeError as e:
            logger.warning(
                f"Missing positional parameters. Error: {e}")   
            abort(500, message="Missing parameters")
