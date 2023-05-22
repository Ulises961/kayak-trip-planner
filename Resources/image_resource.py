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

    def retrieveImageById(id):
        image = Image.query.filter_by('id', id).first()
        image_json = ImageSchema.dump(image)
        if not image_json:
             raise NoResultFound()
        return image_json

    def retrieveAllImages():
        images = Image.query.all()
        images_json = [ImageSchema.dump(image) for image in images]
        if not images_json:
                raise NoResultFound()
        return images_json
    
    def get(self, id=None):
        """
        ImageResource GET method. Retrieves the information related to the image with the passed id in the request
        """
        if id:  
            try:
                self.retrieveImageById(id)
            except NoResultFound:
                abort(404, message=f"Image with id {id} not found in database")
        else:
            try:
                self.retrieveAllImages()
            except NoResultFound:
                abort(404, message="No images available")
    
    def post(self):
        """
        ImageResource POST method. Adds a new image to the database.

        :return: Image, 201 HTTP status code.
        """
        image = ImageSchema().load(request.get_json())

        try:
            db.session.add(image)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this image is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return ImageSchema.dump(image), 201
