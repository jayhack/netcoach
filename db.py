import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import pandas as pd

engine = create_engine('sqlite:///data/test_db.sqlite', echo=False)
Session = sessionmaker(bind=engine)

################################################################################
####################[ DATABSE SCHEMA ]##########################################
################################################################################

Base = declarative_base()

class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    record_type = Column(String)
    data = Column(PickleType)
    ts = Column(DateTime)

class Model(Base):
    """
    Class: Model:
    =============
    Represents an individual model
    """
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    comment = Column(String)

Base.metadata.create_all(engine)


################################################################################
####################[ ModelTracker ]############################################
################################################################################

class ModelTracker(object):
    """
    Class: ModelTracker 
    ===================
    Interface to the database for saving models, etc.

    Usage:
    ------
    >> mt = ModelTracker('3conv_2layers', comment='for cv pool app')
    >> mt.add_record(l, 'loss')
    >> mt.add_record(a, 'accuracy')
    """
    def __init__(self, name, comment=''):
        #=====[ Step 1: db setup ]=====
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        self.session = Session()

        #=====[ Step 2: grab model ]=====
        try:
            self.model = Model(name=name, comment=comment)
            self.session.add(self.model)
            self.session.commit()
        except:
            self.model = self.session.query(Model) \
                            .filter(Model.name.in_([name])) \
                            .first()

        #=====[ Step 3: set local ]=====
        self.name = self.model.name
        self.comment = self.model.comment

    def add_record(self, data, record_type):
        ts = datetime.datetime.now()
        r = Record(name=self.name, record_type=record_type, data=data, ts=ts)
        self.session.add(r)
        self.session.commit()
        return r

    def get_records(self, record_type):
        records = self.session.query(Record) \
            .filter(Record.name.in_([self.name])) \
            .filter(Record.record_type.in_([record_type])) \
            .order_by(Record.ts).all()
        df = pd.DataFrame({
            'id':[r.id for r in records],
            'data':[r.data for r in records],
            'ts':[r.ts for r in records]
        })
        return df


################################################################################
####################[ DBClient ]################################################
################################################################################

class DBClient(object):
    """
    Class: DBClient 
    ===============
    Allows you to stash records of loss, etc.
    """
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.session = Session()

    ################################################################################
    ####################[ ADDING ]##################################################
    ################################################################################

    def clear(self):
        """clears entire database"""
        self.session.query(Record).delete()
        self.session.query(Model).delete()
        self.session.commit()

    def get_model_names(self):
        """returns all unique model names"""
        names = [x[0] for x in self.session.query(Model.name).all()]
        return list(set(names))

    def get_model_tracker(self, name):
        """returns named model tracker or raises NameError"""
        if not name in self.get_model_names():
            raise NameError("No such model: {}".format(name))
        return ModelTracker(name)








