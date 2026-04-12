from app.extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price =  db.Column(db.Integer)

    bookings = db.relationship('Booking', backref='service', lazy=True) 