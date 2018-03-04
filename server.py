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

#facility_func = lambda facility: 1000 if "dummy" not in facility else 0
client_func = lambda client, facility: \
        distance(client['lat'], client['long'], \
            facility['lat'], facility['long'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['json', 'csv']

@app.route('/')
def upload(error = None):
    return render_template('upload.html', error=error)

@app.route('/run', methods=['POST'])
def run_algorithm():
    submitted_file = request.files['file']
    if not allowed_file(submitted_file.filename):
        flash("Filetype not allowed", "error")
        return redirect(url_for('upload'))
    data = process_input(submitted_file)
    fcosts, ccosts = make_mapping(data, get_fcost, get_ccost)
    output = choose_facilities(fcosts, ccosts)
    print(output.keys()[0])
    facilities = [data['facilities'][facility.index]
            for facility in output.keys()]


    return render_template('map.html', points=facilities)

if __name__ != '__main__':
    app.run()