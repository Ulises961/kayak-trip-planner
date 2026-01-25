from typing import Optional
from Models.day import Day
from Models.sea import Sea
from Api.database import db
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound

from Models.weather import Weather


class DayService:
    @staticmethod
    def get_day_by_id(day_id: int) -> Day:
        """
        Retrieve a day description with the different sea and weather states during that day.

        Params:
            day_id(int) id of the sea entity
        Returns:
            The sea and its states

        Raises:
            NoResultFound: If no sea exists
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
            raise NoResultFound(f"Sea with id {day_id} not found")

        return day

    @staticmethod
    def update_weather_and_sea(day: Day):
        pass
