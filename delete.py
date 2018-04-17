#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:12:30 2018

@author: hannah
"""

from db import db, Prefer
from sqlalchemy import not_

query = Prefer.query.all()
for q in query:
    print q.p_id, q.username, q.prefername, q.prefernum
'''
for q in query:
    db.session.delete(q)
db.session.commit()
'''



#p = db.session.query(Prefer).filter(Prefer.username.like('hannah')).update({'username':'test1'}, synchronize_session=False)


