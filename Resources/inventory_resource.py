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

    def retrieveInventoryById(self, id):
        inventory = Inventory.query.filter_by(id=id).first()
        inventory_json = InventorySchema().dump(inventory)
        if not inventory_json:
            raise NoResultFound()
        return inventory_json
    
    def get(self):
        """
        InventoryResource GET method. Retrieves the information related to the inventory with the passed id in the request
        """
        
        inventory_id = None
        
        try:
            inventory_id = request.args.get('id')
        except ValueError:
            db.session.rollback()
            abort(500, message=f"Missing parameters, {ValueError}")
            
        if inventory_id:
            logger.info(f"Retrive inventory with id {inventory_id}")

            try:
                json = self.retrieveInventoryById(id=inventory_id)
                return json, 200
            except NoResultFound:
                db.session.rollback()
                abort(404, message=f"Inventory with id {inventory_id} not found in database")
        else:
            logger.info(f"Retrive all inventories from db")
            try:
                inventories = Inventory.query.all()
                inventories_json = [InventorySchema().dump(inventory) for inventory in inventories]
                return inventories_json, 200
            
            except IntegrityError:
                db.session.rollback()
                abort(500, message=f"Error while retrieving days")
    
    def post(self):
        """
        InventoryResource POST method. Adds a new inventory to the database.

        :return: Inventory, 201 HTTP status code.
        """
        inventory = InventorySchema().load(request.get_json())

        try:
            db.session.add(inventory)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this inventory is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return InventorySchema().dump(inventory), 201
        
    def put(self):

        logger.info(f"Update trip {request.get_json()} in db")
        updatedInventory = InventorySchema().load(request.get_json())
        
        try:
            db.session.merge(updatedInventory)
            db.session.commit()
    
        except TypeError as e:
            logger.warning(
                f"Missing parameters. Error: {e}")
            abort(500, message="Missing parameters")

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error: {e}"
            )
            abort(500, message="Unexpected Error!")

        else:
            inventory = Inventory.query.filter_by(id=updatedInventory.id).first()
            return InventorySchema().dump(inventory), 201
