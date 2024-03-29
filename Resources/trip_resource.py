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

    def __retrieve_trip_by_id(self,id):
        return Trip.query.filter_by(id = id).first()

    
    def get(self):
        """
        TripResource GET method. Retrieves the information related to a trip with the passed id in the request
        """

        try:
            id = request.args.get('id')
            if id:
                logger.info(f"Retrieving trip with id {id}")
                trip = self.__retrieve_trip_by_id(id)
                trip_json = TripSchema().dump(trip)
                if not trip_json:
                    raise NoResultFound()
                return trip_json, 200
            else:
                logger.info(f"retrieving all Trips in db")
                trips = Trip.query.all()
                trips_json =  [TripSchema().dump(trip) for trip in trips]
                if len(trips_json) == 0:
                    abort(404, message=f"No trips in db")
                return trips_json, 200
        except NoResultFound:
                logger.error(f"Trip with id {id} not found in database")
                abort(404, message=f"Trip with id {id} not found in database")
        except Exception as e:
                abort(500, message=f"Error:{e}")
        
        
    def post(self):
        """
        TripResource POST method. Adds a new trip to the database.

        :return: Trip, 201 HTTP status code.
        """

        try:
            trip_json = request.get_json()
            trip = TripSchema().load(trip_json)
            db.session.add(trip)
            db.session.commit()

            trip = Trip.query.filter_by(id=trip.id).first()
            return TripSchema().dump(trip), 201

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}"
            )
            abort(500, message=f"{e}")

    def put(self):

        logger.info(f"Update trip {request.get_json()} in db")
        
        try:
            updatedTrip = TripSchema().load(request.get_json())
            db.session.merge(updatedTrip)
            db.session.commit()
            trip = Trip.query.filter_by(id=updatedTrip.id).first()
            return TripSchema().dump(trip), 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}")
            abort(500, message=e)

    def delete(self):
        try:
            id = request.args.get('id')
            logger.info(f"Deleting day {id} ")

            trip_to_delete = self.__retrieve_trip_by_id(id)
            db.session.delete(trip_to_delete)
            db.session.commit()
            logger.info(f"Trip {id} successfully deleted")
            return "Deletion successful", 200
        
        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
