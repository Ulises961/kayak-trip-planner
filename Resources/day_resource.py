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

    def __retrieveDayByKey(self, day_number, date, itinerary_id):
        day = Day.query.filter_by(
            day_number=day_number, date=date, itinerary_id=itinerary_id).first()
        day_json = DaySchema().dump(day)

        if not day_json:
            raise NoResultFound()

        return day_json, 200

    def get(self):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        try:
            day_number = request.args.get('day_number')
            date = request.args.get('date')
            itinerary_id = request.args.get('itinerary_id')
        except ValueError:
            db.session.rollback()
            abort(500, message=f"Missing parameters, {ValueError}")
        if day_number and date and itinerary_id:
            logger.info(f"Retrive day with id {id}")

            try:
                json = self.__retrieveDayByKey(day_number, date, itinerary_id)
                return json, 200
            except NoResultFound:
                db.session.rollback()
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
                db.session.rollback()
                abort(500, message=f"Error while retrieving days")

    def post(self):
        """
        DayResource POST method. Adds a new Day to the database.

        :return: Day, 201 HTTP status code.
        """

        logger.info(f"Insert day {request.get_json()} in db")

        try:
            day = DaySchema().load(request.get_json())
            db.session.add(day)
            db.session.commit()

        except TypeError as e:
            logger.warning(
                f"Missing parameters. Error: {e}")
            db.session.rollback()
            abort(500, message="Missing parameters")

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this day is already in the database. Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Unexpected Error!")

        finally:
            return DaySchema().dump(day), 201

    def put(self):

        logger.info(f"Update day {request.get_json()} in db")
        day_json = request.get_json()
        try:
            day = Day.query.filter_by(day_number=day_json['day_number'],
                                      date=day_json['date'], itinerary_id=day_json['itinerary_id']).first()
            day = DaySchema().load(day_json, instance=day)
            db.session.add(day)
            db.session.commit()

        except TypeError as e:
            logger.warning(
                f"Missing parameters. Error: {e}")
            db.session.rollback()
            abort(500, message="Missing parameters")

        except IntegrityError as e:
            db.session.rollback()
            logger.warning(
                f"Integrity Error: {e}"
            )
            abort(500, message="Unexpected Error!")

        finally:
            day = Day.query.filter_by(
                day_number=day_json['day_number'],
                date=day_json['date'], 
                itinerary_id=day_json['itinerary_id']
                ).first()
            
            return DaySchema().dump(day), 201

    def delete(self):
        try:
            day_number = request.args.get('day_number')
            date = request.args.get('date')
            itinerary_id = request.args.get('itinerary_id')

            logger.info(f"Deleting day {day_number, date, itinerary_id} ")

            dayToDelete = Day.query.filter_by(
                day_number=day_number, date=date, itinerary_id=itinerary_id).first()
            db.session.delete(dayToDelete)
            db.session.commit()
            logger.info(
                f"Day {day_number, date, itinerary_id} successfully deleted")
            return "Deletion successful", 200

        except Exception | ValueError as e:
            db.session.rollback()
            abort(
                500, message=f"Error while performing deletion,\nDetail: {e}")
