from flask import Flask, render_template, send_file, request, abort, jsonify, redirect, url_for
import datetime
import random
import json
import uuid
from werkzeug import secure_filename
import glob
import os
from SimpleCV import *
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import numpy as np

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

    files = sorted(files, key= lambda f: os.path.getmtime(f))

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

        
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid4())+filename[-4:]

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if not is_cat(filename):
            os.remove(app.config['UPLOAD_FOLDER']+"/"+filename)
            
            return redirect(url_for('index'))

        return redirect(url_for('news'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
def is_cat(filename):
    b = Image(app.config['UPLOAD_FOLDER']+"/"+filename).findBlobs()[0]
    ary = [b.area(), b.height(), b.width()]
    name = target_names[clf.predict(ary)[0]]
    probability = clf2.predict_proba(ary)[0]

    if probability[1] < .5:
        return True
    else:
        return False

print "Training"
target_names = ['planes', 'cats']

planes = ImageSet('cv/supervised/planes') 
plane_blobs = [p.findBlobs()[0] for p in planes] #exact the blobs for our features
tmp_data = [] #array to store data features
tmp_target = [] #array to store targets

for p in plane_blobs: #Format Data for SVM
    tmp_data.append([p.area(), p.height(), p.width()])
    tmp_target.append(0)

cats = ImageSet('cv/supervised/cats')
cat_blobs = [c.findBlobs()[0] for c in cats]
for c in cat_blobs:
    tmp_data.append([c.area(), c.height(), c.width()])
    tmp_target.append(1)

dataset = np.array(tmp_data)
targets = np.array(tmp_target)

clf = LinearSVC()
clf = clf.fit(dataset, targets)
clf2 = LogisticRegression().fit(dataset, targets)

print "Done training"


if __name__ == '__main__':
    app.debug = True
    app.run(port=3333)


