from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

class RepLookupForm(FlaskForm):
    address = StringField(label='Enter Your Address', validators=[InputRequired(message="You must enter an address to find local representatives.")])
    submit = SubmitField(label='Find Your Representatives')

