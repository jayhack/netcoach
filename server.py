"""
Module: server 
==============
Runs the actual server
"""
import flask
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

from db import DBClient, Record

app = flask.Flask(__name__)
dbclient = DBClient()


def make_figure(model_name):
    """makes and returns a figure"""
    mt = dbclient.get_model_tracker(model_name)
    loss_records = mt.get_records('loss')
    acc_records = mt.get_records('accuracy')
    fig = figure(
                tools='pan,wheel_zoom,reset',
                plot_width=500,
                plot_height=300
            )

    # TODO: switch this to timestamp?
    x = range(len(loss_records))
    fig.circle(x, loss_records['data'], legend="loss", color="red")
    fig.line(x, loss_records['data'], legend="loss", color="red")
    fig.circle(x, acc_records['data'], legend="accuracy", color="green")
    fig.line(x, acc_records['data'], legend="accuracy", color="green")

    return fig


@app.route("/")
def plot():
    """Grabs all active models and plots them"""
    


    # model_name = 'my_first_model'
    # mt = dbclient.get_model_tracker(model_name)
    # loss_records = mt.get_records('loss')
    # acc_records = mt.get_records('accuracy')

    # fig = figure(
    #             # title='{}'.format(model_name),
    #             tools='pan,wheel_zoom,reset',
    #             plot_width=500,
    #             plot_height=300
    #             )
    # fig.line(range(len(loss_records)), loss_records['data'])
    # fig.line(range(len(acc_records)), acc_records['data'])

    fig = make_figure('quadratic_model')

    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#module-bokeh.resources
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw + ['js'],
        css_raw=INLINE.css_raw + ['css'],
        js_files=INLINE.js_files + ['js'],
        css_files=INLINE.css_files + ['css'],
    )

    print INLINE.css_files + ['css']
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
    script, div = components(fig, INLINE)
    html = flask.render_template(
        'index.html',
        plot_script=script, plot_div=div, plot_resources=plot_resources,
        model_names=dbclient.get_model_names()
    )
    return encode_utf8(html)


def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()