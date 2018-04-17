#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:16:08 2018

@author: hannah
"""
from gevent import wsgi
from app import app
from form import LoginForm, ImgForm
from flask import render_template, request, redirect, url_for, session, flash
from db import db, Prefer
import sqlite3
import numpy as np


num = 1
count = {}
db.create_all()
left = app.config["ITER_NUM"]


@app.route('/login', methods=['GET', 'POST'])
def login():
    global num, count
    num = 0
    count = {}
    # every time before user login, shuffle the image
    form = LoginForm()
    session["user"] = ""
    error = None
    if request.method == 'POST':
        session["user"] = request.form['username']
        session['num'] = num
        session['left'] = left
        session['count'] = count
        if session["user"] == "":
            error = 'Invalid username'
            flash("Please enter your name")
        #elif (session["user"] in [prefer.username for prefer in db.session.query(Prefer).all()]):
            #error = 'Replicated name'
            #flash("Name already exists. Please alter another")
        else:
            print session["user"]
            # save the username
            return redirect(url_for('showimg'))
    return render_template('login.html', title="Sign In", form=form, error=error)
    

def write2db(username, like):
    try:
        table_prefer = Prefer.query.all()
        if len(table_prefer) == 0:
            pid = np.int64(0)
            db.session.add(Prefer(p_id=str(1), username=username, prefername=like, prefernum=1))
        else:
            # get the last p_id(PRIMARY KEY, UNIQUE)
            pid = np.int64(table_prefer[-1].p_id)+1
            p = Prefer.query.filter(Prefer.username.like(username)&Prefer.prefername.like(like)).first()
            if p == None:
                db.session.add(Prefer(p_id=str(pid), username=username, prefername=like, prefernum=1))
            else:
                db.session.query(Prefer).filter(Prefer.username.like(username)&Prefer.prefername.like(like)).\
                update({'prefernum':str(int(p.prefernum)+1)}, synchronize_session=False)
        
    except sqlite3.IntegrityError, sqlite3.OperationalError:
        return 
    finally:
        db.session.commit()

    return


@app.route('/showimg', methods=["GET", "POST"])
def showimg():
    imgform = ImgForm()
    # randomly display 2 new images
    filename1 = np.random.randint(low=0, high=app.config["PIC_NUM"], dtype=np.int64)
    filename2 = np.random.randint(low=0, high=app.config["PIC_NUM"], dtype=np.int64)
    while(filename1 == filename2):
        filename2 = np.random.randint(low=0, high=app.config["PIC_NUM"], dtype=np.int64)    
    img1 = str(filename1)+".jpg"
    img2 = str(filename2)+".jpg"
    value1 = str(filename1)
    value2 = str(filename2)

    if request.method == "POST" :
        like = request.form["like"]
        if like != "":
            # save to write in database
            write2db(session["user"], like)
        else:
            pass
        session['num'] += 1
        session['left'] -= 1
        if session['num'] >= app.config["ITER_NUM"]:
            return logout()
        else:
            return render_template("showimg.html", form=imgform, img1=img1, 
                               img2=img2, value1=value1, value2=value2, left=session['left'])
    elif request.method == 'GET':      
        return render_template("showimg.html", form=imgform, img1=img1, 
                               img2=img2, value1=value1, value2=value2, left=session['left'])
    else:
        pass
    
    
@app.route('/logout')
def logout():
    # Close connection to DB
    db.session.close()
    session.pop("user", None)
    flash('Thanks. Finished. You were logged out')
    return redirect(url_for('login'))

 
if __name__ == '__main__':
    server = wsgi.WSGIServer(('192.168.6.107', 5000), app)
    server.serve_forever()

    #app.run(host='192.168.6.107', port=5000, debug=True)
