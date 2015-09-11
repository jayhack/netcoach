"""
Module: server 
==============
Runs the actual server
"""
import pickle
import flask
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

from db import DBClient, ModelTracker, Model, Record
from mvcmodel import MVCModel

app = flask.Flask(__name__)
dbclient = DBClient()
nrows = 3
mvc_model = MVCModel(npages=1, nrows=3, ncols=2)

################################################################################
####################[ REST API ]################################################
################################################################################

@app.route('/add_model')
def add_model():
    args = flask.request.args
    mt = ModelTracker(args['model_name'], args['comment'])
    return 'success'

@app.route('/add_record')
def add_record():
    args = flask.request.args
    mt = ModelTracker(args['model_name'])
    data = pickle.loads(args['data_pickled'])
    mt.add_record(args['record_type'], data)
    return 'success'


################################################################################
####################[ INDEX ]###################################################
################################################################################

def parse_args(args):
    """parses args, generating (i, j, name) triplets"""
    for k, v in args.items():
        splits = k.split('_')
        row, col = int(splits[-2]), int(splits[-1])
        yield row, col, v

def update_model_views(args):
    """updates model_view based on args"""
    for row, col, model_name in parse_args(args):
        mt = ModelTracker(model_name)
        mvc_model.update_cell(0, row, col, mt)


@app.route("/")
def index():
    """plots all model views"""
    #=====[ Step 1: update model views ]=====
    update_model_views(flask.request.args)

    #=====[ Step 2: get plot resources ]=====
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw + ['js'],
        css_raw=INLINE.css_raw + ['css'],
        js_files=INLINE.js_files + ['js'],
        css_files=INLINE.css_files + ['css'],
    )

    #=====[ Step 3: render templates ]=====
    html = flask.render_template(
        'index.html',
        plot_resources=plot_resources,
        mvc_model=mvc_model,
        all_model_names=dbclient.get_model_names()
    )
    return encode_utf8(html)


def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()