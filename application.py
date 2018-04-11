import os, time, json, base64
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Info
from werkzeug import secure_filename, ImmutableMultiDict
from werkzeug.datastructures import FileStorage





# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.update(dict(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(application.root_path, 'parkpal.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
))

UPLOAD_FOLDER = os.path.join(application.root_path, 'static/upload/')
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

        if not request.files:
            return 'request.files is empty'

        data = dict(request.files)['testfile']
        picture = data[0]   # This is a filestorage object

        print("Picture stream")
        print(picture.stream.read())
        if picture:
            filename = picture.filename
            picture.save(os.path.join(application.config['UPLOAD_FOLDER'], filename), buffer_size=4096)
            picture.close()
            print("Successfully saved post data")
            return redirect(url_for('post_info'))
        else:
            return 'Bad File'

    elif request.method == 'GET':
        return render_template("pic.html")




# add a rule for the index page.
application.add_url_rule('/', 'default', (lambda: default() ))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
