from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.booking import Booking
from app.models.user import User
from app.models.service import Service
from app.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# 🔒 Admin Dashboard
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != "admin":
        return redirect(url_for('home.dashboard'))

    bookings = Booking.query.order_by(Booking.id.desc()).all()
    users = User.query.all()
    services = Service.query.all()

    return render_template(
        'admin/dashboard.html',
        bookings=bookings,
        users=users,
        services=services
    )

# 🔄 Update Booking Status
@admin_bp.route('/update/<int:id>/<status>')
@login_required
def update_status(id, status):
    if current_user.role != "admin":
        return redirect(url_for('home.dashboard'))

    booking = Booking.query.get(id)

    if booking:
        booking.status = status
        db.session.commit()

    return redirect(url_for('admin.dashboard'))