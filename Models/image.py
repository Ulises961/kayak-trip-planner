from app import db

class Image (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    size = db.Column(db.Numeric)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'))

    def __repr__(self):
        return f'<Image "{self.name, self.location, self.size}">'
