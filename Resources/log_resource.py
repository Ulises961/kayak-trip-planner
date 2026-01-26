from http import HTTPStatus
from http.client import HTTPException
import logging
from typing import cast
from flask import Blueprint, abort, g, jsonify, request
from sqlalchemy.exc import NoResultFound, IntegrityError
from Models.user import User
from Schemas.log_schema import LogSchema 
from Models.log import Log
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

LOG_ENDPOINT = "/api/log"
log_api = Blueprint('log', __name__, url_prefix=LOG_ENDPOINT)

def retrieveLogById(id: int):
    return db.session.query(Log, id=id).first()

@log_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
@require_owner('log')
def get_logs():
    """
    LogResource GET method. Retrieves all the logs associated to a user
    """
    try:        
        logs = db.session.query(Log, user_id=g.current_user_id)
        return jsonify([LogSchema().dump(log) for log in logs]), HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"{e}")



@log_api.route("/endorsed", methods=["GET"])
@JWTService.authenticate_restful
def get_endorsed_logs():
    """
    LogResource GET method. Retrieves all the logs associated to a user
    """
    try:        
        user = cast(User, db.session.query(User, id=g.user_current_id).join(User.endorsed_logs))
        logs = user.endorsed_logs 
        return jsonify([LogSchema().dump(log) for log in logs]), HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"{e}")


@log_api.route("/create", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('log')
def post():
    """
    LogResource POST method. Adds a new log to the database.

    :return: Log, 201 HTTP status code.
    """
    try:
        log_json = request.get_json()
        log = LogSchema().load(log_json)
        db.session.add(log)
        db.session.commit()
        return jsonify(LogSchema().dump(log)), HTTPStatus.CREATED
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this log is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, message="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating log: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@log_api.route("/<int:id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('log')
def update_log(id: int):
    try:
        existing_log = db.session.query(Log, id=id)

        if not existing_log:
            abort(HTTPStatus.NOT_FOUND, description="Log with id {id} not found")

        updated_log = LogSchema().load(request.get_json())
        
        db.session.merge(update_log)
        db.session.commit()
        db.session.refresh(updated_log)

        return LogSchema().dump(update_log), HTTPStatus.OK
    
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this log is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, message="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating log: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@log_api.route("/<int:id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('log')
def delete_log(id: int):
    try:
        logger.info(f"Deleting log with id {id} ")

        log = retrieveLogById(id)
        if not log:
            abort(HTTPStatus.NOT_FOUND, description=f"Log with id {id} not found")

        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Deletion successful"}), HTTPStatus.OK
    
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this log is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, message="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating log: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))