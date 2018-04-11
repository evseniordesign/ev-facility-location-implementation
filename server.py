"""
Simple server to send map data back. Virtually nonexistent UI.
Run with `FLASK_APP=server.py flask run` after doing a pip install.
"""
from flask import Flask, flash, render_template, redirect, request, url_for
from mapping.cost_gen import get_fcost, get_ccost
from mapping.mapping import make_mapping, process_input
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
        flash("Filetype not allowed", "error")
        return redirect(url_for('upload'))

    try:
        data = process_input(request.files)
        make_mapping(data, get_fcost, get_ccost, use_time_dist=True)
    except Exception as e:
        print e
        flash("Incorrectly formatted data", "error")
        return redirect(url_for('upload'))

    output = choose_facilities(data['facilities'], data['clients'])

    unassigned_clients = []
    facilities = []
    powerlines = data['powerlines']
    for facility in output.keys():
        if 'dummy' not in facility:
            facility['assigned_clients'] = output[facility]
            facilities.append(facility)
        else:
            unassigned_clients = list(output[facility])

    if not facilities:
        flash("No facilities to open", "error")
        return redirect(url_for('upload'))

    return render_template('map.html',
                           points=facilities,
                           unassigned=unassigned_clients,
                           powerlines=powerlines)

if __name__ == '__main__':
    app.run()
