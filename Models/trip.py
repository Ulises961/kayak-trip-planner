from Api.database import db
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.itinerary import Itinerary
from Models.inventory import Inventory
 
class Trip (db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    inventory: Mapped[Optional[Inventory]] = db.relationship( backref="trip_inventory", uselist=False)
    itinerary:  Mapped[Optional[Itinerary]] = db.relationship( backref="trip_itinerary", uselist=False)
    
