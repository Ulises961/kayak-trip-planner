import logging
from flask_restful import Resource
from flask import request
from Schemas.point_schema import PointSchema
from Services.point_service import PointService


logger = logging.getLogger(__name__)

POINT_ENDPOINT = "/api/point"

class PointResource(Resource):
    """RESTful resource for Point operations."""
    
    def get(self, id=None):
        """
        PointResource GET method. Retrieves point(s) by ID or all points.
        
        Args:
            id: Optional point ID
            
        Returns:
            JSON response with point data and 200 status code
        """
        if id:
            point = PointService.get_point_by_id(id)
            return PointSchema().dump(point), 200
        else:
            logger.info("Retrieve all points from db")
            points = PointService.get_all_points()
            return [PointSchema().dump(point) for point in points], 200

    
    def post(self):
        """
        PointResource POST method. Adds a new point to the database.

        Returns:
            JSON response with created point and 201 status code
        """
        point_data = request.get_json()
        point = PointService.create_point(point_data)
        return PointSchema().dump(point), 201
        
    def put(self):
        """
        PointResource PUT method. Updates an existing point.
        
        Returns:
            JSON response with updated point and 200 status code
        """
        point_data = request.get_json()
        point = PointService.update_point(point_data)
        return PointSchema().dump(point), 200

    def delete(self, id):
        """
        PointResource DELETE method. Deletes a point by ID.
        
        Args:
            id: Point ID to delete
            
        Returns:
            Success message and 200 status code
        """
        logger.info(f"Deleting point {id}")
        PointService.delete_point(id)
        return {"message": "Deletion successful"}, 200

        
