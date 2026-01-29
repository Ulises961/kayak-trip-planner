from http import HTTPStatus
import logging
from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from Schemas.item_schema import ItemSchema
from Services.item_service import ItemService
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
from Api.database import db
logger = logging.getLogger(__name__)

ITEM_ENDPOINT = "/api/item"
item_api = Blueprint('item', __name__, url_prefix=ITEM_ENDPOINT)

@item_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('item')
def get_item(id: int):
    """GET /api/item/<id> - Retrieve item by ID"""
    try:
        item = ItemService.get_item_by_id(id)
        return jsonify(ItemSchema().dump(item)), HTTPStatus.OK
    
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Item with id {id} not found")
    except Exception as e:
        logger.error(f"Error retrieving item: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@item_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('item', parent_resource=('inventory', 'inventory_id'), from_body=True)
def create_item():
    """POST /api/item/create - Create new item"""
    try:
        item_data = request.get_json()
        item = ItemService.create_item(item_data)
        return jsonify(ItemSchema().dump(item)), HTTPStatus.CREATED
    
    except HTTPException:
        raise
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@item_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('item')
def update_item(id: int):
    """POST /api/item/<id>/update - Update existing item"""
    try:
        logger.info(f"Update item {id} in db")
        item_data = request.get_json()
        item = ItemService.update_item(id, item_data)
        return jsonify(ItemSchema().dump(item)), HTTPStatus.OK
        
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Item with id {id} not found")
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@item_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('item')
def delete_item(id: int):
    """DELETE /api/item/<id> - Delete item by ID"""
    try:
        logger.info(f"Deleting item {id}")
        ItemService.delete_item(id)
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error deleting item: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete item due to existing references")
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
