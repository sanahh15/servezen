from flask import Blueprint, flash, render_template, request, jsonify,redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db
from werkzeug.security import check_password_hash
auth_bp = Blueprint('auth', __name__,)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('auth.register'))
        
        user = User(name=name, email=email, role="user")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
      
      #role-based redirection
            if user.role == "admin":
                return redirect('/admin-dashboard')
            else:
                return redirect('/')    
            
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home.home'))

