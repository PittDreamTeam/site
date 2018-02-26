import os, time, json
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Spots


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='heypal',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'budget.db')
))
db.init_app(app)
api = Api(app)

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized DB")

@app.route("/", methods=['GET', 'POST'])
def default():
    if request.method == "POST":
        name = request.form["name"]
        return name + " spots"
    return render_template("default.html")

class Count(Resource):
    def get(self):
        countlist =[]
        for i in Count.query.all():
            count = {
            'count' : i.somenumber
            }
            countlist.append(cat)
            return jsonify(countlist)

        def post(self):
            print("POST")
            json_data = request.get_json(force=False)
            count = json_data['anumber']
            newCount = Count(count)
            db.session.add(newCount)
            db.session.commit()
            return jsonify(count=count)
        api.add_resource(Count, '/count', '/count/<count>')
