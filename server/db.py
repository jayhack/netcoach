"""
Module: db
==========
Contains database module
"""
from os.path import exists
from os.path import join
import json
import pandas as pd
import sqlite3 as sq3


class DBClient(object):
	"""
	Class: DBClient
	===============
	Faciliates access to stored records

	Temporarily just reads/writes from a JSON file, 
	update this to orchestrate or local DB later
	"""
	def __init__(self, username, password):
		self.__dict__.update(locals())
		self.connect()

	def connect(self):
		"""connects to DB. TODO: update to orchestrate"""
		self.conn = sq3.connect(":memory:")

	def reset(self):
		"""clears all records"""
		cursor = self.conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS Models")
		cursor.execute("""
		CREATE TABLE Models(
		    id INTEGER PRIMARY KEY,
		    model_name TEXT,
		    comment TEXT,
		    metadata BLOB
		)""")
		cursor.execute("DROP TABLE IF EXISTS Records")
		cursor.execute("""
		CREATE TABLE Records(
		    id INTEGER PRIMARY KEY,
		    model_name TEXT,
		    value FLOAT
		)""")

	def get_series_names(self):
		"""returns a list of series names"""
		cursor = self.conn.cursor()
		cursor.execute("""
			SELECT DISTINCT 
		""")

	def get_series(self, name):
		"""returns pd.Series of all records for given model"""
		records = [r for r in self.records if r['name'] == name]
		return pd.DataFrame(records)

	def add_record(self, name, value):
		self.records.append({
			'name':name,
			'value':value,
			'timestamp':pd.datetime.now()
			})


class Model(object):
	"""
	Class: Model
	============
	Contains metadata, jumping point for series 

	Should be created through a join in SQL 
	"""
	def __init__(self, name, comment, metadata):
		self.__dict__.update(locals())


class Series(object):
	"""
	Class: Series
	=============
	Thin wrapper around a pd.Series that allows you to
	add records
	"""
	def __init__(self, dbclient, name):
		self.__dict__.update(locals())

	def add_record(self, value):
		self.dbclient.add_record(self.name, value)

	def get_values(self):
		"""returns pd.Series of values"""
		return self.dbclient.get_series(self.name)




