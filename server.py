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

app = flask.Flask(__name__, static_url_path='/templates')
dbclient = DBClient()


@app.route("/")
def plot():
    """Grabs all active models and plots them"""
    args = flask.request.args
    print args

    dbclient = DBClient()
    model_name = 'my_model'
    loss_df = dbclient.get_records(model_name, 'loss')

    fig = figure(title='{} Loss'.format(model_name))
    fig.line(range(len(loss_df)), loss_df['data'])

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