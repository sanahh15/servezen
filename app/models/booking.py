from app.extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Booked")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))


    
    # ✅ ADD THESE
    user = db.relationship('User')
    service = db.relationship('Service')