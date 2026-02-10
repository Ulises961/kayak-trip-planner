"""
Point Service - Business logic for point operations.
"""
import logging
from sqlite3 import IntegrityError
from typing import List, Optional, cast
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from Models.day import Day
from Models.itinerary import Itinerary
from Models.point import Point
from Schemas.point_schema import PointSchema
from Api.database import db

logger = logging.getLogger(__name__)


class PointService:
    """Service class for Point-related business logic."""
    
    @staticmethod
    def get_point_by_id(point_id: int) -> Optional[Point]:
        """
        Retrieve a point by its ID.
        
        Args:
            point_id: The ID of the point to retrieve
            
        Returns:
            Point object if found, None otherwise
            
        Raises:
            NoResultFound: If point doesn't exist
        """

        point = db.session.query(Point).filter_by(id=point_id).first()
        if not point:
            logger.warning(f"Point with id {point_id} not found")
            raise NoResultFound(f"Point {point_id} not found in database")
        return point
    
    @staticmethod
    def get_all_points(itinerary_id:int) -> List[Point]:
        """
        Retrieve all points from the database.
        
        Params:
            itinerary_id(int) the id of the itinerary containing the points

        Returns:
            List of all Point objects
            
        Raises:
            NoResultFound: If no points exist
        """
        itinerary = db.session.query(Itinerary)\
            .options(selectinload(Itinerary.days).selectinload(Day.points))\
            .filter_by(id=itinerary_id)\
            .first()
        
        if not itinerary:
            raise NoResultFound(f"Itinerary {itinerary_id} not found in database")
        
        points = [point for day in itinerary.days if day.points is not None for point in day.points]

        if not points:
            logger.warning("No points found in database")
            raise NoResultFound("No points found in database")
        return points
    
    @staticmethod
    def create_point(point_data: dict) -> Point:
        """
        Create a new point.
        
        Args:
            point_data: Dictionary containing point information
            
        Returns:
            Created Point object
            
        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info(f"Creating new point")
        point: Point = cast(Point,PointSchema().load(point_data))
        db.session.add(point)
        db.session.commit()
        
        # Refresh to get relationships
        db.session.refresh(point)
        logger.info(f"Point {point.id} created successfully")
        return point
    
    @staticmethod
    def update_point(point_id: int, point_data: dict) -> Point:
        """
        Update an existing point.
        
        Args:
            id: Integer ID of the updated point
            point_data: Dictionary containing point information with ID
            
        Returns:
            Updated Point object
            
        Raises:
            ValidationError: If data is invalid
            NoResultFound: If point doesn't exist
        """
        point_data.setdefault("id", point_id)
        point: Point = PointSchema().load(point_data)  # type: ignore
        
        # Verify point exists
        existing_point = PointService.get_point_by_id(point.id)
        if not existing_point:
            raise NoResultFound(f"Point {point.id} not found")
        
        logger.info(f"Updating point {point.id}")
        db.session.merge(point)
        db.session.commit()
        db.session.refresh(existing_point)      
  
        return point
    
    @staticmethod
    def delete_point(point_id: int) -> None:
        """
        Delete a point by its ID.
        
        Args:
            point_id: The ID of the point to delete
            
        Raises:
            NoResultFound: If point doesn't exist
        """
        point = PointService.get_point_by_id(point_id)
        logger.info(f"Deleting point {point_id}")
        db.session.delete(point)
        db.session.commit()
        logger.info(f"Point {point_id} deleted successfully")
    
    @staticmethod
    def get_points_by_day(day_id: int) -> List[Point]:
        """
        Retrieve all points for a specific day.
        
        Args:
            day_id: The ID of the day
            
        Returns:
            List of Point objects for that day
        """
        points = db.session.query(Point).filter_by(day_id=day_id).all()
        logger.info(f"Found {len(points)} points for day {day_id}")
        return points

    @staticmethod
    def get_points_in_range(range:float,long: float, lat:float)-> List[Point]:
        return []