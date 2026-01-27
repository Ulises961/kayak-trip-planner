from http import HTTPStatus
import logging
from flask import Blueprint, jsonify, request, abort, g
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from Models.trip import Trip
from Models.user import User
from Schemas.inventory_schema import InventorySchema
from Models.inventory import Inventory
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
logger = logging.getLogger(__name__)

INVENTORY_ENDPOINT = "/api/inventory"
inventory_api = Blueprint('inventory', __name__, url_prefix=INVENTORY_ENDPOINT)

@inventory_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('inventory')
def get_all_inventories():
    """GET /api/inventory - Retrieve all inventories"""
    try:
        logger.info("Retrieve all inventories from db")
        inventories = db.session.query(Inventory, user_id=g.current_user_id)
        return jsonify([InventorySchema().dump(inventory) for inventory in inventories]), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error retrieving inventories: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('inventory')
def get_inventory(id: int):
    """GET /api/inventory/<id> - Retrieve inventory by ID"""
    logger.info(f"Retrieve inventory with id {id}")
    
    inventory = db.session.get(Inventory, id)
    
    if not inventory:
        abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
    
    return jsonify(InventorySchema().dump(inventory)), HTTPStatus.OK

@inventory_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('inventory')
def create_inventory():
    """POST /api/inventory - Create new inventory"""
    try:
        inventory = InventorySchema().load(request.get_json())
        db.session.add(inventory)
        db.session.commit()
        
        return jsonify(InventorySchema().dump(inventory)), HTTPStatus.CREATED
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error creating inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('inventory')
def update_inventory(id: int):
    """POST /api/inventory/<id> - Update existing inventory"""
    try:
        logger.info(f"Update inventory {id} in db")
        
        existing_inventory = db.session.get(Inventory, id)
        
        if not existing_inventory:
            abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
        
        inventory_data = request.get_json()

        if "items" in inventory_data:
            if items:= inventory_data.get("items", []):
                existing_inventory.items = items

        updated_inventory = InventorySchema().load(inventory_data)
        
        db.session.merge(updated_inventory)
        db.session.commit()
        db.session.refresh(updated_inventory)
        
        return jsonify(InventorySchema().dump(updated_inventory)), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error updating inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@inventory_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('inventory')
def delete_inventory(id: int):
    """DELETE /api/inventory/<id> - Delete inventory by ID"""
    try:
        logger.info(f"Deleting inventory {id}")
        
        inventory = db.session.get(Inventory, id)
        
        if not inventory:
            abort(HTTPStatus.NOT_FOUND, description=f"Inventory with id {id} not found")
        
        db.session.delete(inventory)
        db.session.commit()
        
        logger.info(f"Inventory with id {id} successfully deleted")
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error deleting inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Cannot delete inventory due to existing references")
    except Exception as e:
        logger.error(f"Error deleting inventory: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
