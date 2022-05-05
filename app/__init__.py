from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.models import User
from app.extensions import app

from app.main.routes import main

app.register_blueprint(main)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)