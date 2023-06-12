from ismightier_app import db
from sqlalchemy.dialects import postgresql
from sqlalchemy import PrimaryKeyConstraint

db.reflect()

class USCongressTbl(db.Model):
    __tablename__ = 'us_congress'
    __table_args__ = {
        'autoload_with': db.engine
    }
    
class LetterPartTbl(db.Model):
    __tablename__ = 'letter_part'
    __table_args__ = {
        'autoload_with': db.engine
    }

class RepresentativeSentimentTbl(db.Model):
    __tablename__ = 'representative_sentiment'
    #__table_args__ = (
        #db.PrimaryKeyConstraint(
        #    'full_name',
        #    'state',
        #    'subject'
        #),
    __table_args__ = {
            'autoload':True,
            'autoload_with': db.engine
        }
    #)
    
class SentimentLevelTbl(db.Model):
    __tablename__ = 'letter_part'
    __table_args__ = {
        'autoload_with': db.engine
    }
    
class FederalSponsorTbl(db.Model):
    __tablename__ = 'federal_sponsor'
    #__table_args__ = (
    #    db.PrimaryKeyConstraint(
    #        'bill',
    #        'sponsor_bioguide_id'
    #    ),
    __table_args__ = {
            'autoload':True,
            'autoload_with': db.engine
        }
    #)

class StateSponsorTbl(db.Model):
    __tablename__ = 'state_sponsor'
    #__table_args__ = (
        #db.PrimaryKeyConstraint(
        #    'state',
        #    'bill',
        #    'sponsor_name'
        #),
    __table_args__ = {
            'autoload':True,
            'autoload_with': db.engine
        }
    #)


# USCongressTbl,LetterPartTbl,RepresentativeSentimentTbl,SentimentLevelTbl,FederalSponsorTbl,StateSponsorTbl
