from typing import Optional, Dict, Any, List
from Models.day import Day
from Models.sea import Sea
from Models.weather import Weather
from Api.database import db
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound, IntegrityError
from datetime import date, time
import logging

logger = logging.getLogger(__name__)


class DayService:
    @staticmethod
    def get_day_by_id(day_id: int) -> Day:
        """
        Retrieve a day description with the different sea and weather states during that day.

        Params:
            day_id(int) id of the day entity
        Returns:
            The day with its sea and weather data

        Raises:
            NoResultFound: If no day exists
        """
        day = (
            db.session.query(Day)
            .options(
                selectinload(Day.sea),
                selectinload(Sea.sea_states),
                selectinload(Day.weather),
                selectinload(Weather.weather_states)
            )
            .filter_by(id=day_id)
            .first()
        )

        if not day:
            raise NoResultFound(f"Day with id {day_id} not found")

        return day

    @staticmethod
    def get_by_itinerary(itinerary_id: int) -> List[Day]:
        """
        Retrieve all days for a specific itinerary.

        Params:
            itinerary_id(int) id of the itinerary
        Returns:
            List of days belonging to the itinerary
        """
        days = db.session.query(Day).filter_by(itinerary_id=itinerary_id).all()
        return days

    @staticmethod
    def get_by_ids(day_ids: List[int]) -> List[Day]:
        """
        Retrieve days by their IDs.

        Params:
            day_ids: List of day IDs
        Returns:
            List of days
        """
        days = db.session.query(Day).filter(Day.id.in_(day_ids)).all()
        return days

    @staticmethod
    def get_by_key(day_number: int, day_date: date, itinerary_id: int) -> Optional[Day]:
        """
        Retrieve a day by its composite key.

        Params:
            day_number: The day number
            day_date: The date of the day
            itinerary_id: The itinerary ID
        Returns:
            The day if found, None otherwise
        """
        day = db.session.query(Day).filter_by(
            day_number=day_number,
            date=day_date,
            itinerary_id=itinerary_id
        ).first()
        return day

    @staticmethod
    def create_day(day: Day) -> Day:
        """
        Create a new day.

        Params:
            day: Day object to create
        Returns:
            Created day object
        """
        db.session.add(day)
        db.session.commit()
        db.session.refresh(day)
        return day

    @staticmethod
    def update_day(day_id: int, day_data: Dict[str, Any]) -> Day:
        """
        Update an existing day with new data, including weather and sea information.

        Params:
            day_id: ID of the day to update
            day_data: Dictionary containing update data
        Returns:
            Updated day object
        Raises:
            NoResultFound: If day doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Get the existing day
        existing_day = db.session.get(Day, day_id)
        
        if not existing_day:
            raise NoResultFound(f"Day with id {day_id} not found")
        
        # Check if nested objects are present in the request (even if None)
        has_weather_key = 'weather' in day_data
        has_sea_key = 'sea' in day_data
        
        # Extract nested objects
        weather_data = day_data.pop('weather', None) if has_weather_key else None
        sea_data = day_data.pop('sea', None) if has_sea_key else None
        
        # Update simple fields directly from day_data (skip id)
        for key, value in day_data.items():
            if key == 'id':
                continue
            if hasattr(existing_day, key):
                # Convert date string to date object if needed
                if key == 'date' and isinstance(value, str):
                    value = date.fromisoformat(value)
                setattr(existing_day, key, value)
        
        # Handle weather update/creation
        if has_weather_key:
            DayService._update_weather(existing_day, weather_data)
        
        # Handle sea update/creation
        if has_sea_key:
            DayService._update_sea(existing_day, sea_data)
        
        db.session.commit()
        db.session.refresh(existing_day)
        
        return existing_day

    @staticmethod
    def _update_weather(day: Day, weather_data: Optional[Dict[str, Any]]) -> None:
        """
        Update or create weather data for a day.

        Params:
            day: The day to update
            weather_data: Weather data dictionary or None to remove
        """
        if weather_data:  # Non-null weather data
            if day.weather:
                # Update existing weather
                for key, value in weather_data.items():
                    if key == 'day_id':
                        continue
                    if hasattr(day.weather, key):
                        setattr(day.weather, key, value)
            else:
                # Create new weather
                weather = Weather(**weather_data)
                day.weather = weather
        else:  # Null weather data - remove association
            if day.weather:
                db.session.delete(day.weather)
                day.weather = None

    @staticmethod
    def _update_sea(day: Day, sea_data: Optional[Dict[str, Any]]) -> None:
        """
        Update or create sea data for a day.

        Params:
            day: The day to update
            sea_data: Sea data dictionary or None to remove
        """
        if sea_data:  # Non-null sea data
            if day.sea:
                # Update existing sea
                for key, value in sea_data.items():
                    if key == 'day_id':
                        continue
                    if hasattr(day.sea, key):
                        # Convert time string to time object if needed
                        if key in ('high_tide', 'low_tide') and isinstance(value, str):
                            value = time.fromisoformat(value)
                        setattr(day.sea, key, value)
            else:
                # Create new sea
                # Convert time strings if present
                if 'high_tide' in sea_data and isinstance(sea_data['high_tide'], str):
                    sea_data['high_tide'] = time.fromisoformat(sea_data['high_tide'])
                if 'low_tide' in sea_data and isinstance(sea_data['low_tide'], str):
                    sea_data['low_tide'] = time.fromisoformat(sea_data['low_tide'])
                sea = Sea(**sea_data)
                day.sea = sea
        else:  # Null sea data - remove association
            if day.sea:
                db.session.delete(day.sea)
                day.sea = None

    @staticmethod
    def delete_day(day_id: int) -> None:
        """
        Delete a day by its ID.

        Params:
            day_id: ID of the day to delete
        Raises:
            NoResultFound: If day doesn't exist
            IntegrityError: If deletion violates database constraints
        """
        day_to_delete = db.session.get(Day, day_id)
        
        if not day_to_delete:
            raise NoResultFound(f"Day with id {day_id} not found")
        
        db.session.delete(day_to_delete)
        db.session.commit()
        logger.info(f"Day with id {day_id} successfully deleted")
    