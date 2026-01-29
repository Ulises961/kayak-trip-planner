"""
Image Service - Business logic for image operations.
"""
import logging
from typing import List, Optional, cast
from sqlalchemy.exc import NoResultFound, IntegrityError

from Models.image import Image
from Models.point import Point
from Schemas.image_schema import ImageSchema
from Api.database import db

logger = logging.getLogger(__name__)


class ImageService:
    """Service class for Image-related business logic."""

    @staticmethod
    def get_image_by_id(image_id: int) -> Image:
        """
        Retrieve an image by its ID.

        Args:
            image_id: The ID of the image to retrieve

        Returns:
            Image object if found

        Raises:
            NoResultFound: If image doesn't exist
        """
        image = db.session.get(Image, image_id)
        if not image:
            logger.warning(f"Image with id {image_id} not found")
            raise NoResultFound(f"Image {image_id} not found in database")
        return image

    @staticmethod
    def get_images_by_point(point_id: int) -> List[Image]:
        """
        Retrieve all images for a specific point.

        Args:
            point_id: The ID of the point

        Returns:
            List of Image objects
        """
        from Models.point_has_image import PointHasImage

        images = (
            db.session.query(Image)
            .join(PointHasImage, Image.id == PointHasImage.c.image_id)
            .filter(PointHasImage.c.point_id == point_id)
            .all()
        )
        logger.info(f"Found {len(images)} images for point {point_id}")
        return images

    @staticmethod
    def create_image(image_data: dict) -> Image:
        """
        Create a new image.

        Args:
            image_data: Dictionary containing image information

        Returns:
            Created Image object

        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info("Creating new image")
        image = cast(Image, ImageSchema().load(image_data))
        db.session.add(image)
        db.session.commit()

        db.session.refresh(image)
        logger.info(f"Image {image.id} created successfully")
        return image

    @staticmethod
    def update_image(image_id: int, image_data: dict) -> Image:
        """
        Update an existing image.

        Args:
            image_id: The ID of the image to update
            image_data: Dictionary containing image information

        Returns:
            Updated Image object

        Raises:
            ValidationError: If data is invalid
            NoResultFound: If image doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Verify image exists
        existing_image = ImageService.get_image_by_id(image_id)
        if not existing_image:
            raise NoResultFound(f"Image with id {image_id} not found")
        logger.info(f"Updating image {image_id}")

        updated_image = ImageSchema().load(image_data)

        try:
            merged_image = cast(Image, db.session.merge(updated_image))
            db.session.commit()
            db.session.refresh(merged_image)

            logger.info(f"Image {image_id} updated successfully")
            return merged_image

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error updating image {image_id}: {e}")
            raise

    @staticmethod
    def delete_image(image_id: int) -> None:
        """
        Delete an image by its ID.

        Args:
            image_id: The ID of the image to delete

        Raises:
            NoResultFound: If image doesn't exist
            IntegrityError: If image has references that prevent deletion
        """
        image = ImageService.get_image_by_id(image_id)

        try:
            logger.info(f"Deleting image {image_id}")
            db.session.delete(image)
            db.session.commit()
            logger.info(f"Image {image_id} deleted successfully")

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting image {image_id}: {e}")
            raise IntegrityError(
                f"Cannot delete image {image_id} due to existing references",
                params=None,
                orig=e
            )

    @staticmethod
    def attach_image_to_point(image_id: int, point_id: int) -> None:
        """
        Attach an image to a point.

        Args:
            image_id: The ID of the image
            point_id: The ID of the point

        Raises:
            NoResultFound: If image or point doesn't exist
        """

        image = ImageService.get_image_by_id(image_id)
        point = db.session.get(Point, point_id)

        if not point:
            raise NoResultFound(f"Point {point_id} not found")

        if image not in point.images:
            point.images.append(image)
            db.session.commit()
            logger.info(f"Image {image_id} attached to point {point_id}")
        else:
            logger.info(f"Image {image_id} already attached to point {point_id}")

    @staticmethod
    def detach_image_from_point(image_id: int, point_id: int) -> None:
        """
        Detach an image from a point.

        Args:
            image_id: The ID of the image
            point_id: The ID of the point

        Raises:
            NoResultFound: If image or point doesn't exist
        """

        image = ImageService.get_image_by_id(image_id)
        point = db.session.get(Point, point_id)

        if not point:
            raise NoResultFound(f"Point {point_id} not found")

        if image in point.images:
            point.images.remove(image)
            db.session.commit()
            logger.info(f"Image {image_id} detached from point {point_id}")
        else:
            logger.info(f"Image {image_id} not attached to point {point_id}")
