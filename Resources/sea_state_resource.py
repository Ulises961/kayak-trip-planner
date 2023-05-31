import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_state_schema import SeaStateSchema
from Models.sea_state import SeaState
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

SEA_STATE_ENDPOINT = "/api/sea_state"

class SeaStateResource(Resource):

    def __retrieve_sea_state_by_key(self,day_number, date, itinerary_id, time):
        return SeaState.query.filter_by(day_number=day_number, date=date, itinerary_id=itinerary_id, time=time).first()
    
    def get(self):
        """
        SeaStateResource GET method. Retrieves the information related to the sea state with the passed id in the request
        """
        try:
            sea_state = SeaStateSchema().dump(request.get_json())
            sea_state = self.__retrieve_sea_state_by_key( sea_state.day_number,
                sea_state.date,
                sea_state.itinerary_id,
                sea_state.time
                )
            sea_state_json =  SeaStateSchema().dump(sea_state)
            if not sea_state_json:
                raise NoResultFound()
            return sea_state_json, 200
        except NoResultFound:
                abort(404, message=f"Sea state {sea_state} not found in database")
        except Exception as e:
            abort(500, message=f"Error: {e}")

    def post(self):
        """
        SeaStateResource POST method. Adds a new sea_state to the database.

        :return: SeaState, 201 HTTP status code.
        """
        try:
            sea_state = SeaStateSchema().load(request.get_json())
            db.session.add(sea_state)
            db.session.commit()
            sea_state = self.__retrieve_sea_state_by_key(
                sea_state.day_number,
                sea_state.date,
                sea_state.itinerary_id,
                sea_state.time
                )
            return SeaStateSchema().dump(sea_state), 201
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this sea_state is already in the database. Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Unexpected Error!")

    def put(self):
        try:
            logger.info(f"Update sea state {request.get_json()} in db")
            sea_state = SeaStateSchema().load(request.get_json())
            db.session.merge(sea_state)
            db.session.commit()
            sea_state = self.__retrieve_sea_state_by_key( sea_state.day_number,
                sea_state.date,
                sea_state.itinerary_id,
                sea_state.time
                )

            return SeaStateSchema().dump(sea_state), 201

        except Exception as e:
            logger.warning(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self):
        try:

            sea_state = SeaStateSchema().dump(request.get_json())
            logger.info(f"Deleting sea state {sea_state} ")

            sea_state = self.__retrieve_sea_state_by_key( sea_state.day_number,
                sea_state.date,
                sea_state.itinerary_id,
                sea_state.time
                )
            db.session.delete(sea_state)
            db.session.commit()
            logger.info(f"Sea state {sea_state} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")