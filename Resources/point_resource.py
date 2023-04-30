import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.point_schema import PointSchema 
from Models.point import Point
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

POINT_ENDPOINT = "/api/point/<id>"

class PointResource(Resource):

    def retrievePointById(id):
        point = Point.query.filter_by('id', id).first()
        point_json = PointSchema.dump(point)
        if not point_json:
             raise NoResultFound()
        return point_json
    
    def get(self, id=None):
        """
        PointResource GET method. Retrieves the information related to the point with the passed id in the request
        """
        try:
            self.retrieveItineraryById(id)
        except NoResultFound:
                abort(404, message=f"Itinerary with id {id} not found in database")
    
    def post(self):
        """
        PointResource POST method. Adds a new point to the database.

        :return: Point, 201 HTTP status code.
        """
        point = PointSchema().load(request.get_json())

        try:
            db.session.add(point)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this point is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return point, 201
