from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail 

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail() 


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User   # ✅ import inside function
    return User.query.get(int(user_id))