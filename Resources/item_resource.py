from http import HTTPStatus
import logging
from typing import cast
from flask import Blueprint, g, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from Schemas.item_schema import ItemSchema
from Models.item import Item
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner


# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

ITEM_ENDPOINT = "/api/item"

item_api = Blueprint('item', __name__, url_prefix=ITEM_ENDPOINT)

def __retrieve_item_by_id(id):
    return db.session.get(Item,id)

@item_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('item')
def get_all_items():
    """GET /api/item - Retrieve all items"""
    try:
        logger.info("Retrieve all items from db")
        items = db.session.query(Item, user_id=g.current_user_id)
        return jsonify([ItemSchema().dump(item) for item in items]), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error retrieving items: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))


@item_api.route("/<int:id>", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('item')
def get_item(id:int):
    """GET /api/item/<id> - Retrieve item"""
    item = __retrieve_item_by_id(id)
    if not item:
        abort(HTTPStatus.NOT_FOUND, message=f"Item with id {id} not found in database")

    return jsonify(ItemSchema().dump(item)), HTTPStatus.OK


@item_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('item')
def create_item():
    """
    ItemResource POST method. Adds a new item to the database.

    :return: Item, 201 HTTP status code.
    """
    try:
        item = cast(Item, ItemSchema().load(request.get_json()))
        db.session.add(item)
        db.session.commit()
        item = __retrieve_item_by_id(item.id)
        return jsonify(ItemSchema().dump(item)), HTTPStatus.CREATED

    
    except HTTPException:
            raise
    except IntegrityError as e:
        logger.error(f"Integrity error creating item: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@item_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('item')
def update_item(id: int):
    """POST /api/item/<id>/update - Update existing item"""
    try:
        logger.info(f"Update item {id} in db")
        
        existing_item = db.session.get(Item, id)
        
        if not existing_item:
            abort(HTTPStatus.NOT_FOUND, description=f"Item with id {id} not found")
        
        item_data = request.get_json()
        updated_item = ItemSchema().load(item_data)
        
        db.session.merge(updated_item)
        db.session.commit()
        db.session.refresh(updated_item)
        
        return jsonify(ItemSchema().dump(updated_item)), HTTPStatus.OK
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(f"Integrity error updating item: {e}")
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity constraint violated")
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@item_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('item')
def delete_item(id: int):
    """DELETE /api/item/<id> - Delete item by ID"""
    try:
        logger.info(f"Deleting item {id}")
        
        item = db.session.get(Item, id)
        
        if not item:
            abort(HTTPStatus.NOT_FOUND, description=f"Item with id {id} not found")
        
        db.session.delete(item)
        db.session.commit()
        
        logger.info(f"Item with id {id} successfully deleted")
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
