import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.log_schema import LogSchema 
from Models.log import Log
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

LOG_ENDPOINT = "/api/log"

class LogResource(Resource):

    def retrieveLogById(self, id):
        return Log.query.filter_by(id=id).first()
    
    def get(self):
        """
        LogResource GET method. Retrieves the information related to the image with the passed id in the request
        """
        
        id = request.args.get('id')
        
        if id:
            try:
                log = self.retrieveLogById(id)
                return LogSchema().dump(log)
            except NoResultFound:
                abort(404, message=f"Log with id {id} not found in database")
        else: 
            abort(404, message=f"Missing id parameter")

    def post(self):
        """
        LogResource POST method. Adds a new log to the database.

        :return: Log, 201 HTTP status code.
        """
        log_json = request.get_json()
        
        log = LogSchema().load(log_json)

        try:
            db.session.add(log)
            db.session.commit()
        except IntegrityError as e:
            logger.error(
                f"Integrity Error, this log is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return LogSchema().dump(log), 201
        
    def put(self):
        try:
            logger.info(f"Update log {request.get_json()} in db")
            updatedLog = LogSchema().load(request.get_json())
            db.session.merge(updatedLog)
            db.session.commit()
            log = Log.query.filter_by(id=updatedLog.id).first()
        
            return LogSchema().dump(log), 201
        
        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")
    
    def delete(self):
        try:
            log_id = request.args.get('id')
            logger.info(f"Deleting log {log_id} ")

            log = self.retrieveLogById(log_id)
            db.session.delete(log)
            db.session.commit()
            logger.info(f"Log with id {log_id} successfully deleted")
            return "Deletion successful", 200
        
        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
