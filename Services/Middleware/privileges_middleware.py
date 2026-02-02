"""
Privileges Middleware - Resource ownership verification.

This module provides functions to verify that a user has access to specific resources
by checking ownership chains through the database relationships.
"""

from functools import wraps
from http import HTTPStatus
import logging
from typing import Optional

from flask import abort, g, request
from Api.database import db
from Models.inventory_items import inventory_items
from Models.user import User
from Models.trip import Trip
from Models.itinerary import Itinerary
from Models.day import Day
from Models.sea import Sea
from Models.weather import Weather
from Models.inventory import Inventory
from Models.item import Item
from Models.point import Point
from Models.log import Log
from Models.image import Image

logger = logging.getLogger(__name__)


def require_owner(resource_type, *, id_param='id', from_body=False, parent_resource=None):
    """
    Decorator to ensure user owns the resource or has access to it.
    
    This decorator verifies that the authenticated user has permission to access
    the requested resource by checking the ownership chain in the database.
    
    Args:
        resource_type: Type of resource ('trip', 'itinerary', 'day', 'sea', 'weather', 
                        'inventory', 'item', 'point', 'log', 'image')
        id_param: Name of the parameter containing the resource ID (default: 'id')
        from_body: If True, extract id_param from request body instead of URL (default: False)
        parent_resource: Tuple of (parent_type, parent_id_param) to check parent ownership
                         for create operations. E.g., ('itinerary', 'itinerary_id')
    
    Examples:
        # GET /api/day/<id> - Check day ownership from URL
        @require_owner('day')
        
        # POST /api/day/create with {"itinerary_id": 5} - Check itinerary ownership from body
        @require_owner('day', parent_resource=('itinerary', 'itinerary_id'), from_body=True)
        
        # PUT /api/day/<id>/update with body - Check day ownership from URL
        @require_owner('day', id_param='id')
    """
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # Get current user from g (set by authenticate_restful)
            user_id = g.get('current_user_id')
            if not user_id:
                abort(HTTPStatus.UNAUTHORIZED, description="Authentication required")
            
            # Determine which resource to check
            if parent_resource:
                # For create operations, check parent resource ownership
                parent_type, parent_id_field = parent_resource
                
                if from_body:
                    data = request.get_json()
                    if not data:
                        abort(HTTPStatus.BAD_REQUEST, description="Request body required")
                    resource_id = data.get(parent_id_field)
                else:
                    resource_id = kwargs.get(parent_id_field)
                
                if not resource_id:
                    abort(HTTPStatus.BAD_REQUEST, description=f"{parent_id_field} required")
                
                check_type = parent_type
            else:
                # For read/update/delete operations, check the resource itself
                if from_body:
                    data = request.get_json()
                    if not data:
                        abort(HTTPStatus.BAD_REQUEST, description="Request body required")
                    resource_id = data.get(id_param)
                else:
                    resource_id = kwargs.get(id_param)
                
                if not resource_id:
                    abort(HTTPStatus.BAD_REQUEST, description=f"Resource ID ({id_param}) required")
                
                check_type = resource_type
            
            # Check if user owns or has access to the resource
            has_access = check_resource_ownership(
                user_id=user_id,
                resource_type=check_type,
                resource_id=resource_id
            )
            
            if not has_access:
                abort(HTTPStatus.FORBIDDEN, description=f"Access denied to {check_type} {resource_id}")
            
            return f(*args, **kwargs)
        return decorator_function
    return decorator

def check_resource_ownership(
    user_id: str, resource_type: str, resource_id: int
) -> bool:
    """
    Check if a user has ownership or access rights to a specific resource.

    This function verifies the ownership chain by traversing database relationships
    from the resource back to the user.

    Args:
        user_id: The public_id of the user
        resource_type: Type of resource ('trip', 'itinerary', 'day', 'sea', 'weather', etc.)
        resource_id: The ID of the resource

    Returns:
        True if user has access, False otherwise
    """
    try:
        # Verify user exists
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            logger.warning(f"User {user_id} not found")
            return False

        # Check ownership based on resource type
        if resource_type == "trip":
            return _check_trip_ownership(user.id, resource_id)

        elif resource_type == "itinerary":
            return _check_itinerary_ownership(user.id, resource_id)

        elif resource_type == "day":
            return _check_day_ownership(user.id, resource_id)

        elif resource_type == "sea":
            return _check_sea_ownership(user.id, resource_id)

        elif resource_type == "weather":
            return _check_weather_ownership(user.id, resource_id)

        elif resource_type == "inventory":
            return _check_inventory_ownership(user.id, resource_id)

        elif resource_type == "item":
            return _check_item_ownership(user.id, resource_id)

        elif resource_type == "point":
            return _check_point_ownership(user.id, resource_id)

        elif resource_type == "log":
            return _check_log_ownership(user.id, resource_id)

        elif resource_type == "image":
            return _check_image_ownership(user.id, resource_id)

        else:
            logger.error(f"Unknown resource type: {resource_type}")
            return False

    except Exception as e:
        logger.error(f"Error checking ownership: {e}")
        return False


