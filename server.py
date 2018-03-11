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
    return ('json' in files and files['json'].filename.endswith('.json')) or \
    ('csvfacility' in files and files['csvfacility'].filename.endswith('.csv')
    and 'csvclient' in files and files['csvclient'].filename.endswith('.csv'))

@app.route('/')
def upload(error = None):
    return render_template('upload.html', error=error)

@app.route('/run', methods=['POST'])
def run_algorithm():
    if not allowed_files(request.files):
        flash("Filetype not allowed", "error")
        return redirect(url_for('upload'))

    try:
        data = process_input(request.files)
        make_mapping(data, get_fcost, get_ccost)
    except Exception as e:
        print e
        flash("Incorrectly formatted data", "error")
        return redirect(url_for('upload'))

    output = choose_facilities(data['facilities'], data['clients'])

    facilities = output.keys()
    for facility in facilities:
        facility['num_assigned_clients'] = len(output[facility])

    if not facilities:
        flash("No facilities to open", "error")
        return redirect(url_for('upload'))

    return render_template('map.html', points=facilities)

if __name__ == '__main__':
    app.run()
