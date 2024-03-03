from ismightier_app import db
from sqlalchemy.dialects import postgresql
from sqlalchemy import PrimaryKeyConstraint, text

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

# Query Factory for form QuerySelect field
def getSubjects():
    subjects = db.session.execute(db.select(LetterPartTbl).distinct(LetterPartTbl.subject)).scalars()
    return subjects

def getLevels():
    levels = db.session.execute(db.select(LetterPartTbl.government_level).all())
    return levels

def getBills():
    bills = db.session.execute(db.select(LetterPartTbl).distinct(LetterPartTbl.bill_referenced)).scalars()
    return bills


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

# class SentimentLevelTbl(db.Model):
#     __tablename__ = 'sentiment_level'
#     __table_args__ = {
#         'autoload_with': db.engine
#     }
class SentimentLevelTbl(db.Model):
    __table__ = db.metadata.tables['sentiment_level']

# def getSentiments():
#     sentiments = db.session.execute(db.select(SentimentLevelTbl)).scalars().all()
#     return sentiments

def getSentiments():
    sentiments = db.session.execute(db.select(SentimentLevelTbl)).scalars().all()
    sentiment_list = []
    for row in sentiments:
        tup = (row.level, row.description)
        sentiment_list.append(tup)
    return sentiment_list

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
