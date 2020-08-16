from app import db


class Cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), index=True, unique=True)
    cases = db.Column(db.Integer)
    tests = db.Column(db.Integer)
    positive = db.Column(db.Float)

