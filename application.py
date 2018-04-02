import os, time, json
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Info
from werkzeug import secure_filename, ImmutableMultiDict
from werkzeug.datastructures import FileStorage



UPLOAD_FOLDER = '/tmp/'

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.update(dict(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(application.root_path, 'parkpal.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
))

db.init_app(application)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@application.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized DB")

# print a nice greeting.
def default(username = "World"):
    return render_template("index.html")


@application.route('/info', methods = ['GET', 'POST'])
def post_info():

    if request.method == 'POST':
        # if request.headers['Content-Type'] == 'application/json':
        #     json = request.json
        #     info = Info(name=json['Name'], date=json['Date'], res=json['Resolution'], filetype=json['File'], data=json['Data'])
        #     db.session.add(info)
        #     db.session.commit()
        files = dict(request.files)['test']
        picture = files[0]
        if picture:
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            picture.close()
            return redirect(url_for('post_info'))
        else:
            return 'Bad File'

    elif request.method == 'GET':
        infos = Info.query.all()
        if infos is not None:
            return render_template("info.html", infos=infos)
        else:
            return render_template("info.html", infos=None)



# add a rule for the index page.
application.add_url_rule('/', 'default', (lambda: default() ))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
