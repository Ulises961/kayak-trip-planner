from http import HTTPStatus
from http.client import HTTPException
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import NoResultFound
from flask import Blueprint, abort, g, jsonify, request
from Schemas.trip_schema import TripSchema
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
from Services.trip_service import TripService

logger = logging.getLogger(__name__)

TRIP_ENDPOINT = "/api/trip"
## TODO: Trip creation needs a separate microservice different from trip execution to avoid bogging down service through trip creation
## TODO: A trip created is published in Kafka and then stored in db
trip_api = Blueprint("trip", __name__, url_prefix=TRIP_ENDPOINT)


@trip_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner("trip")
def get_trip(id: int):
    """
    TripResource GET method. Retrieves trip(s) by ID or all trips.

    Returns:
        JSON response with trip data and 200 status code
    """
    try:
        logger.info(f"Retrieving trip with id {id}")
        trip = TripService.get_trip_by_id(int(id))
        return jsonify(TripSchema().dump(trip)), HTTPStatus.OK

    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Trip with id {id} not found")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@trip_api.route("/<int:user_id>/all", methods=["GET"])
@JWTService.authenticate_restful
def get_all_user_trips(user_id: int):
    """
    TripResource GET method. Retrieves trip(s) by ID or all trips.

    Returns:
        JSON response with trip data and 200 status code
    """
    try:
        logger.info(f"Retrieving trip with id {id}")
        trips = TripService.get_trips_by_user(user_id)
        return jsonify([TripSchema().dump(trip) for trip in trips]), HTTPStatus.OK

    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Trip with id {id} not found")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@trip_api.route("/<int:user_id>/invitations", methods=["GET"])
@JWTService.authenticate_restful
def get_all_user_invitations(user_id):
    """
    TripResource GET method. Retrieves trip(s) by ID or all trips.

    Returns:
        JSON response with trip data and 200 status code
    """
    try:
        logger.info(f"Retrieving trip with id {id}")
        trips = TripService.get_invitations_by_user(user_id)
        return jsonify([TripSchema().dump(trip) for trip in trips]), HTTPStatus.OK

    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Trip with id {id} not found")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@trip_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
def post():
    """
    TripResource POST method. Adds a new trip to the database.

    Returns:
        JSON response with created trip and 201 status code
    """
    try:
        trip_data = request.get_json()
        trip = TripService.create_trip(trip_data)
        return jsonify(TripSchema().dump(trip)), HTTPStatus.CREATED
    except HTTPException:
        raise
    except IntegrityError as e:
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@trip_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
def put(id:int):
    """
    TripResource PUT method. Updates an existing trip.

    Returns:
        JSON response with updated trip and 200 status code
    """
    try:
        logger.info(f"Update trip {request.get_json()} in db")
        trip_data = request.get_json()
        trip = TripService.update_trip(trip_data)
        return jsonify(TripSchema().dump(trip)), HTTPStatus.OK
    except HTTPException:
        raise
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@trip_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
def delete(id: int):
    """
    TripResource DELETE method. Deletes a trip by ID.

    Returns:
        Success message and 200 status code
    """
    try:
        delete_to_all_participants = request.args.get("for_everyone",False, type=bool)
        
        logger.info(f"Deleting trip {id}")
        TripService.delete_trip(int(id), delete_to_all_participants)
        return {"message": "Deletion successful"}, HTTPStatus.OK
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

