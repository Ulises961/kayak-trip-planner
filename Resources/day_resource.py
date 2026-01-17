from http import HTTPStatus
import logging
from typing import Any, Dict, List, cast
from flask import Blueprint, jsonify, request
from Api.database import db
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError, NoResultFound
from Schemas.day_schema import DaySchema
from Models.day import Day
from Services.jwt_service import JWTService

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

DAY_ENDPOINT = "/api/day"
day_api = Blueprint('day', __name__, url_prefix=DAY_ENDPOINT)

@day_api.route("/itinerary/<int:itinerary_id>", methods=['GET'])
def read_by_itinerary(itinerary_id: int):
    days = Day.query.filter_by(itinerary_id=itinerary_id)
    return jsonify([DaySchema().dump(day) for day in days]), 200

@day_api.route("/read_by_ids", methods=['POST'])
def read_by_ids():
    body = request.get_json()
    ids: List[int] = body.get("ids", None)
    if not ids:
        abort(HTTPStatus.BAD_REQUEST, description = "Missing day ids")
    days = Day.query.filter(Day.id.in_(ids))
    return jsonify([DaySchema().dump(day) for day in days]), 200

@day_api.route("/by-key", methods=['POST'])
def read_by_key():
    body = request.get_json()
    key: Dict[str, Any] = body.get("key", None)
    if not key:
        abort(HTTPStatus.BAD_REQUEST, description = "Missing day keys")

    day = Day.query.filter_by(day_number=key['day_number'], date=key['date'], itinerary_id=key['itinerary_id']).first()
    return jsonify(DaySchema().dump(day)), 200

@day_api.route("/create", methods=["POST"])
def create_day():
    """POST /api/day - Create new day"""
    day = DaySchema().load(request.get_json())
    db.session.add(day)
    db.session.commit()
    return jsonify(DaySchema().dump(day)), 201

@day_api.route("/update", methods=['POST'])
def update_day():
    """POST /api/day/update - Update existing day"""
    try:
        day_data = request.get_json()
        
        if not day_data or 'id' not in day_data:
            abort(HTTPStatus.BAD_REQUEST, description="Missing day id")
        
        day_id = day_data.pop('id')  # Remove id from update data
        
        # Get the existing day
        existing_day = Day.query.filter_by(id=day_id).first()
        
        if not existing_day:
            abort(HTTPStatus.NOT_FOUND, description=f"Day with id {day_id} not found")
        
        # Validate with schema (partial=True allows updating subset of fields)
        schema = DaySchema(partial=True)
        validated_data:dict = cast(dict,schema.load(day_data))
        
        # Update only the provided fields
        for key, value in validated_data.items():
            setattr(existing_day, key, value)
        
        db.session.commit()
        db.session.refresh(existing_day)
        
        return jsonify(schema.dump(existing_day)), HTTPStatus.OK
        
    except IntegrityError as e:
        logger.error(f"Integrity error updating day: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating day: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@day_api.route("/delete/<int:id>", methods=["DELETE"])
def delete_day(id: int):
    """DELETE /api/day/delete/<id> - Delete day by ID"""
    try:
        day_to_delete = Day.query.get(id)
        
        if not day_to_delete:
            abort(HTTPStatus.NOT_FOUND, description=f"Day with id {id} not found")
        
        db.session.delete(day_to_delete)
        db.session.commit()
        
        logger.info(f"Day with id {id} successfully deleted")
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except IntegrityError as e:
        logger.error(f"Integrity error deleting day: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete day due to existing references")
    except Exception as e:
        logger.error(f"Error deleting day: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))