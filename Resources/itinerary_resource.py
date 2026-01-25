from http import HTTPStatus
import logging
from flask import Blueprint, g, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from Schemas.itinerary_shema import ItinerarySchema
from Models.itinerary import Itinerary
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner

# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

ITINERARY_ENDPOINT = "/api/itinerary"
itinerary_api = Blueprint("itinerary", __name__, url_prefix=ITINERARY_ENDPOINT)


def __retrieve_itinerary_by_id(id: int):
    return Itinerary.query.filter_by(id=id).first()


@itinerary_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('itinerary')
def get_all_itineraries():
    """GET /api/itinerary - Retrieve all itineraries"""
    try:
        logger.info("Retrieve all itineraries from db")
        itineraries = db.session.query(Itinerary, user_id=g.current_user_id)

        return jsonify([ItinerarySchema().dump(itinerary) for itinerary in itineraries]), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error retrieving itineraries: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@itinerary_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('itinerary')
def get_itinerary(id: int):
    """GET /api/itinerary/<id> - Retrieve itinerary by ID"""
    logger.info(f"Retrieve itinerary with id {id}")
    
    itinerary = db.session.get(Itinerary, id)
    
    if not itinerary:
        abort(HTTPStatus.NOT_FOUND, description=f"Itinerary with id {id} not found")
    
    return jsonify(ItinerarySchema().dump(itinerary)), HTTPStatus.OK

@itinerary_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('itinerary')
def create_itinerary():
    """POST /api/itinerary/create - Create new itinerary"""
    try:
        itinerary = ItinerarySchema().load(request.get_json())
        db.session.add(itinerary)
        db.session.commit()
        
        return jsonify(ItinerarySchema().dump(itinerary)), HTTPStatus.CREATED
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error creating itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@itinerary_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('itinerary')
def update_itinerary(id: int):
    """POST /api/itinerary/<id>/update - Update existing itinerary"""
    try:
        logger.info(f"Update itinerary {id} in db")
        
        existing_itinerary = db.session.get(Itinerary, id)
        
        if not existing_itinerary:
            abort(HTTPStatus.NOT_FOUND, description=f"Itinerary with id {id} not found")
        
        itinerary_data = request.get_json()
        updated_itinerary = ItinerarySchema().load(itinerary_data)
        
        db.session.merge(updated_itinerary)
        db.session.commit()
        db.session.refresh(updated_itinerary)
        
        return jsonify(ItinerarySchema().dump(updated_itinerary)), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error updating itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@itinerary_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('itinerary')
def delete_itinerary(id: int):
    """DELETE /api/itinerary/<id> - Delete itinerary by ID"""
    try:
        logger.info(f"Deleting itinerary {id}")
        
        itinerary = db.session.get(Itinerary, id)
        
        if not itinerary:
            abort(HTTPStatus.NOT_FOUND, description=f"Itinerary with id {id} not found")
        
        db.session.delete(itinerary)
        db.session.commit()
        
        logger.info(f"Itinerary with id {id} successfully deleted")
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error deleting itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete itinerary due to existing references")
    except Exception as e:
        logger.error(f"Error deleting itinerary: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
