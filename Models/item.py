from Api.database import db
from sqlalchemy import ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.inventory import Inventory

import enum


class ItemCategoryType(enum.Enum):
    FIRST_AID = "first_aid"
    CAMPING = "camping"
    REPAIR = "repair"
    TRAVEL = "travel"
    GENERIC = "generic"
    FOOD = "food"

class Item(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[Optional[ItemCategoryType]] = mapped_column(
        Enum(ItemCategoryType), nullable=True
    )
    checked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'),nullable=False)
