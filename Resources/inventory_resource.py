import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.inventory_schema import InventorySchema
from Models.inventory import Inventory
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

INVENTORY_ENDPOINT = "/api/inventory"

class InventoryResource(Resource):

    def __retrieve_inventory_by_id(self, id):
        return Inventory.query.filter_by(id=id).first()
        
    
    def get(self):
        """
        InventoryResource GET method. Retrieves the information related to the inventory with the passed id in the request
        """

        try:
            inventory_id = request.args.get('id')
            if inventory_id:
                logger.info(f"Retrive inventory with id {inventory_id}")

                inventory = self.__retrieve_inventory_by_id(inventory_id)
                inventory_json = InventorySchema().dump(inventory)

                if not inventory_json:
                    raise NoResultFound()
                return inventory_json,200
            else:
                logger.info(f"Retrive all inventories from db")
                
                inventories = Inventory.query.all()
                inventories_json = [InventorySchema().dump(inventory) for inventory in inventories]
                return inventories_json, 200
            
        except IntegrityError:
            db.session.rollback()
            abort(500, message=f"Error while retrieving days")
        
        except NoResultFound:
            db.session.rollback()
            abort(404, message=f"Inventory with id {inventory_id} not found in database")
    
    def post(self):
        """
        InventoryResource POST method. Adds a new inventory to the database.

        :return: Inventory, 201 HTTP status code.
        """
        try:
            inventory = InventorySchema().load(request.get_json())
            db.session.add(inventory)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}"
            )

            abort(500, message=f"Error:{e}")
        else:
            return InventorySchema().dump(inventory), 201
        
    def put(self):
        try:
            logger.info(f"Update trip {request.get_json()} in db")
            updatedInventory = InventorySchema().load(request.get_json())
            db.session.merge(updatedInventory)
            db.session.commit()
            inventory = Inventory.query.filter_by(id=updatedInventory.id).first()
        
            return InventorySchema().dump(inventory), 201
        
        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")
    
    def delete(self):
        try:
            inventory_id = request.args.get('id')
            logger.info(f"Deleting inventory {inventory_id} ")

            inventory_to_delete = self.__retrieve_inventory_by_id(inventory_id)
            db.session.delete(inventory_to_delete)
            db.session.commit()
            logger.info(f"Inventory with id {inventory_id} successfully deleted")
            return "Deletion successful", 200
        
        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
