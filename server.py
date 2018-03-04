"""
Simple server to send map data back. Virtually nonexistent UI.
Run with `FLASK_APP=server.py flask run` after doing a pip install.
"""
from flask import Flask, flash, render_template, redirect, request, url_for
import json
import math
from mapping.mapping import make_mapping, process_input
from facility_location.algorithm import choose_facilities
from mapping.cost_gen import get_fcost, get_ccost
from common.helpers import distance
app = Flask(__name__)
app.secret_key = "super secret key"

def allowed_files(files):
    return (files['json'] is not None and files['json'].filename.endswith('.json')) or \
    (files['csvfacility'] is not None and files['csvfacility'].filename.endswith('.csv')
    and files['csvclient'] is not None and files['csvclient'].filename.endswith('.csv'))

@app.route('/')
def upload(error = None):
    return render_template('upload.html', error=error)

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

if __name__ == '__main__':
    app.run()
