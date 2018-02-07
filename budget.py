import os, time, json
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Category, Purchase


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='chatty',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'budget.db')
))
db.init_app(app)
api = Api(app)

class Categories(Resource):
    def get(self):
        catlist =[]
        for i in Category.query.all():
            cat = {
            'name' : i.name,
            'budget' : i.budget,
            'remaining' : i.remaining
            }
            catlist.append(cat)
        return jsonify(catlist)

    def post(self):
        json_data = request.get_json(force=True)
        category = json_data['catname']
        budget = json_data['catbudget']
        if Category.query.filter_by(name=category).first() != None:
            abort(409)
        newCat = Category(category, budget)
        db.session.add(newCat)
        db.session.commit()
        return jsonify(name=category, budget=budget, remaining=newCat.remaining)

    def delete(self):
        name = request.get_json(force=True)
        cat = Category.query.filter_by(name=name).first()
        db.session.delete(cat)
        purchasesToDelete = Purchase.query.filter_by(category=name).all()
        for purchase in purchasesToDelete:
            db.session.delete(purchase)
        db.session.commit()
        return jsonify(name=cat.name, budget=cat.budget, remaining=cat.remaining)


api.add_resource(Categories, '/cats', '/cats/<name>')

class Purchases(Resource):
    def get(self):
        purchaselist =[]
        json = {}
        for i in Purchase.query.all():
            purchase = {
            'name' : i.name,
            'amount' : i.amount,
            'category' : i.category
            }
            purchaselist.append(purchase)
            json = {"purchases" : purchaselist}
        return jsonify(json)

    def post(self):
        json_data = request.get_json(force=True)
        name = json_data['purname']
        amount = json_data['puramount']
        category = json_data['purcategory']
        newPur = Purchase(name, amount, category)
        cat = Category.query.filter_by(name=category).first()
        cat.remaining = cat.remaining - int(amount)
        db.session.add(newPur)
        db.session.commit()
        purchase = {
        'name' : name,
        'amount' : amount,
        'category' : category
        }
        category = {
        'name' : cat.name,
        'budget' : cat.budget,
        'remaining' : cat.remaining
        }
        json = {"purchase":purchase, "category":category}
        return jsonify(json)

api.add_resource(Purchases, '/purchases')



@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.add(Category("None", 0))
    db.session.commit()
    print("Initialized DB")

@app.route("/")
def default():
    categories = Category.query.all()
    return render_template("default.html", categories=categories)
