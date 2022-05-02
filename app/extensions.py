from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models import User
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

# TODO: Add authentication setup code here!

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)