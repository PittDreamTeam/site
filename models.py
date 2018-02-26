from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Spots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    remaining = db.Column(db.Integer, nullable = False)

    def __init__(self, remaining):
        self.remaining = remaining

class Count(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    somenumber = db.Column(db.Integer, nullable = False)

    def __init__(self, somenumber):
        self.somenumber = somenumber
