"""
Module: visualizer
==================
Contains class for producing visualizations
"""
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

class ModelView(object):
	"""
	Class: Visualizer
	=================
	Produces plots of loss functions
	"""
	def __init__(self):
		self.name = ''
		self.comment = ''
		self.fig = figure(tools='pan,wheel_zoom,reset', plot_width=500, plot_height=300)
		self.script, self.div = components(self.fig, INLINE)

	def update(self, model_tracker):
		"""updates this view with internals of model_tracker"""
		#=====[ Step 1: update name/comment	]=====
		self.name = model_tracker.name
		self.comment = model_tracker.comment

		#=====[ Step 2: make figure	]=====
		loss_records = model_tracker.get_records('loss')
		acc_records = model_tracker.get_records('accuracy')
		self.fig = figure(
			tools='pan,wheel_zoom,reset',
			plot_width=500,
			plot_height=300
		)
		x = range(len(loss_records))
		self.fig.circle(x, loss_records['data'], legend="loss", color="red")
		self.fig.line(x, loss_records['data'], legend="loss", color="red")
		self.fig.circle(x, acc_records['data'], legend="accuracy", color="green")
		self.fig.line(x, acc_records['data'], legend="accuracy", color="green")

		#=====[ Step 3: make script/div	]=====
		self.script, self.div = components(self.fig, INLINE)


