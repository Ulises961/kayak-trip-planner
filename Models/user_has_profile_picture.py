from database import db

userHasProfilePicture = db.Table('user_has_profile_picture',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('image_id ',db.Integer, db.ForeignKey('image.id'))
    )

