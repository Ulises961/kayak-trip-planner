from http import HTTPStatus
import logging
from typing import Any, Dict, List, cast
from datetime import date
from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from Api.database import db
from sqlalchemy.exc import IntegrityError
from Schemas.day_schema import DaySchema
from Schemas.sea_schema import SeaSchema
from Schemas.weather_schema import WeatherSchema
from Models.day import Day
from Models.sea import Sea
from Models.weather import Weather
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner

logger = logging.getLogger(__name__)

DAY_ENDPOINT = "/api/day"
day_api = Blueprint('day', __name__, url_prefix=DAY_ENDPOINT)

@day_api.route("/itinerary/<int:itinerary_id>", methods=['GET'])
@JWTService.authenticate_restful
@require_owner('day')
def read_by_itinerary(itinerary_id: int):
    days = db.session.query(Day).filter_by(itinerary_id=itinerary_id).all()
    return jsonify([DaySchema().dump(day) for day in days]), HTTPStatus.OK

@day_api.route("/read_by_ids", methods=['POST'])
@JWTService.authenticate_restful
@require_owner('day')
def read_by_ids():
    body = request.get_json()
    ids: List[int] = body.get("ids", None)
    if not ids:
        abort(HTTPStatus.BAD_REQUEST, description = "Missing day ids")
    days = db.session.query(Day).filter(Day.id.in_(ids)).all()
    return jsonify([DaySchema().dump(day) for day in days]), HTTPStatus.OK

@day_api.route("/by-key", methods=['POST'])
@JWTService.authenticate_restful
@require_owner('day')
def read_by_key():
    body = request.get_json()

    if not body or not body.get("day_number") or not body.get("date") or not body.get("itinerary_id"):
        abort(HTTPStatus.BAD_REQUEST, description = "Missing or incomplete day key")

    day = db.session.query(Day).filter_by(day_number=body['day_number'], date=body['date'], itinerary_id=body['itinerary_id']).first()
    return jsonify(DaySchema().dump(day)), HTTPStatus.OK

@day_api.route("", methods=["POST"])
@day_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('day')
def create_day():
    """POST /api/day - Create new day"""
    day = DaySchema().load(request.get_json())
    db.session.add(day)
    db.session.commit()
    return jsonify(DaySchema().dump(day)), HTTPStatus.CREATED

@day_api.route("/<int:id>/update", methods=['POST'])
@JWTService.authenticate_restful
@require_owner('day')
def update_day(id:int):
    """POST /api/day/update - Update existing day"""
    try:
        day_data = request.get_json()
     
        # Get the existing day
        existing_day = db.session.get(Day, id)
        
        if not existing_day:
            abort(HTTPStatus.NOT_FOUND, description=f"Day with id {id} not found")
        
        # Check if nested objects are present in the request (even if None)
        has_weather_key = 'weather' in day_data
        has_sea_key = 'sea' in day_data
        
        # Handle nested objects (weather and sea) separately
        weather_data = day_data.pop('weather', None)
        sea_data = day_data.pop('sea', None)
        
        # Update simple fields directly from day_data (skip id)
        for key, value in day_data.items():
            if key == 'id':
                continue
            if hasattr(existing_day, key):
                # Convert date string to date object if needed
                if key == 'date' and isinstance(value, str):
                    value = date.fromisoformat(value)
                setattr(existing_day, key, value)
        
        # Handle weather update/creation - only if key was present
        if has_weather_key:
            if weather_data:  # Non-null weather data
                weather_obj = cast(Weather, WeatherSchema().load(weather_data))
                if existing_day.weather:
                    # Update existing weather
                    for key, value in weather_data.items():
                        if hasattr(existing_day.weather, key):
                            setattr(existing_day.weather, key, value)
                else:
                    # Create new weather
                    existing_day.weather = weather_obj
            else:  # Null weather data - remove association
                if existing_day.weather:
                    db.session.delete(existing_day.weather)
                    existing_day.weather = None
        
        # Handle sea update/creation - only if key was present
        if has_sea_key:
            if sea_data:  # Non-null sea data
                sea_obj = cast(Sea, SeaSchema().load(sea_data))
                if existing_day.sea:
                    # Update existing sea
                    for key, value in sea_data.items():
                        if hasattr(existing_day.sea, key):
                            setattr(existing_day.sea, key, value)
                else:
                    # Create new sea
                    existing_day.sea = sea_obj
            else:  # Null sea data - remove association
                if existing_day.sea:
                    db.session.delete(existing_day.sea)
                    existing_day.sea = None
        
        db.session.commit()
        db.session.refresh(existing_day)
        
        return jsonify(DaySchema().dump(existing_day)), HTTPStatus.OK
        
    except HTTPException:
        # Re-raise HTTP exceptions (like abort calls)
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error updating day: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating day: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@day_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('day')
def delete_day_by_id(id: int):
    """DELETE /api/day/<id> - Delete day by ID"""
    try:
        day_to_delete = db.session.get(Day, id)
        
        if not day_to_delete:
            abort(HTTPStatus.NOT_FOUND, description=f"Day with id {id} not found")
        
        db.session.delete(day_to_delete)
        db.session.commit()
        
        logger.info(f"Day with id {id} successfully deleted")
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        # Re-raise HTTP exceptions (like abort calls)
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error deleting day: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete day due to existing references")
    except Exception as e:
        logger.error(f"Error deleting day: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))