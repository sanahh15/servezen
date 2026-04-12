from flask import Flask
from .extensions import db, login_manager
from .routes.auth import auth_bp
from .routes.home import home_bp
from .routes.booking import booking_bp
from .routes.admin import admin_bp
from config import Config

# Import all models so SQLAlchemy can resolve relationship targets.
from . import models

def create_app():
    app = Flask(__name__)

    # ✅ load config
    app.config.from_object(Config)
    
 

    db.init_app(app)
    login_manager.init_app(app)

    # ✅ register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)

    return app