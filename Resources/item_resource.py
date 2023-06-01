import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.item_schema import ItemSchema
from Models.item import Item
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db


# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

ITEM_ENDPOINT = "/api/item"


class ItemResource(Resource):

    def __retrieve_item_by_id(self,id):
        return Item.query.filter_by(id=id).first()

    def get(self):
        """
        ItemResource GET method. Retrieves the information related to the image with the passed id in the request
        """
        try:
            id = request.args.get("id")
            if id:
                item = self.__retrieve_item_by_id(id)
                item_json = ItemSchema().dump(item)
                if not item_json:
                    raise NoResultFound()
                return item_json, 200
        except NoResultFound:
            abort(404, message=f"Image with id {id} not found in database")

    def post(self):
        """
        ItemResource POST method. Adds a new item to the database.

        :return: Item, 201 HTTP status code.
        """
        try:
            item = ItemSchema().load(request.get_json())
            db.session.add(item)
            db.session.commit()
            item = self.__retrieve_item_by_id(item.id)
            return ItemSchema().dump(item), 201

        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error: {e}")
            abort(500, message="Unexpected Error!")
            

    def put(self):
        try:
            logger.info(f"Update item {request.get_json()} in db")
            item = ItemSchema().load(request.get_json())
            db.session.merge(item)
            db.session.commit()
            item = self.__retrieve_item_by_id(item.id)
            return ItemSchema().dump(item), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self):
        try:
            item_id = request.args.get('id')
            logger.info(f"Deleting item {item_id} ")

            item = self.__retrieve_item_by_id(item_id)
            db.session.delete(item)
            db.session.commit()
            logger.info(f"Item with id {item_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
