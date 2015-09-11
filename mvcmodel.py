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

class PlotCell(object):
	"""
	Class: PlotCell
	===============
	Contains info for a single plot cell; has ability to create charts
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


class MVCModel(object):
	"""
	Class: MVCModel
	===============
	Contains full state of entire website
	"""
	def __init__(self, nrows=3, ncols=4, npages=10):
		self.nrows = nrows
		self.ncols = ncols
		self.npages = npages
		self._pages = []
		for p in range(npages):
			self._pages.append([])
			for r in range(nrows):
				self._pages[p].append([])
				for c in range(ncols):
					self._pages[p][r].append(PlotCell())

	def update_cell(self, page, row, col, model_tracker):
		self._pages[page][row][col].update(model_tracker)

	def get_cell(self, page, row, col):
		return self._pages[page][row][col]



