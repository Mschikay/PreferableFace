#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:22:03 2018

@author: hannah
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField("", validators=[DataRequired()])
    
class ImgForm(FlaskForm):
    name1 = StringField("name1", validators=[DataRequired()])    
    name2 = StringField("name2", validators=[DataRequired()])    
