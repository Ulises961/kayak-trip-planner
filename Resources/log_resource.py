from http import HTTPStatus
from http.client import HTTPException
import logging
from flask import Blueprint, abort, g, jsonify, request
from sqlalchemy.exc import IntegrityError
from Schemas.log_schema import LogSchema 
from Api.database import db
from Services.Middleware.auth_middleware import JWTService
from Services.Middleware.privileges_middleware import require_owner
from Services.log_service import LogService


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

LOG_ENDPOINT = "/api/log"
log_api = Blueprint('log', __name__, url_prefix=LOG_ENDPOINT)


@log_api.route("/all", methods=["GET"])
@JWTService.authenticate_restful
def get_logs():
    """
    LogResource GET method. Retrieves all the logs associated to a user
    """
    try:        
        logs = LogService.get_logs_by_user(g.current_user_id)
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
        
        logs = LogService.get_endorsed_logs(g.current_user_id) 
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
        log = LogService.create_log(log_json)
        return jsonify(LogSchema().dump(log)), HTTPStatus.CREATED
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this log is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating log: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@log_api.route("/<string:public_id>/update", methods=["POST"])
@JWTService.authenticate_restful
@require_owner('log')
def update_log(public_id: str):
    try:
        updated_log = LogService.update_log(public_id, request.get_json())

        return jsonify(LogSchema().dump(updated_log)), HTTPStatus.OK
    
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.error(
            f"Integrity Error, this log is already in the database. Error: {e}"
        )
        db.session.rollback()
        abort(HTTPStatus.CONFLICT, description="Database integrity violated")

    except Exception as e:
        logger.error(f"Error creating log: {e}")
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

@log_api.route("/<string:public_id>", methods=["DELETE"])
@JWTService.authenticate_restful
@require_owner('log')
def delete_log(public_id: str):
    try:
        logger.info(f"Deleting log with id {public_id} ")

        log = LogService.delete_log(public_id)
        if not log:
            abort(HTTPStatus.NOT_FOUND, description=f"Log with id {public_id} not found")

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