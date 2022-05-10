from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.models import User

import os

app = Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)