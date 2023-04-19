import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.log_schema import LogSchema 
from Models.log import Log


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/log/<id>"

class ImageResource(Resource):

    def retrieveLogById(id):
        log = Log.query.filter_by('id', id).first()
        log_json = LogSchema.dump(log)
        if not log_json:
             raise NoResultFound()
        return log_json
    
    def get(self, id=None):
        """
        LogResource GET method. Retrieves the information related to the image with the passed id in the request
        """
        if id:
            try:
                self.retrieveLogById(id)
            except NoResultFound:
                abort(404, message=f"Log with id {id} not found in database")
        else: 
            abort(404, message=f"Missing id parameter")