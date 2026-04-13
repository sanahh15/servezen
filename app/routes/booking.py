from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.booking import Booking
from app.extensions import db

booking_bp = Blueprint('booking', __name__)

from app.models.service import Service

@booking_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        date = request.form.get('date')

        new_booking = Booking(
            service_id=service_id,
            date=date,
            user_id=current_user.id
        )

        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('home.dashboard'))

    services = Service.query.all()

    return render_template('booking/book.html', services=services)

#view user bookings
@booking_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('booking/my_bookings.html', bookings=bookings)


@booking_bp.route('/cancel/<int:id>')
@login_required
def cancel(id):
    booking = Booking.query.get(id)

    if booking and booking.user_id == current_user.id:
        booking.status = "Cancelled"
        db.session.commit()

    return redirect(url_for('home.dashboard'))