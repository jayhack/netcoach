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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

############################################################
##########[ SQL SETUP ]#####################################
############################################################

db = create_engine('sqlite:///data/netcoach.sqlite', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Record(Base):
    """
    Table: Record
    -------------
    Contains records - individual entries in series
    """
    __tablename__ = 'Records'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    series_name = Column(String)
    value = Column(PickleType)
    ts = Column(DateTime)


class Model(Base):
    """
    Class: Model:
    =============
    Contains models - metadata representing a given
    model.
    """
    __tablename__ = 'Models'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    comment = Column(String)
    meta = Column(PickleType)

Base.metadata.create_all(engine)
session = Session()


############################################################
##########[ DBClient ]######################################
############################################################

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

    def reset(self):
        """clears all records"""
        session.query(Record).delete()
        session.query(Model).delete()
        session.commit()

    def get_model_names(self):
        """returns a list of series names"""
        names = [x[0] for x in self.session.query(Model.name).all()]
        return list(set(names))

    def get_series_names(self):
        """returns a list of series names"""
        names = [x[0] for x in self.session.query(Record.series).all()]

    def get_series(self, name):
        """returns pd.Series of all records for given model"""
        records = [r for in self.records if r['name'] == name]
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




