from app import db

class Log(db.Model):

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    hours = db.Column(db.Numeric)
    avg_sea = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Log "{self.id}, User {self.user_id}">'
