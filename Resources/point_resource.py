import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.point_schema import PointSchema 
from Models.point import Point
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

POINT_ENDPOINT = "/api/point"

class PointResource(Resource):

    def __retrieve_point_by_id(self,id):
        return Point.query.filter_by(id = id).first()
        
    
    def get(self, id=None):
        """
        PointResource GET method. Retrieves the information related to the point with the passed id in the request
        """
        try:
            if id:
                point = self.__retrieve_point_by_id(id)
                point_json = PointSchema().dump(point)
                if not point_json:
                    raise NoResultFound()
                return point_json,200
            else:
                logger.info(f"Retrive all points from db")
                points = Point.query.all()
                point_json = [PointSchema().dump(point) for point in points]
                if len(point_json) == 0:
                    raise NoResultFound()
                return point_json, 200
        except NoResultFound:
                abort(404, message=f"Point {id} not found in database")
        except Exception as e:
            abort(500, message=f"Error:{e}")

    
    def post(self):
        """
        PointResource POST method. Adds a new point to the database.

        :return: Point, 201 HTTP status code.
        """

        try:
            point = PointSchema().load(request.get_json())
            db.session.add(point)
            db.session.commit()
            point = self.__retrieve_point_by_id(point.id)
            return PointSchema().dump(point), 201
        
        except IntegrityError as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}"
            )

            abort(500, message="Error: {e}")
        
    def put(self):
        try:
            point = PointSchema().load(request.get_json())
            db.session.merge(point)
            db.session.commit()
            point = self.__retrieve_point_by_id(point.id)

            return PointSchema().dump(point), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self,id):
        try:
            logger.info(f"Deleting point {id} ")

            point = self.__retrieve_point_by_id(id)
            db.session.delete(point)
            db.session.commit()
            logger.info(f"Item with id {id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")

        
