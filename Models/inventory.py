import uuid_extension

from Api.database import db
from Models.base_model import BaseModel
from Models.inventory_items import inventory_items
from sqlalchemy import UUID, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID as _UUID

if TYPE_CHECKING:
    from Models.item import Item

class Inventory(BaseModel):
    def __init__(self,items=[],**kwargs):
        self.items = items
        self.__dict__.update(kwargs)

    trip_id: Mapped[Optional[_UUID]] = mapped_column(UUID, ForeignKey('trip.id'), nullable=True)
    user_id:Mapped[_UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable= False)
    items: Mapped[List["Item"]] = relationship(secondary=inventory_items, cascade='all,delete')

    def __repr__(self):
        return f'<Inventory "{self.id}">'
