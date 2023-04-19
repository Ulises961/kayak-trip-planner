import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.item_schema import ItemSchema 
from Models.item import Item


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/item/<id>"

class ImageResource(Resource):

    def retrieveItemById(id):
        item = Item.query.filter_by('id', id).first()
        item_json = ItemSchema.dump(item)
        if not item_json:
             raise NoResultFound()
        return item_json
    
    def get(self, id=None):
        """
        ItemResource GET method. Retrieves the information related to the image with the passed id in the request
        """
        if id:
            try:
                self.retrieveImageById(id)
            except NoResultFound:
                abort(404, message=f"Image with id {id} not found in database")
        else: 
            abort(404, message=f"Missing id parameter")