from flask import Flask, render_template, send_file, request, abort, jsonify
import datetime
import random
import json
import uuid

import src

app = Flask(__name__)

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/upload')
def about():
    return render_template("about.html", page_name="about")

@app.route('/login')
def resume():
    return render_template("about.html", page_name="about")
    
if __name__ == '__main__':
    app.debug = True
    app.run(port=3333)
