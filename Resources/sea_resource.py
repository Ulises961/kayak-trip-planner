import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.sea_schema import SeaSchema
from Models.sea import Sea
from flask import request
from Api.database import db


# It will print the name of this module when the main app is running
logger = logging.getLogger(__name__)

SEA_ENDPOINT = "/api/sea"


class SeaResource(Resource):

    def __retrieve_sea_by_key(self, day_id):
        return Sea.query.filter_by(
            day_id=day_id).first()

    def get(self, day_id=None):
        """
        SeaResource GET method. Retrieves the information related to the sea with the passed keys in the request
        """
        try:
            if day_id:
                sea = self.__retrieve_sea_by_key(day_id)
                sea_json = SeaSchema().dump(sea)
                if not sea_json:
                    raise NoResultFound()
                return sea_json, 200
            else:
                logger.info(f"Retrive all seas from db")
                seas = Sea.query.all()
                sea_json = [SeaSchema().dump(sea) for sea in seas]
                if len(sea_json) == 0:
                    raise NoResultFound()
                return sea_json, 200
            
        except NoResultFound:
            abort(
                404, message=f"Sea not found in database")
        except Exception as e:
            abort(500, message=f"Error:{e}")

    def post(self):
        """
        SeaResource POST method. Adds a new sea to the database.
        :return: Sea, 201 HTTP status code.
        """

        try:
            sea = SeaSchema().load(request.get_json())
            logger.info(
                f"Inserting sea: {sea}"
            )
            db.session.add(sea)
            db.session.commit()
            sea = self.__retrieve_sea_by_key(
                sea.day_id,
            )
            return SeaSchema().dump(sea), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def put(self):
        """
        Sea Resource POST method. Updates an existing user.

        :return: Sea, 201 HTTP status code.
        """

        try:
            updated_sea = SeaSchema().load(request.get_json())
            db.session.merge(updated_sea)
            db.session.commit()
            updated_sea = self.__retrieve_sea_by_key(
                updated_sea.day_id,
            )
            logger.info(
                f"Sea: {updated_sea}"
            )
            return SeaSchema().dump(updated_sea), 201

        except Exception as e:
            logger.error(
                f"Error: {e}")
            db.session.rollback()
            abort(500, message=f"Error:{e}")

    def delete(self, day_id=None):
        """
        Sea Resource DELETE method. Eliminates an existing sea from the db.

        :return: Deletion successful,200 HTTP status code. | 500, Error
        """

        try:
            logger.info(
                f"Deleting sea with day_id{day_id}")
            sea_to_delete = self.__retrieve_sea_by_key(day_id)

            db.session.delete(sea_to_delete)
            db.session.commit()
            logger.info(
                f"Sea with id{sea_to_delete.day_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}")
            abort(
                500, message=f"Error: {e}")
