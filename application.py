import os, time, json, base64
import run_one, tint


from PIL import Image
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, Info
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


@application.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized DB")

# print a nice greeting.
def default(username = "World"):
    return render_template("index.html")

@application.route('/reset', methods = ['POST'])
def reset():
    if request.method == 'POST':
        # with count.get_lock():
        #     count.value=0
        # print("RESET")
        im = Image.open("static/processed/picture.jpg")
        colorful = tint.tintRed(im, 100, 200, 100, 200)
        colorful.save("static/processed/picture.jpg")
        return "OK"


@application.route('/info', methods = ['GET', 'POST'])
def post_info():

    if request.method == 'POST':
        print("POST!\n\n\n")
        print("content type headers - {}".format(request.headers['Content-Type']))

        # Finished picture transaction comes in as application/json
        if request.headers['Content-Type'] == 'application/json':
            json = request.json
            msg=json['Msg']
            if(msg=='Done'):
                with count.get_lock():
                    count.value=0
                img = run_one.get_im()
                img.save("static/processed/picture.jpg")
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
        return render_template("pic.html")




# add a rule for the index page.
application.add_url_rule('/', 'default', (lambda: default() ))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
