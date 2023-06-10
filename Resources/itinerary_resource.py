import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.itinerary_shema import ItinerarySchema
from Models.itinerary import Itinerary
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

ITINERARY_ENDPOINT = "/api/itinerary"


class ItineraryResource(Resource):

    def __retrieve_itinerary_by_id(self, id):
        return Itinerary.query.filter_by(id=id).first()

    def get(self):
        """
        ItineraryResource GET method. Retrieves the information related to the itinerary with the passed id in the request
        """
        try:
            itinerary_id = request.args.get('id')
            if id:
                itinerary = self.__retrieve_itinerary_by_id(itinerary_id)
                day_json = ItinerarySchema().dump(itinerary)
                if not day_json:
                    raise NoResultFound()
                return day_json
            else:
                itineraries = Itinerary.query.all()
                itineraries_json = [ItinerarySchema().dump(
                    itinerary) for itinerary in itineraries]
                if len(itineraries_json) == 0:
                    raise NoResultFound()
                return itineraries_json, 200
        except NoResultFound:
            abort(
                404, message=f"Itinerary with id {itinerary_id} not found in database")
        except Exception as e:
            abort(500, message=f"Error:{e}")

    def post(self):
        """
        ItineraryResource POST method. Adds a new itinerary to the database.

        :return: Itinerary, 201 HTTP status code.
        """
        try:
            itinerary = ItinerarySchema().load(request.get_json())
            db.session.add(itinerary)
            db.session.commit()
        except IntegrityError as e:
            logger.error(
                f"Integrity Error, this itinerary is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return ItinerarySchema().dump(itinerary), 201

    def put(self):

        try:
            logger.info(f"Update trip {request.get_json()} in db")
            updated_itinerary = ItinerarySchema().load(request.get_json())
            db.session.merge(updated_itinerary)
            db.session.commit()
            itinerary = self.__retrieve_itinerary_by_id(updated_itinerary.id)
            return ItinerarySchema().dump(itinerary), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self):
        try:
            itinerary_id = request.args.get('id')
            logger.info(f"Deleting itinerary {itinerary_id} ")

            itinerary_to_delete = self.__retrieve_itinerary_by_id(itinerary_id)
            db.session.delete(itinerary_to_delete)
            db.session.commit()
            logger.info(
                f"Itinerary with id {itinerary_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}"
            )
            abort(
                500, message=f"Error: {e}")
