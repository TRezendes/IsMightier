from ismightier_app import db

db.reflect()

class USCongressTbl(db.Model):
    __tablename__ = 'us_congress'
    __table_args__ = {
        'autoload_with': db.engine
    }
