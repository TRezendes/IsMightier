from wtforms import BooleanField, DecimalField, HiddenField, IntegerField, RadioField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, ValidationError
from flask_wtf import FlaskForm

class RepLookupForm(FlaskForm):
    address = StringField(label='Your Address', validators=[DataRequired()])
    submit = SubmitField(label='Find Your Representatives')
