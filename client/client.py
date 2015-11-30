"""
Module: client
==============

Contains class SeriesTracker, which allows you to
add series
"""

class Model(object):
	"""
	Class: Model
	============
	Tracks a model
	"""
	def __init__(self, name, comment, metadata):
		self.__dict__.update(locals())

	def add_record(self):
		pass
