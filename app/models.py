# Create your models here.
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    objects = db.relationship('Object', back_populates='collection')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    image_url = db.Column(URLType)
    collection_id = db.Column(
        db.Integer, db.ForeignKey('collection.id'), nullable=False)
    collection = db.relationship('Collection', back_populates='objects')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users_favorites = db.relationship('User', secondary='user_favorites')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    favorite_objects = db.relationship('Object', secondary='user_favorites')

favorites_table = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('object_id', db.Integer, db.ForeignKey('object.id'))
)