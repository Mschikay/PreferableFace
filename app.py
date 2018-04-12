#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:07:58 2018

@author: hannah
"""

from flask import Flask

app = Flask(__name__)

# 必须设置
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "loginsystem"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/hannah/Desktop/flask/database/prefer.db'

app.config["PICPATH"] = "/home/hannah/Desktop/flask/templates/"
app.config["ITER_NUM"] = 1
app.config["PIC_NUM"] = 10
