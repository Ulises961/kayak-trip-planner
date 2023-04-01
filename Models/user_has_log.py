from database import db

class UserHasLog (db.Model):
    log_id   = db.Column(db.Integer, db.ForeignKey('log.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
