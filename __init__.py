from flask import Flask, render_template, send_file, request, abort, jsonify, redirect, url_for
import datetime
import random
import json
import uuid
from werkzeug import secure_filename
import glob
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/newsfeed')
def news():
    files = glob.glob("static/uploads/*")
    if files is not None:
        files.reverse()
    return render_template("newfeed.html", page_name="NewsFeed", files=files)

@app.route('/upload')
def upload():
    return render_template("upload.html", page_name="upload")

@app.route('/login')
def login():
    return render_template("about.html", page_name="about")

@app.route('/upload_image', methods=["post","get"])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # check if cat

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('news'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
if __name__ == '__main__':
    app.debug = True
    app.run(port=3333)
