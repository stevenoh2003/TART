from backend import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    location_x = db.Column(db.Integer)  # X-coordinate of the location in the mall
    location_y = db.Column(db.Integer)  # Y-coordinate of the location in the mall
    price = db.Column(db.Float)
    expiration_date = db.Column(db.DateTime)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': (self.location_x, self.location_y),
            'price': self.price,
            'expiration_date': self.expiration_date.strftime('%Y-%m-%d') if self.expiration_date else None
        }