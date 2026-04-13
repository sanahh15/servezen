from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models.booking import Booking
from app.models.service import Service
from app.models.user import User
home_bp = Blueprint('home', __name__ )


@home_bp.route('/')
def home():
        services = [
        (1, "Doctor Consultation", "Online doctor appointment", 500),
        (2, "Lab Test", "Blood test at home", 300),
        (3, "Medicine Delivery", "Doorstep medicines", 200)
    ]
        return render_template('home.html', services=services)


@home_bp.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(Booking.id.desc()).all()

    services = Service.query.all()

    upcoming = Booking.query.filter_by(
        user_id=current_user.id,
        status="Booked"
    ).order_by(Booking.id.desc()).first()

    return render_template(
        'home/dashboard.html',
        bookings=bookings,
        services=services,
        upcoming=upcoming
    )

@home_bp.route('/add-services')
def add_services():
    from app.models.service import Service
    from app.extensions import db

    s1 = Service(name="Doctor Consultation", price=500)
    s2 = Service(name="Lab Test", price=300)
    s3 = Service(name="Medicine Delivery", price=200)

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    return "Services Added Successfully!"

@home_bp.route('/make-admin')
def make_admin():
    from app.models.user import User
    from app.extensions import db

    user = User.query.filter_by(email='sahanar20657@gmail.com').first()

    if not user:
        return "User not found ❌"

    user.role = "admin"
    db.session.commit()

    return f"{user.email} is now ADMIN ✅"