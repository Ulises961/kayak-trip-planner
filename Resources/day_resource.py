import logging
from flask import request
from Api.database import db
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from Schemas.day_schema import DaySchema
from Models.day import Day

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/day"

class DayResource(Resource):

    def retrieveDayById(id):
        day = Day.query.filter_by('id', id).first()
        day_json = DaySchema.dump(day)
        if not day_json:
             raise NoResultFound()
        return day_json
    
    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        try:
            self.retrieveDayById(id)
        except NoResultFound:
                abort(404, message=f"Day with id {id} not found in database")

    def post(self):
        """
        DayResource POST method. Adds a new Day to the database.

        :return: Day, 201 HTTP status code.
        """
        day = DaySchema().load(request.get_json())

        try:
            db.session.add(day)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this day is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return day, 201


        
