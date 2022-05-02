# Create your forms here.
import imp
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from app.models import Collection, Object, User
from app import bcrypt

class CollectionForm(FlaskForm):
    title = StringField('Name of Collection', validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Add this New Collection')

class ObjectForm(FlaskForm):
    name = StringField('Name of Object', validators=[DataRequired(), Length(min=3, max=80)])
    category = StringField('Category of Object', validators=[DataRequired()])
    collection = QuerySelectField('Collection', query_factory=lambda: Collection.query, allow_blank=False)
    image_url = StringField('Object Image URL')
    submit = SubmitField('Add this New Object')

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password does not match. Please try again.')