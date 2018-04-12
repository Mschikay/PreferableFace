# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:07:58 2018

@author: hannah
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine, Integer
from app import app

db = SQLAlchemy(app)
# followed line must exist if a table has been deleted
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)

class Prefer(db.Model):
    __tablename__ = 'prefer'
    p_id = Column(String(20), primary_key=True)
    username = Column(String(20))
    prefername = Column(String(20))   
    prefernum = Column(Integer)

    def __init__(self, p_id, username, prefername, prefernum):
        self.p_id = p_id
        self.username = username
        self.prefername = prefername
        self.prefernum = prefernum
        
