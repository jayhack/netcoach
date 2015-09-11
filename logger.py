"""
Module: logger
==============
Contains class ModelLogger, the main interface to logging 
"""
import os
import requests
import pickle

class ModelLogger(object):
	"""
	Class: ModelLogger 
	==================
	Main interface to logging

	Usage:
	------
	>>> mlog = ModelLogger('my_model', 'http://jayhack.pythonanywhere.com')
	>>> mlog.add_record('loss', l)
	>>> mlog.add_record('accuracy', a)
	"""

	def __init__(self, name, comment=None, host_url='http://jayhack.pythonanywhere.com'):
		"""connect to remote server"""
		self.name = name
		self.comment = comment
		self.host_url = host_url
		self.model_url = self.host_url + '/add_model'
		self.record_url = self.host_url + '/add_record'
		

	def add_model(self):
		"""adds model to remote host"""
		payload = {
					'model_name':self.name,
					'comment':self.comment
		}
		r = requests.get(self.model_url, params=payload)
		return r

	def add_record(self, record_type, data):
		"""adds record to remote host"""
		payload = {
					'model_name':self.name,
					'record_type':record_type,
					'data_pickled':pickle.dumps(data)
				}
		r = requests.get(self.record_url, params=payload)