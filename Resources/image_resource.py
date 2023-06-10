import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.image_schema import ImageSchema 
from Models.image import Image
from flask import request
from sqlalchemy.exc import IntegrityError
from Api.database import db

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

IMAGE_ENDPOINT = "/api/image"

class ImageResource(Resource):

    def __retrieve_image_by_id(self,id):
        return Image.query.filter_by(id = id).first()
    
    def get(self, id=None):
        """
        ImageResource GET method. Retrieves the information related to the image with the passed id in the request
        """
         
        try:
            id = request.args.get('id')
            image = self.__retrieve_image_by_id(id)
            image_json = ImageSchema().dump(image)
            if not image_json:
                raise NoResultFound()
            return image_json,200
        except NoResultFound:
                abort(404, message="No images available")
        except Exception as e:
            abort(500, message=f"Error:{e}")
    
    def post(self):
        """
        ImageResource POST method. Adds a new image to the database.

        :return: Image, 201 HTTP status code.
        """

        try:
            image = ImageSchema().load(request.get_json())
            db.session.add(image)
            db.session.commit()
            image = self.__retrieve_image_by_id(image.id)
            return ImageSchema().dump(image), 201
        
        except IntegrityError as e:
            db.session.rollback()
            logger.error(
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        
    def put(self):
        try:
            logger.info(f"Update image {request.get_json()} in db")
            image = ImageSchema().load(request.get_json())
            db.session.merge(image)
            db.session.commit()
            image = self.__retrieve_image_by_id(image.id)
            return ImageSchema().dump(image), 201

        except Exception as e:
            logger.error(
                f"Error: {e}"
            )
            db.session.rollback()
            abort(500, message="Error: {e}")

    def delete(self):
        try:
            image_id = request.args.get('id')
            logger.info(f"Deleting image {image_id} ")

            image = self.__retrieve_image_by_id(image_id)
            db.session.delete(image)
            db.session.commit()
            logger.info(f"Image with id {image_id} successfully deleted")
            return "Deletion successful", 200

        except Exception as e:
            db.session.rollback()
            abort(
                500, message=f"Error: {e}")
