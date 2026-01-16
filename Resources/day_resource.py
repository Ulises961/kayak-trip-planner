from http import HTTPStatus
import logging
from typing import cast
from flask import request
from Api.database import db
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError, NoResultFound
from Schemas.day_schema import DaySchema
from Models.day import Day
from Services.jwt_service import JWTService

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

DAY_ENDPOINT = "/api/day"


class DayResource(Resource):
    
    def __retrieve_day_by_key(self, day_number, date, itinerary_id):
        return Day.query.filter_by(
            day_number=day_number, date=date, itinerary_id=itinerary_id).first()

    def __retrieve_day_by_id(self, id):
        return Day.query.filter_by(
            id=id).first()

    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        try:

            day_number = request.args.get('day_number')
            date = request.args.get('date')
            itinerary_id = request.args.get('itinerary_id')
            
            if id:
                day = self.__retrieve_day_by_id(id)
                day_json = DaySchema().dump(day)
                if not day_json:
                    raise NoResultFound()
                return day_json, 200

            elif day_number and date and itinerary_id:
                logger.info(
                    f"Retrive day number {day_number} with date {date} from itinerary {itinerary_id}")
                day = self.__retrieve_day_by_key(
                    day_number, date, itinerary_id)
                day_json = DaySchema().dump(day)
                if not day_json:
                    print('hello',day_number,itinerary_id,date,Day.query.all())
                    raise NoResultFound()
                return day_json, 200

            elif not id and not (day_number and date and itinerary_id):
                logger.info(f"Retrive all days from db")
                days = Day.query.all()
                days_json = [DaySchema().dump(day) for day in days]
                if len(days_json) == 0:
                    raise NoResultFound()
                return days_json, 200
            else:
                raise NoResultFound()

        except NoResultFound:
            abort(404, message=f"Resource not found")
        except Exception as e:
            abort(500, message=f"Error:{e}")

    def post(self):
        """
        DayResource POST method. Adds a new Day to the database.

        :return: Day, 201 HTTP status code.
        """

        logger.info(f"Insert day {request.get_json()} in db")

        try:
            day_json = request.get_json()
            day = DaySchema().load(day_json)
            db.session.add(day)
            db.session.commit()

            day = Day.query.filter_by(
                day_number=day_json['day_number'],
                date=day_json['date'],
                itinerary_id=day_json['itinerary_id']
            ).first()
            return DaySchema().dump(day), 201
        except Exception as e:
            logger.error(
                f"Error: {e}")
            db.session.rollback()
            abort(500, message=f"{e}")

    def put(self):

        logger.info(f"Update day {request.get_json()} in db")

        try:
            day = cast(Day,DaySchema().load(request.get_json()))
            if not day:
                abort(HTTPStatus.BAD_REQUEST, description="Day not found")
            db.session.merge(day)
            db.session.commit()

            if day: 
                updated_day = self.__retrieve_day_by_id(
                    day.id
                )

                return DaySchema().dump(updated_day), 201

        except Exception as e:
            logger.error(
                f"Error: {e}")
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def delete(self,id=None):
        try:
            day_to_delete = None
            if id: 
                day_to_delete = self.__retrieve_day_by_id(
                id)
            else:
                day_number = request.args.get('day_number')
                date = request.args.get('date')
                itinerary_id = request.args.get('itinerary_id')

                logger.info(f"Deleting day {day_number, date, itinerary_id} ")

                day_to_delete = self.__retrieve_day_by_key(
                    day_number, date, itinerary_id)
            
            db.session.delete(day_to_delete)
            db.session.commit()

            logger.info(
                f"Day with id {id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
