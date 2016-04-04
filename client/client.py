"""
Module: client
==============

Contains class SeriesTracker, which allows you to
add series
"""
from datetime import datetime
import requests

class NetCoachClient(object):
    """
    Class: NetCoachClient
    =====================
    Allows you to send results on a particular net
    """
    def __init__(self, netcoach_url, netcoach_port):
        self.__dict__.update(locals())
        self.add_url = netcoach_url + ':' + netcoach_port + '/add_record'

    def add_record(self, series_name, val):
        """
        Adds a record to the NetCoach service
        :param series_name: name of the series to append to
        :param val: value to append
        :return: None
        """
        ts = str(datetime.now())
        requests.get(self.add_url, params={'series_name':series_name, 'ts':ts, 'val':val})
        return None
