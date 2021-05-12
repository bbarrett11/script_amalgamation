from flask import Flask, request, jsonify,url_for, redirect
from flask import render_template
import sys

analyzed_fps = []

app = Flask(__name__)
@app.route('/known', methods=["GET", "POST"])
def known():
    return render_template('known.html')

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        fpid = request.json['id']
        print(fpid, file=sys.stderr)
        if(fpid in analyzed_fps):
            return jsonify({'page' : '/known'})
        else:
            analyzed_fps.append(fpid)
            return jsonify({'page' : 'None'})
    return render_template('index.html',known=known)