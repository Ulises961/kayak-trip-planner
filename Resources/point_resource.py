from http import HTTPStatus
from http.client import HTTPException
import logging
from sqlite3 import IntegrityError
from typing import List
from flask import Blueprint, abort, jsonify, request
from Models.point import Point
from Schemas.point_schema import PointSchema
from Services.Middleware.auth_middleware import JWTService
from Services.point_service import PointService
from Api.database import db
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger(__name__)

POINT_ENDPOINT = "/api/point"
point_api = Blueprint('point', __name__, url_prefix=POINT_ENDPOINT)


## TODO: PoI points need to run as a separate microservice that can be cached and served
## TODO:  When a PoI is created then is shared to kafka or MQrabbit and saved into the db
@point_api.route("/pois", methods=["GET"])
@JWTService.authenticate_restful
def get_poi():
    """
    PointResource GET method. Retrieves point(s) of interest.
        
    Returns:
        JSON response with point data and 200 status code
    """
    try:
        range: float =  request.args.get('range', 0.0, type=float)
        longitude: float = request.args.get('long', 0.0, type=float)
        latitude: float = request.args.get('lat', 0.0, type=float)
        points:List[Point] = PointService.get_points_in_range(range,longitude, latitude)

        return jsonify([PointSchema().dump(point) for point in points])
    except Exception as e:
        logger.error(f"Error retrieving itineraries: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@point_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
def create_point():
    """
    PointResource POST method. Adds a new point to the database.

    Returns:
        JSON response with created point and 201 status code
    """
    try:
        point_data = request.get_json()
        point = PointService.create_point(point_data)
        return jsonify(PointSchema().dump(point)), HTTPStatus.CREATED

    except HTTPException:
            raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this point is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, message="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating point: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@point_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful             
def update_point(id: int):
    """
    PointResource PUT method. Updates an existing point.
    
    Returns:
        JSON response with updated point and 200 status code
    """
    try:
        point_data = request.get_json()
        point = PointService.update_point(id, point_data)
        return jsonify(PointSchema().dump(point)), HTTPStatus.OK

    except HTTPException:
            raise
    except NoResultFound:
         abort(HTTPStatus.NOT_FOUND, description=f"Point with id {id} not found")

    except Exception as e:
        logger.error(f"Error creating point: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@point_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
def get_point(id: int):
    """
    PointResource GET method. Retrieves a single point by ID.
    
    Args:
        id: Point ID to retrieve
        
    Returns:
        JSON response with point data and 200 status code
    """
    try:
        point = PointService.get_point_by_id(id)
        return jsonify(PointSchema().dump(point)), HTTPStatus.OK
    
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Point with id {id} not found")
    
    except Exception as e:
        logger.error(f"Error retrieving point: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@point_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful      
def delete(id:int):
    """
    PointResource DELETE method. Deletes a point by ID.
    
    Args:
        id: Point ID to delete
        
    Returns:
        Success message and 200 status code
    """
    try:
        logger.info(f"Deleting point {id}")
        PointService.delete_point(id)
        return {"message": "Deletion successful"}, 200

    
    except HTTPException:
            raise
    except NoResultFound as e:
        logger.error(
            f"Integrity Error, this point is already in the database. Error: {e}"
        )
        abort(HTTPStatus.NOT_FOUND, message=f"Point with id {id} not found")

    except Exception as e:
        logger.error(f"Error deleting point: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))