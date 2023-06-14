from wtforms import SelectField
from wtforms.validators import InputRequired, ValidationError
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from ismightier_app.models import getBills, getLevels, getSentiments, getSubjects

class LetterOptionsForm(FlaskForm):
    subject = QuerySelectField(query_factory=getSubjects,label='Letter Subject', validators=[InputRequired()], get_label='subject')
    recipient_sentiment = QuerySelectField(query_factory=getSentiments,label='Recipient Sentiment', validators=[InputRequired()], get_label='description')
    government_level = QuerySelectField(query_factory=getLevels,label='Level of Government', validators=[InputRequired()], get_label='government_level')
    chamber = SelectField(label='Legislative Chamber', choices=['Upper','Lower','Any'])
    geography = SelectField(label='Location', choices=[('US','United States'),('AK','Alaska'),('AL','Alabama'),('AR','Arkansas'),('AZ','Arizona'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DC','Washington DC'),('DE','Delaware'),('FL','Florida'),('GA','Georgia'),('GU','Guam'),('HI','Hawaii'),('IA','Iowa'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('MA','Massachusetts'),('MD','Maryland'),('ME','Maine'),('MH','Marshall Islands'),('MI','Michigan'),('MN','Minnesota'),('MO','Missouri'),('MP','Northern Mariana Island'),('MS','Mississippi'),('MT','Montana'),('NC','North Carolina'),('ND','North Dakota'),('NE','Nebraska'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NV','Nevada'),('NY','New York'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('PR','Puerto Rico'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VA','Virginia'),('VI','Virgin Islands'),('VT','Vermont'),('WA','Washington'),('WI','Wisconsin'),('WV','West Virginia'),('WY','Wyoming')])
    bill_referenced = QuerySelectField(query_factory=getBills,label='Referenced Legislation', get_label='bill_referenced')



