from flask import Blueprint, render_template
from app.models.service import Service
home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
        services = Service.query.all()
        return render_template('home.html', services=services)

