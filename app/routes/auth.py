from flask import Blueprint, flash, render_template, request, jsonify,redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db
from werkzeug.security import check_password_hash
auth_bp = Blueprint('auth', __name__,)
import random
from datetime import datetime, timedelta
from app.extensions import mail  


def generate_otp():
    return str(random.randint(100000, 999999))
# 🔹 REGISTER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation
        if not name or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long", "danger")
            return redirect(url_for('auth.register'))

        if "@" not in email:
            flash("Invalid email format", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "warning")
            return redirect(url_for('auth.register'))

        # Create user
        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


# 🔹 LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=True)

            # Role-based redirect
            if user.role == "admin":
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            otp = generate_otp()
            user.otp = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()

            from flask_mail import Message
            msg = Message(
    "OTP for Password Reset",
    sender="sahanar2065@gmail.com",   # ✅ ADD THIS LINE
    recipients=[email]
)
            msg.body = f"Your OTP is {otp}"

            mail.send(msg)

            return redirect(url_for('auth.verify_otp', email=email))

        flash("Email not found", "danger")

    return render_template('auth/forgot.html')


@auth_bp.route('/verify-otp/<email>', methods=['GET', 'POST'])
def verify_otp(email):
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        entered_otp = request.form.get('otp')

        if user and user.otp == entered_otp:
            if datetime.utcnow() > user.otp_expiry:
                flash("OTP expired", "danger")
            else:
                return redirect(url_for('auth.reset_password', email=email))
        else:
            flash("Invalid OTP", "danger")

    return render_template('auth/verify_otp.html')


@auth_bp.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        password = request.form.get('password')

        user.set_password(password)
        user.otp = None
        user.otp_expiry = None

        db.session.commit()

        flash("Password updated successfully", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')

# 🔹 LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home.home'))