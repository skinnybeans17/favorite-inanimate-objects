from flask import Flask
from flask_login import LoginManager
from app.models import User
from flask_bcrypt import Bcrypt
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'main.homepage'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)