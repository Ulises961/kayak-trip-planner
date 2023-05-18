import logging
from flask import request
from Api.database import db
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from Schemas.day_schema import DaySchema
from Models.day import Day
from Models.itinerary import Itinerary

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

DAY_ENDPOINT = "/api/day"


class DayResource(Resource):

    def __retrieveDayById(id):
        day = Day.query.filter_by('id', id).first()
        day_json = DaySchema.dump(day)

        if not day_json:
            raise NoResultFound()
        
        return day_json, 200

    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        if id:
            logger.info(f"Retrive day with id {id}")
            
            try:
                json = self.__retrieveDayById(id)
                return json, 200
            except NoResultFound:
                abort(404, message=f"Day with id {id} not found in database")

        else:
            logger.info(f"Retrive all days from db")
            try:
                days = Day.query.all()
                days_json = [DaySchema().dump(day) for day in days]
                if len(days_json) == 0:
                    abort(404, message=f"No days in db")
                return days_json, 200
            except IntegrityError:
                abort(500, message=f"Error while retrieving days")

    def post(self):
        """
        DayResource POST method. Adds a new Day to the database.

        :return: Day, 201 HTTP status code.
        """

        logger.info(f"Insert day {request.get_json()} in db")
        day = DaySchema().load(request.get_json())

        try:
            db.session.add(day)
            db.session.commit()

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this day is already in the database. Error: {e}"
            )
            abort(500, message="Unexpected Error!")

        finally:
            return DaySchema().dump(day), 201
