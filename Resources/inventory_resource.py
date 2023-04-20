import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.inventory_schema import InventorySchema
from Models.inventory import Inventory
from flask import request
from sqlalchemy.exc import IntegrityError
from database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/inventory/<id>"

class InventoryResource(Resource):

    def retrieveInventoryById(id):
        inventory = Inventory.query.filter_by('id', id).first()
        inventory_json = InventorySchema.dump(inventory)
        if not inventory_json:
             raise NoResultFound()
        return inventory_json
    
    def get(self, id=None):
        """
        InventoryResource GET method. Retrieves the information related to the inventory with the passed id in the request
        """
        try:
            self.retrieveInventoryById(id)
        except NoResultFound:
                abort(404, message=f"Inventory with id {id} not found in database")
    
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
            return inventory, 201
