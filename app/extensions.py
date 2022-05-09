from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)