import json
import flask
from flask import request
from flask import render_template
from db import DBClient

app = flask.Flask(__name__, static_url_path='/static')
dbclient = DBClient(data_dir='./data/')

######################################################################
##################[ STATIC ]##########################################
######################################################################

@app.route('/js/<path:path>')
def send_js(path):
    return app.send_static_file('js/{}'.format(path))

@app.route('/css/<path:path>')
def send_css(path):
    return app.send_static_file('css/{}'.format(path))

######################################################################
##################[ MAIN HOOKS ]######################################
######################################################################

@app.route("/get_series_list", methods=['GET', 'POST'])
def get_series_list():
    """
    Hook: get_series_list
    ---------------------
    Returns list of available series as a list of strings
    """
    return json.dumps(dbclient.get_series_names())

@app.route("/get_series", methods=['GET'])
def get_series():
    """
    Hook: get_plot_data
    -------------------
    Returns plot data for a specified series_id
    """
    series_name = request.args.get('series_name')
    records = dbclient.get_series(series_name)
    data = {
        'x':[r['x'] for r in records],
        'y':[r['y'] for r in records]
    }
    return json.dumps(data)

@app.route("/add_series", methods=['GET'])
def add_series():
    """
    Hook: add_series
    ----------------
    Adds a series to the DB; does nothing if model already exists.

    Incoming JSON format:
        {'name':'...', 'comment':'...'}
    """
    series_name = request.args.get('series_name')
    if not series_name in dbclient.get_series_names():
        dbclient.add_series(series_name)
    return 'Success'

@app.route("/add_record", methods=['GET'])
def add_record():
    """
    Hook: add_record
    ----------------
    Adds a record for the specified model.
    """
    series_name = request.args.get('series_name')
    ts = request.args.get('ts')
    val = request.args.get('val')
    dbclient.add_record(series_name, val, ts)
    return 'Success'

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()