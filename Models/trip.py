import uuid
from Api.database import db
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.itinerary import Itinerary
    from Models.inventory import Inventory
    from Models.user import User


class Trip (db.Model):
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    inventory: Mapped[Optional["Inventory"]] = relationship(foreign_keys="Inventory.trip_id", uselist=False, cascade='all, delete,save-update')
    itinerary: Mapped[Optional["Itinerary"]] = relationship(foreign_keys="Itinerary.trip_id", uselist=False, cascade='all, delete,save-update')
    travellers: Mapped[List["User"]] = relationship(secondary='user_has_trip', back_populates='trips')
    pending_travellers: Mapped[List["User"]] = relationship(secondary='user_has_invitation', back_populates='invitations')
    is_draft: Mapped[bool] = mapped_column(Boolean, default=True)