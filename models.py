from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
import datetime


db = SQLAlchemy()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    spots = db.Column(db.Integer, nullable = False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, spots):
        self.spots = spots

    def __repr__(self):
        return '<{}>'.format(self.id)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(LargeBinary, nullable = False)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<{}>'.format(self.name)
