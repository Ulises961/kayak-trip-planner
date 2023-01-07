from app import db
import enum

class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'


class Point (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    gps = db.Column(db.Numeric)
    notes = db.Column(db.Text)
    type = enum.Enum(PointType)
