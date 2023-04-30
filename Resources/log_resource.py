import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.log_schema import LogSchema 
from Models.log import Log
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

LOG_ENDPOINT = "/api/log/<id>"

class LogResource(Resource):

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

    def post(self):
        """
        LogResource POST method. Adds a new log to the database.

        :return: Log, 201 HTTP status code.
        """
        log = LogSchema().load(request.get_json())

        try:
            db.session.add(log)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this log is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return log, 201
