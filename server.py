"""
Simple server to send map data back. Virtually nonexistent UI.
Run with `FLASK_APP=server.py flask run` after doing a pip install.
"""
from flask import Flask, flash, render_template, redirect, request, url_for
from mapping.cost_gen import get_fcost, get_ccost
from mapping.mapping import make_mapping, process_input
from mapping.powerlines import color_powerlines
from facility_location.algorithm import choose_facilities
app = Flask(__name__, static_url_path='/static')
app.secret_key = "super secret key"

def allowed_files(files):
    """
    Check whether 'files' is a valid set of files to run the algorithm on.
    """
    return ('json' in files and files['json'].filename.endswith('.json')) or \
    ('csvfacility' in files and files['csvfacility'].filename.endswith('.csv')
     and 'csvclient' in files and files['csvclient'].filename.endswith('.csv'))

def user_error(message):
    flash(message, 'error')
    return redirect(url_for('upload'))

@app.route('/')
def upload(error=None):
    """
    Present the upload page to the user.
    """
    return render_template('upload.html', error=error)

@app.route('/run', methods=['POST'])
def run_algorithm():
    """
    Run the algorithm and present google maps output to the user.
    """
    if not allowed_files(request.files):
        return user_error('Filetype not allowed')

    unassigned_clients = []
    facilities = []
    powerlines = []

    data = process_input(request.files)

    if not data:
        # User didn't provide enough files
        return user_error('Not enough data')

    try:
        make_mapping(data, get_fcost, get_ccost, use_time_dist=True)
    except (KeyError, ValueError):
        # Data didn't have correct keys
        # Either incomplete or invalid data files
        return user_error('Incorrectly formatted data')

    output = choose_facilities(data['facilities'], data['clients'])

    if 'powerlines' in data:
        try:
            powerlines = data['powerlines']
            color_powerlines(data, output)
        except KeyError:
            return user_error('Incorrectly formatted data')

    # Create objects to output to map
    for facility in output.keys():
        if 'dummy' not in facility:
            facility['assigned_clients'] = output[facility]
            facilities.append(facility)
        else:
            unassigned_clients = list(output[facility])

    if not facilities:
        return user_error('No facilities to open')

    return render_template('map.html',
                           points=facilities,
                           unassigned=unassigned_clients,
                           powerlines=powerlines)

if __name__ == '__main__':
    app.run()
