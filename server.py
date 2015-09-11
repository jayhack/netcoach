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
from view import ModelView

app = flask.Flask(__name__)
dbclient = DBClient()


################################################################################
####################[ INITIALIZE MODEL VIEWS ]##################################
################################################################################

nrows, ncols = 3, 2
model_views = []
for i in range(nrows):
    model_views.append([])
    for j in range(ncols):
        model_views[i].append(ModelView())


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
    print mt.get_records(args['record_type'])    
    return 'successfully added record for model: {}'.format(args['model_name'])


################################################################################
####################[ INDEX ]###################################################
################################################################################

def parse_args(args):
    """parses args, generating (i, j, name) triplets"""
    print args.items()
    for k, v in args.items():
        splits = k.split('_')
        row, col = int(splits[-2]), int(splits[-1])
        yield row, col, v

def update_model_views(args):
    """updates model_view based on args"""
    for row, col, model_name in parse_args(args):
        mt = ModelTracker(model_name)
        model_views[row][col].update(mt)


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
        model_views=model_views,
        all_model_names=dbclient.get_model_names(),
        nrows=nrows, ncols=ncols
    )
    return encode_utf8(html)


def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()