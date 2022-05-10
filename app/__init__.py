from flask_login import LoginManager
from app.extensions import app
from app.models import User
from flask_bcrypt import Bcrypt
from app.main.routes import main
from app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

login_manager = LoginManager(app)
login_manager.login_view = 'main.homepage'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)