import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_schema import SeaSchema
from Models.sea import Sea
from flask import request
from Api.database import db


# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

SEA_ENDPOINT = "/api/sea"


class SeaResource(Resource):

    def __retrieve_sea_by_key(self, day_number, date, itinerary_id):
        return Sea.query.filter_by(
            day_number=day_number, date=date, itinerary_id=itinerary_id).first()


    def get(self):
        """
        SeaResource GET method. Retrieves the information related to the sea with the passed keys in the request
        """
        try:
            day_number = request.args.get('day_number')
            date = request.args.get('date')
            itinerary_id = request.args.get('itinerary_id')
            sea = self.__retrieve_sea_by_key(day_number, date, itinerary_id)
            sea_json = SeaSchema().dump(sea)
            if not sea_json:
                raise NoResultFound()
            return sea_json, 200
        except NoResultFound:
            abort(
                404, message=f"Sea with day number{day_number}date {date} itinerary id{itinerary_id} not found in database")

    def post(self):
        """
        SeaResource POST method. Adds a new sea to the database.
        :return: Sea, 201 HTTP status code.
        """

        try:
            sea = SeaSchema().load(request.get_json())
            logger.info(
                f"Inserting sea: {sea}"
            )
            db.session.add(sea)
            db.session.commit()
            sea = self.__retrieve_sea_by_key(
                sea.day_number,
                sea.date,
                sea.itinerary_id
            )
            return SeaSchema().dump(sea), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def put(self):
        """
        Sea Resource POST method. Updates an existing user.

        :return: Sea, 201 HTTP status code.
        """

        try:
            updated_sea = SeaSchema().load(request.get_json())
            db.session.merge(updated_sea)
            db.session.commit()
            updated_sea = self.__retrieve_sea_by_key(
                updated_sea.day_number,
                updated_sea.date,
                updated_sea.itinerary_id
            )
            logger.info(
                f"Sea: {updated_sea}"
            )
            return SeaSchema().dump(updated_sea), 201

        except Exception as e:
            logger.error(
                f"Error: {e}")
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def delete(self):
        """
        Sea Resource DELETE method. Eliminates an existing sea from the db.

        :return: Deletion successful,200 HTTP status code. | 500, Error
        """

        try:
            day_number = request.args.get('day_number')
            date = request.args.get('date')
            itinerary_id = request.args.get('itinerary_id')
            logger.info(
                f"Deleting sea with day number{day_number}date {date} itinerary id{itinerary_id}")
            sea = self.__retrieve_sea_by_key(day_number, date, itinerary_id)

            db.session.delete(sea)
            db.session.commit()
            logger.info(
                f"Sea with with day number{day_number}date {date} itinerary id{itinerary_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}")
            abort(
                500, message=f"Error: {e}")
