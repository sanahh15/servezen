from flask import Flask
from flask_mail import Mail
from .extensions import db, login_manager ,mail
from .routes.auth import auth_bp
from .routes.home import home_bp
from .routes.booking import booking_bp
from .routes.admin import admin_bp

# ✅ CREATE MAIL OBJECT HERE (GLOBAL)
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    # Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'sahanar2065@gmail.com'
    app.config['MAIL_PASSWORD'] = 'qvqbafkwlqmcmjgb'

    # ✅ INIT MAIL HERE
    mail.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)

    return app