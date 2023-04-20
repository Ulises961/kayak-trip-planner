import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_schema import SeaSchema
from Models.sea import Sea

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/sea/<id>"

class SeaResource(Resource):

    def retrieveSeaById(id):
        sea = Sea.query.filter_by('id', id).first()
        sea_json = SeaSchema.dump(sea)
        if not sea_json:
             raise NoResultFound()
        return sea_json
    
    def get(self, id=None):
        """
        SeaResource GET method. Retrieves the information related to the sea with the passed id in the request
        """
        try:
            self.retrieveSeaById(id)
        except NoResultFound:
                abort(404, message=f"Sea with id {id} not found in database")
        