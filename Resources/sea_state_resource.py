import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_state_schema import SeaStateSchema
from Models.sea_state import SeaState

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/sea_state/<id>"

class SeaResource(Resource):

    def retrieveSeaStateById(id):
        sea_state = SeaState.query.filter_by('id', id).first()
        sea_state_json = SeaStateSchema.dump(sea_state)
        if not sea_state_json:
             raise NoResultFound()
        return sea_state_json
    
    def get(self, id=None):
        """
        SeaResource GET method. Retrieves the information related to the sea state with the passed id in the request
        """
        try:
            self.retrieveSeaStateById(id)
        except NoResultFound:
                abort(404, message=f"Sea State with id {id} not found in database")
        