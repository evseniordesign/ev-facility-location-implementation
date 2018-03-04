"""
Simple server to send map data back. Virtually nonexistent UI.
Run with `FLASK_APP=server.py flask run` after doing a pip install.
"""
from flask import Flask, render_template, redirect, request, url_for
import json
import math
from mapping import make_mapping
from facility_location.algorithm import choose_facilities
app = Flask(__name__)

def distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat']) ** 2 +
                     (p1['long'] - p2['long']) ** 2)

facility_func = lambda facility: 1000000
client_func = lambda client, facility: distance(client, facility) * 1000

@app.route('/')
def upload():
    return render_template('upload.html')

@app.route('/run', methods=['POST'])
def run_algorithm():
    submitted_file = request.files['file']
    data = json.loads(submitted_file.read())
    #fcosts, ccosts = make_mapping(data, facility_func, client_func)
    #output = choose_facilities(fcosts, ccosts)
    #facilities = [data['facilities'][facility.index]
    #        for facility in output.keys()]

    print data
    #return render_template('map.html', points=data.facilities)

