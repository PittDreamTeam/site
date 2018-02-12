import os, time, json
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Spots


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

class Spots(Resource):
    def get(self):
        catlist =[]
        for i in Category.query.all():
            cat = {
            'remaining' : i.remaining
            }
            catlist.append(cat)
        return jsonify(catlist)

    def post(self):
        print("HERE")
        json_data = request.get_json(force=False)
        spots = json_data['catname']
        budget = json_data['catbudget']
        if Spots.query.filter_by(name=category).first() != None:
            abort(409)
        newCat = Spots(category, budget)
        db.session.add(newCat)
        db.session.commit()
        return jsonify(name=category, budget=budget, remaining=newCa.remaining)

    def delete(self):
        name = request.get_json(force=True)
        cat = Spots.query.filter_by(name=name).first()
        db.session.delete(cat)
        purchasesToDelete = Purchase.query.filter_by(category=name).all()
        for purchase in purchasesToDelete:
            db.session.delete(purchase)
        db.session.commit()
        return jsonify(name=cat.name, budget=cat.budget, remaining=cat.remaining)


api.add_resource(Spots, '/spots', '/spots/<name>')


@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized DB")

@app.route("/")
def default():
    categories = Category.query.all()
    return render_template("default.html", categories=categories)
