
from Api.database import db
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.sea_state import SeaState

class Sea (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_number','itinerary_id','date'],['day.day_number','day.itinerary_id','day.date'], name="day_foreign_keys_in_sea"),
    )
    day_number   = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer,  primary_key=True)
    date         = db.Column(db.Date,primary_key=True)
    moon_phase   = db.Column(db.String(255))
    high_tide    = db.Column(db.Time)
    low_tide     = db.Column(db.Time)
    sea_states: Mapped[Optional[List[SeaState]]] = db.relationship(backref='sea')
    