from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.main.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()