from http import HTTPStatus
import logging
from flask import Blueprint, jsonify, request, abort, g
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from Schemas.inventory_schema import InventorySchema
from Services.inventory_service import InventoryService
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner

logger = logging.getLogger(__name__)

INVENTORY_ENDPOINT = "/api/inventory"
inventory_api = Blueprint('inventory', __name__, url_prefix=INVENTORY_ENDPOINT)

@inventory_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
def get_all_inventories():
    """GET /api/inventory/all - Retrieve all inventories for current user"""
    try:
        logger.info("Retrieve all inventories from db")
        user_id = g.current_user_id
        inventories = InventoryService.get_inventories_by_user(user_id)
        return jsonify([InventorySchema().dump(inventory) for inventory in inventories]), HTTPStatus.OK
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving inventories: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('inventory')
def get_inventory(id: int):
    """GET /api/inventory/<id> - Retrieve inventory by ID"""
    try:
        logger.info(f"Retrieve inventory with id {id}")
        inventory = InventoryService.get_inventory_by_id(id)
        return jsonify(InventorySchema().dump(inventory)), HTTPStatus.OK
    
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
    except Exception as e:
        logger.error(f"Error retrieving inventory: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
def create_inventory():
    """POST /api/inventory/create - Create new inventory"""
    try:
        inventory_data = request.get_json()
        inventory = InventoryService.create_inventory(inventory_data)
        return jsonify(InventorySchema().dump(inventory)), HTTPStatus.CREATED
        
    except HTTPException:
        raise
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating inventory: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('inventory')
def update_inventory(id: int):
    """POST /api/inventory/<id>/update - Update existing inventory"""
    try:
        logger.info(f"Update inventory {id} in db")
        inventory_data = request.get_json()
        inventory = InventoryService.update_inventory(id, inventory_data)
        return jsonify(InventorySchema().dump(inventory)), HTTPStatus.OK
        
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.exception(f"Error updating inventory: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('inventory')
def delete_inventory(id: int):
    """DELETE /api/inventory/<id> - Delete inventory by ID"""
    try:
        logger.info(f"Deleting inventory {id}")
        InventoryService.delete_inventory(id)
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        raise
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
    except IntegrityError:
        abort(HTTPStatus.CONFLICT, description="Cannot delete inventory due to existing references")
    except Exception as e:
        logger.error(f"Error deleting inventory: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
