from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from app.models import Collection

class CollectionForm(FlaskForm):
    title = StringField('Name of Collection', validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Add this New Collection')

class ObjectForm(FlaskForm):
    name = StringField('Name of Object', validators=[DataRequired(), Length(min=3, max=80)])
    category = StringField('Category of Object', validators=[DataRequired()])
    collection = QuerySelectField('Collection', query_factory=lambda: Collection.query, allow_blank=False)
    image_url = StringField('Object Image URL')
    submit = SubmitField('Add this New Object')