from http import HTTPStatus
import logging
from flask import Blueprint, jsonify, abort
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from Schemas.image_schema import ImageSchema 
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
from Services.image_service import ImageService

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

IMAGE_ENDPOINT = "/api/image"
image_api = Blueprint('image', __name__, url_prefix=IMAGE_ENDPOINT)

@image_api.route("/<string:public_id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('image')
def get_image(public_id: str):
    """GET /api/image/<id> - Retrieve image by ID"""
    image = ImageService.get_image_by_id(public_id)
    if not image:
        abort(HTTPStatus.NOT_FOUND, description=f"Image with id {public_id} not found")

    return jsonify(ImageSchema().dump(image)), HTTPStatus.OK

@image_api.route("/<string:public_id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('image')
def delete_image(public_id: str):
    """DELETE /api/image/<id> - Delete image by ID"""
    try:
        ImageService.delete_image(public_id)
        
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        # Re-raise HTTP exceptions to let global handler format them
        raise

    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Image with id {public_id} not found")
    except IntegrityError as e:
        logger.error(f"Integrity error deleting image {public_id}: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete image due to existing references")
    except Exception as e:
        logger.error(f"Error deleting image {public_id}: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))