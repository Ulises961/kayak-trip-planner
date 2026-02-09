import uuid
from Api.database import db
from flask_bcrypt import generate_password_hash
from Models.inventory import Inventory
from Models.item import Item
from Models.itinerary import Itinerary
from Models.user_has_itinerary import user_has_itinerary
from Models.user_has_inventory import user_has_inventory
from Models.user_has_items import user_has_items
from Models.user_has_invitation import user_has_invitation
from Models.user_has_trip import user_has_trip
from Models.user_endorses_log import user_endorses_log
from Models.user_has_profile_picture import userHasProfilePicture
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.log import Log
    from Models.image import Image
    from Models.trip import Trip


class User(db.Model):
    __tablename__ = "users"

    def __init__(self, pwd=None, endorsed_logs=[], logs=[], public_id=None, **kwargs):
        if pwd:
            self.pwd = generate_password_hash(pwd).decode("UTF-8")

        self.endorsed_logs = endorsed_logs
        self.logs = logs

        self.__dict__.update(kwargs)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[Optional[str]] = mapped_column(
        String(255), unique=True, nullable=True, default=lambda: str(uuid.uuid4())
    )
    mail: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    pwd: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    trips: Mapped[List["Trip"]] = relationship(
        secondary=user_has_trip, back_populates="travellers"
    )
    invitations: Mapped[List["Trip"]] = relationship(
        secondary=user_has_invitation, back_populates="pending_travellers"
    )
    endorsed_logs: Mapped[List["Log"]] = relationship(
        secondary=user_endorses_log, back_populates="user_endorsed_logs"
    )
    logs: Mapped[List["Log"]] = relationship(back_populates="user_logs")
    image: Mapped[Optional["Image"]] = relationship(
        secondary=userHasProfilePicture,
        uselist=False,
        cascade="all, delete,save-update",
    )
    itineraries: Mapped[List["Itinerary"]] = relationship(secondary=user_has_itinerary)
    inventories: Mapped[List["Inventory"]] = relationship(secondary=user_has_inventory)
    items: Mapped[List["Item"]] = relationship(secondary=user_has_items)

    def __repr__(self):
        return (
            f'<User "{self.id} {self.mail}, {self.name}, {self.surname}, {self.pwd}">'
        )
