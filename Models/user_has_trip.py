from database import db

user_has_trip = db.Table('user_has_trip', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'))
    )
   