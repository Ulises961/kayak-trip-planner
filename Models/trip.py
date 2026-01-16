from Api.database import db
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.itinerary import Itinerary
    from Models.inventory import Inventory
    from Models.user import User


class Trip (db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    inventory: Mapped[Optional["Inventory"]] = relationship(foreign_keys="Inventory.trip_id", uselist=False, cascade='all, delete,save-update')
    itinerary: Mapped[Optional["Itinerary"]] = relationship(foreign_keys="Itinerary.trip_id", uselist=False, cascade='all, delete,save-update')
    travellers: Mapped[List["User"]] = relationship(secondary='user_has_trip', back_populates='trips')
