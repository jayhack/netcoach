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

app = flask.Flask(__name__)
dbclient = DBClient()
nrows, ncols = 3, 2
plot_names = [[None, None], [None, None], [None, None]]


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

def make_figure(model_tracker):
    """makes and returns a figure"""
    loss_records = model_tracker.get_records('loss')
    acc_records = model_tracker.get_records('accuracy')
    fig = figure(
                tools='pan,wheel_zoom,reset',
                plot_width=500,
                plot_height=300
            )
    x = range(len(loss_records))
    fig.circle(x, loss_records['data'], legend="loss", color="red")
    fig.line(x, loss_records['data'], legend="loss", color="red")
    fig.circle(x, acc_records['data'], legend="accuracy", color="green")
    fig.line(x, acc_records['data'], legend="accuracy", color="green")
    return fig


def make_model_plot(model_name):
    """returns an object that has all plot fields filled"""
    if not model_name is None:
        mt = dbclient.get_model_tracker(model_name)
        fig = make_figure(mt)
        name = mt.name
        comment = mt.comment
    else:
        fig = figure(tools='pan,wheel_zoom,reset', plot_width=500, plot_height=300)
        name = ''
        comment = ''

    script, div = components(fig, INLINE)
    return {
                'fig':fig,
                'name':name,
                'comment':comment,
                'script':script,
                'div':div
            }


@app.route("/")
def plot():
    """Grabs all active models and plots them"""

    #=====[ Step 1: parse args ]=====
    args = flask.request.args
    for k, v in args.items():
        splits = k.split('_')
        row, col = int(splits[-2]), int(splits[-1])
        plot_names[row][col] = v

    #=====[ Step 2: assemble plots ]=====
    model_plots = [[None, None], [None, None], [None, None]]
    for i in range(nrows):
        for j in range(ncols):
                model_plots[i][j] = make_model_plot(plot_names[i][j])


    #=====[ Step 3: make templates ]=====
    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#module-bokeh.resources
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw + ['js'],
        css_raw=INLINE.css_raw + ['css'],
        js_files=INLINE.js_files + ['js'],
        css_files=INLINE.css_files + ['css'],
    )
    html = flask.render_template(
        'index.html',
        plot_resources=plot_resources,
        model_plots=model_plots,
        model_names=dbclient.get_model_names(),
        nrows=nrows, ncols=ncols
    )
    return encode_utf8(html)


def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()