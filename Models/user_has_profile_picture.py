from app import db

class UserHasProfilePicture (db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True )
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