def _check_trip_ownership(user_id: int, trip_id: int) -> bool:
    """Check if user owns or is a companion on the trip."""
    from Models.user_has_trip import user_has_trip

    # Single query to check if user is associated with trip
    result = (
        db.session.query(Trip)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Trip.id == trip_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_itinerary_ownership(user_id: int, itinerary_id: int) -> bool:
    """Check if user owns the itinerary through trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Itinerary)
        .join(Trip, Itinerary.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Itinerary.id == itinerary_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_day_ownership(user_id: int, day_id: int) -> bool:
    """Check if user owns the day through itinerary/trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Day)
        .join(Itinerary, Day.itinerary_id == Itinerary.id)
        .join(Trip, Itinerary.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Day.id == day_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_sea_ownership(user_id: int, sea_id: int) -> bool:
    """Check if user owns the sea through day/itinerary/trip ownership."""
    # Optimized: Single query with joins instead of multiple queries
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Sea)
        .join(Day, Sea.day_id == Day.id)
        .join(Itinerary, Day.itinerary_id == Itinerary.id)
        .join(Trip, Itinerary.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Sea.day_id == sea_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_weather_ownership(user_id: int, weather_id: int) -> bool:
    """Check if user owns the weather through day/itinerary/trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Weather)
        .join(Day, Weather.day_id == Day.id)
        .join(Itinerary, Day.itinerary_id == Itinerary.id)
        .join(Trip, Itinerary.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Weather.day_id == weather_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_inventory_ownership(user_id: int, inventory_id: int) -> bool:
    """Check if user owns the inventory through trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Inventory)
        .join(Trip, Inventory.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Inventory.id == inventory_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_item_ownership(user_id: int, item_id: int) -> bool:
    """Check if user owns the item through inventory/trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Item)
        .join(inventory_items, Item.id == inventory_items.c.item_id)
        .join(Inventory, inventory_items.c.inventory_id == Inventory.id)
        .join(Trip, Inventory.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(
            Item.id == item_id,
            user_has_trip.c.user_id == user_id | user_id == Item.user_id,
        )
        .first()
    )

    return result is not None


def _check_point_ownership(user_id: int, point_id: int) -> bool:
    """Check if user owns the point through day/itinerary/trip ownership."""
    from Models.user_has_trip import user_has_trip

    result = (
        db.session.query(Point)
        .join(Day, Point.day_id == Day.id)
        .join(Itinerary, Day.itinerary_id == Itinerary.id)
        .join(Trip, Itinerary.trip_id == Trip.id)
        .join(user_has_trip, Trip.id == user_has_trip.c.trip_id)
        .filter(Point.id == point_id, user_has_trip.c.user_id == user_id)
        .first()
    )

    return result is not None


def _check_log_ownership(user_id: int, log_id: int) -> bool:
    """Check if user owns or has access to the log."""
    log = db.session.query(Log).filter_by(id=log_id).first()
    if not log:
        return False

    # Check if user is the log author
    # Assuming there's a user_has_log relationship
    return (
        db.session.query(User)
        .join(User.logs)
        .filter(User.id == user_id, Log.id == log_id)
        .first()
        is not None
    )


def _check_image_ownership(user_id: int, image_id: int) -> bool:
    """Check if user owns the image through point or user ownership."""
    image = db.session.query(Image).filter_by(id=image_id).first()
    if not image:
        return False

    # Check if image belongs to user's point or is user's profile picture
    # This depends on your specific image relationships
    # For now, check if user owns related points
    points_with_image = (
        db.session.query(Point).join(Point.images).filter(Image.id == image_id).all()
    )

    for point in points_with_image:
        if _check_point_ownership(user_id, point.id):
            return True

    return False


