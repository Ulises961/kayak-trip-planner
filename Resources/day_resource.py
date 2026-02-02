from http import HTTPStatus
import logging
from datetime import date
from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from Schemas.day_schema import DaySchema
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
from Services.day_service import DayService

logger = logging.getLogger(__name__)

DAY_ENDPOINT = "/api/day"
day_api = Blueprint('day', __name__, url_prefix=DAY_ENDPOINT)

@day_api.route("/itinerary/<int:itinerary_id>", methods=['GET'])
@JWTService.authenticate_restful
@require_owner('day', parent_resource=('itinerary', 'itinerary_id'))
def read_by_itinerary(itinerary_id: int):
    days = DayService.get_by_itinerary(itinerary_id)
    return jsonify([DaySchema().dump(day) for day in days]), HTTPStatus.OK


@day_api.route("/<int:id>", methods=['GET'])
@JWTService.authenticate_restful
def read_by_id(id: int):
    try:
        day = DayService.get_day_by_id(id)
        return jsonify(DaySchema().dump(day)), HTTPStatus.OK
    except HTTPException:
        raise
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@day_api.route("/by-key", methods=['POST'])
@JWTService.authenticate_restful
@require_owner('day', parent_resource=('itinerary', 'itinerary_id'), from_body=True)
def read_by_key():
    try:
        body = request.get_json()

        if not body or not body.get("day_number") or not body.get("date") or not body.get("itinerary_id"):
            abort(HTTPStatus.BAD_REQUEST, description="Missing or incomplete day key")

        # Convert date string if needed
        day_date = body['date']
        if isinstance(day_date, str):
            day_date = date.fromisoformat(day_date)

        day = DayService.get_by_key(
            day_number=body['day_number'],
            day_date=day_date,
            itinerary_id=body['itinerary_id']
        )
        return jsonify(DaySchema().dump(day)), HTTPStatus.OK
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading day by key: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@day_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('day', parent_resource=('itinerary', 'itinerary_id'), from_body=True)
def create_day():
    """POST /api/day - Create new day"""
    try:
        created_day = DayService.create_day(request.get_json())
        return jsonify(DaySchema().dump(created_day)), HTTPStatus.CREATED
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error creating day: {e}")
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating day: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@day_api.route("/<int:id>/update", methods=['POST'])
@JWTService.authenticate_restful
@require_owner('day')
def update_day(id: int):
    """POST /api/day/update - Update existing day"""
    try:
        day_data = request.get_json()
        updated_day = DayService.update_day(id, day_data)
        return jsonify(DaySchema().dump(updated_day)), HTTPStatus.OK
    except HTTPException:
        raise
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except IntegrityError as e:
        logger.error(f"Integrity error updating day: {e}")
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating day: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@day_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('day')
def delete_day_by_id(id: int):
    """DELETE /api/day/<id> - Delete day by ID"""
    try:
        DayService.delete_day(id)
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
    except HTTPException:
        raise
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except IntegrityError as e:
        logger.error(f"Integrity error deleting day: {e}")
        abort(HTTPStatus.CONFLICT, description="Cannot delete day due to existing references")
    except Exception as e:
        logger.error(f"Error deleting day: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))