from flask import Blueprint, flash, render_template, request, jsonify,redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db
from werkzeug.security import check_password_hash
auth_bp = Blueprint('auth', __name__,)

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


# 🔹 LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home.home'))