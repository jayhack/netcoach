import json
import flask
from flask import request
from flask import render_template
#from db import DBClient, ModelTracker

app = flask.Flask(__name__, static_url_path='/static')
#dbclient = DBClient()

######################################################################
##################[ STATIC ]##########################################
######################################################################

@app.route('/js/<path:path>')
def send_js(path):
    """sens js"""
    return app.send_static_file('js/{}'.format(path))

@app.route('/css/<path:path>')
def send_css(path):
    """sends css"""
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
    return json.dumps(["series_1", "series_2", "series_3"])

@app.route("/add_model", methods=['GET'])
def add_model():
    """
    Hook: add_model
    ---------------
    Adds a model to the DB; does nothing if model already exists.

    Incoming JSON format:
        {'name':'...', 'comment':'...'}
    """
    data = json.loads(request.data)
    mt = ModelTracker(data['name'], data['comment'])
    return 'success'


@app.route("/add_record", methods=['GET'])
def add_record():
    """
    Hook: add_record
    ----------------
    Adds a record for the specified model.

    Incoming JSON format:
        {
            'model_name':{'field_name':'value_name'},
            ...
        }
    """
    data = json.loads(request.data)
    record_data = request.get_json()
    for name, data in record_data.items():
        model_tracker = dbclient.get_model_tracker(name)
        for field, value in data.items():            
            model_tracker.add_record(value, field)
    return 'success'


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()