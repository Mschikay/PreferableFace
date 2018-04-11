#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:16:08 2018

@author: hannah
"""
from app import app
from form import LoginForm, ImgForm
from flask import render_template, request, redirect, url_for, session, flash
from db import db, Prefer
import sqlite3
import numpy as np

num = 0
filename = np.arange(app.config["PICNUM"])
save = []
db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    global num 
    num = 0
    # every time before user login, shuffle the image
    global filename
    np.random.shuffle(filename)
    form = LoginForm()
    session["user"] = ""
    error = None
    if request.method == 'POST':
        session["user"] = request.form['username']
        if session["user"] == "":
            error = 'Invalid username'
            flash("Please enter your name")
        elif (session["user"] in [prefer.username for prefer in db.session.query(Prefer).all()]):
            error = 'Replicated name'
            flash("Name already exists. Please alter another")
        else:
            print session["user"]
            # save the username
            # db.session.add(User(username=session["user"]))
            return redirect(url_for('showimg'))
    return render_template('login.html', title="Sign In", form=form, error=error)
    

def write2db(username, save):
    save = list(set(save))
    print save
    if len(save) == 0:
        return 
    else:
        try:
            table_prefer = Prefer.query.all()
            print len(table_prefer)
            if len(table_prefer) == 0:
                pid = np.int64(0)
            # get the last p_id
            else:
                pid = np.int64(table_prefer[-1].p_id)+1
            for i in range(len(save)):
                db.session.add(Prefer(p_id=str(pid+i), username=username, prefer=save[i]))
                db.session.commit()
        
        except sqlite3.IntegrityError, sqlite3.OperationalError:
            return 
        finally:
            # Close connection to DB
            db.session.close()
    return


@app.route('/showimg', methods=["GET", "POST"])
def showimg():
    global num
    global filename  
    imgform = ImgForm()

    if num == app.config["PICNUM"]/2-1:
        write2db(session["user"], save)
        return logout()

    print filename
    img1 = str(filename[num*2])+".jpg"
    img2 = str(filename[num*2+1])+".jpg"
    value1 = str(filename[num*2])
    value2 = str(filename[num*2+1])
    
    if request.method == "POST" :
        like = request.form["like"]
        if like != "":
            # save to write in database
            save.append(like)
        else:
            pass
        # randomly display 2 new images
        num = num+1    
        img1 = str(filename[num*2])+".jpg"
        img2 = str(filename[num*2+1])+".jpg"
        value1 = str(filename[num*2])
        value2 = str(filename[num*2+1])
        return render_template("showimg.html", form=imgform, img1=img1, 
                               img2=img2, value1=value1, value2=value2)
    else:
        return render_template("showimg.html", form=imgform, img1=img1, 
                               img2=img2, value1=value1, value2=value2)


@app.route('/logout')
def logout():
    session.pop("user", None)
    flash('Thanks. Finished. You were logged out')
    return redirect(url_for('login'))

 
if __name__ == '__main__':
    app.run(host='192.168.6.107', port=5000, debug=True)
