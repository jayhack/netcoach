"""
Module: db
==========
Contains database module
Very simple implementation: entire DB is located in memory, is pickled/unpickled
on shutdown and startup. All records are contained in lists.
"""
from os.path import join
from os import listdir
from os.path import exists
import pickle

class DBClient(object):
    """
    Class: DBClient
    ===============
    Faciliates access to stored records
    Data is organized as follows:
    data = {
             series_name:[records...],
             series_name:[records...]
                ...
           }
    """
    def __init__(self, data_dir='./data'):
        self.__dict__.update(locals())
        if exists(join(data_dir, 'data.pkl')):
            self.data = pickle.load(open(join(data_dir, 'data.pkl')))
        else:
            self.data = {}

    def save(self):
        pickle.dump(self.data, open(join(self.data_dir, 'data.pkl'), 'w'))

    def reset(self):
        self.data = {}

    def get_series_names(self):
        return self.data.keys()

    def get_series(self, series_name):
        return self.data[series_name]

    def add_series(self, series_name):
        if series_name in self.data:
            raise Exception("Series already exists")
        self.data[series_name] = []

    def add_record(self, series_name, value, ts):
        self.data[series_name].append({'y':value, 'x':str(ts)})
