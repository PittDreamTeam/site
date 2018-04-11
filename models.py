from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary


db = SQLAlchemy()

class Info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    date = db.Column(db.String(60), nullable = False)
    res = db.Column(db.String(60), nullable = False)
    filetype = db.Column(db.String(60), nullable = False)
    data = db.Column(db.String(100000), nullable = False)


    def __init__(self, name, date, res, filetype, data):
        self.name = name
        self.date = date
        self.res = res
        self.filetype = filetype
        self.data = data

    def __repr__(self):
        return '<{}>'.format(self.name)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(LargeBinary, nullable = False)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<{}>'.format(self.name)
