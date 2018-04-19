import os, time, json, base64
import run_one, tint
from models import db, Entry
import pickle
from model import Model
from PIL import Image
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask import Markup
from flask_restful import Resource, Api, reqparse
from werkzeug import secure_filename, ImmutableMultiDict
from werkzeug.datastructures import FileStorage
from multiprocessing import Value



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
count = Value('i', 0)

net = pickle.load(open('net.pickle', 'rb'))
mod = Model(net)

@application.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized DB")

# print a nice greeting.
def default():
    spaces = Entry.query.order_by(Entry.id.desc()).first()
    open = 0
    if spaces:
        open = spaces.spots
    return render_template("index.html", openspots=open)


@application.route('/reset', methods = ['POST'])
def reset():
    if request.method == 'POST':
        with count.get_lock():
            count.value=0
        print("RESET")
        return "OK"

@application.route('/calibrate', methods = ['GET'])
def calibrate():
    if request.method == 'GET':
        img = Image.open('static/upload/picture.jpg')
        lane_img = mod.highlight_lanes(img)
        lane_img.save("static/processed/calibrate.jpg")
        return render_template("calibrate.html")

@application.route('/info', methods = ['GET', 'POST'])
def post_info():

    if request.method == 'POST':

        # Finished picture transaction comes in as application/json
        if request.headers['Content-Type'] == 'application/json':
            json = request.json
            msg=json['Msg']
            if(msg=='Done'):

                # Process picture
                img = run_one.get_im()
                park_img = mod.highlight_spaces(img)
                lane_img = mod.highlight_lanes(park_img)
                lane_img.save("static/processed/picture.jpg")

                bottom_spaces = len(mod.find_spaces(img))
                top_spaces = len(mod.find_spaces(img, top_lane=True))
                spaces = bottom_spaces + top_spaces
                print("\n\nspaces\n{}".format(spaces))

                # Commit DB statistics
                entry = Entry(spaces)
                db.session.add(entry)
                db.session.commit()

                # Reset Transaction
                with count.get_lock():
                    count.value=0

                return "DONE"


        else:
            print("else")
            # Check to make sure request.files is a thing
            if not request.files:
                return 'request.files is empty'
            data = dict(request.files)['testfile']
            picture = data[0]   # This is a filestorage object

            if picture:
                filename = picture.filename

                if count.value==0:
                    with open(os.path.join(application.config['UPLOAD_FOLDER'], filename), "wb") as myfile:
                        myfile.write(picture.stream.read())
                        myfile.close()
                        with count.get_lock():
                            count.value+=1
                    print("count - {}".format(count.value))
                    return "OK"
                elif count.value>0:
                    with open(os.path.join(application.config['UPLOAD_FOLDER'], filename), "ab") as myfile:
                        myfile.write(picture.stream.read())
                        myfile.close()
                    with count.get_lock():
                        count.value+=1
                    print("count - {}".format(count.value))
                    return "OK"

            else:
                return 'Bad file'

    elif request.method == 'GET':
        return render_template("index.html")


@application.route("/chart")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels)

# add a rule for the index page.
application.add_url_rule('/', 'default', (lambda: default() ))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
