from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    budget = db.Column(db.Integer, nullable = False)
    remaining = db.Column(db.Integer, nullable = False)

    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.remaining = budget

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(60), nullable = False)

    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category
