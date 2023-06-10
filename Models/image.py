from Api.database import db

class Image (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    size = db.Column(db.Numeric)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))

    def __repr__(self):
        return f'<Image "name {self.name}, path {self.location}, size {self.size}">'
