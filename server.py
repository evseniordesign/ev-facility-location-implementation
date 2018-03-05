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
    if not allowed_files(request.files):
        flash("Filetype not allowed", "error")
        return redirect(url_for('upload'))

    data = process_input(request.files)
    fcosts, ccosts = make_mapping(data, get_fcost, get_ccost)
    output = choose_facilities(fcosts, ccosts)

    facilities = [data['facilities'][facility.index]
            for facility in output.keys()]
    num_clients = [len(output[facility]) for facility in output.keys()]

    return render_template('map.html', points=facilities, weights=num_clients)

if __name__ == '__main__':
    app.run()
