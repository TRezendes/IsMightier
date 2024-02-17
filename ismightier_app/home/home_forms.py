from wtforms import BooleanField, DecimalField, HiddenField, IntegerField, RadioField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, ValidationError
from flask_wtf import FlaskForm

class RepLookupForm(FlaskForm):
    address = StringField(label='Enter Your Address', validators=[InputRequired(message="You must enter an address to find local representatives.")])
    submit = SubmitField(label='Find Your Representatives')

class RepLookupGeo(FlaskForm):
    geolocate = SubmitField(label='Search Using your Current Location')
    address = StringField()
