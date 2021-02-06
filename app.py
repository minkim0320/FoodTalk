#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 21:20:53 2021

@author: eriohoti
"""

from flask import Flask, render_template,url_for
from forms import RegistrationForm, LoginForm
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = '663d8c19e83681bb7f7283ee73342404'

config = {
    "apiKey": "AIzaSyCFgKFUtm-kmXEZEoyecrbyxCTtFnLe1ik",
    "authDomain": "foodtalk-f05ed.firebaseapp.com",
    "databaseURL": "https://foodtalk-f05ed-default-rtdb.firebaseio.com",
    "projectId": "foodtalk-f05ed",
    "storageBucket": "foodtalk-f05ed.appspot.com",
    "messagingSenderId": "281572446405",
    "appId": "1:281572446405:web:6e30739ee8a7fc119120ac",
    "measurementId": "G-CGV0VJ25FT"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#user
#uids = ''

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
    #user = auth.sign_in_with_email_and_password(email,password)

@app.route('/business')
def business_main():
    uid = '-temp' #temp - user['idToken]
    user = db.child("Businesses").child(uid) #move these two lines to log in and register 
    bzName = user.child("business").get()
    analytics =db.child("Businesses").child(uid).child("analytics").get()
    if analytics.val() == None:
        return render_template('businessMain.html', title='Business Analytics', bzName=bzName)
    return render_template('businessMain.html', title='Business Analytics', analytics=analytics, bzName=bzName)

@app.route('/business/posts')
def business_posts():
    uid = '-temp'
    user = db.child("Businesses").child(uid)
    bzPosts = user.child("bzPost").get()
    bzName = db.child("Businesses").child("-temp").child("business").get()
    if bzPosts.val() == None:
        return render_template('businessPost.html', title='Business Post Feed', bzName=bzName)
    return render_template('businessPost.html', title='Business Post Feed', bzPosts=bzPosts, bzName=bzName)

@app.route('/customer')
def customer_main():
    uid = '-userTest' #temp - user['idToken]
    user = db.child("Users").child(uid) #move these two lines to log in and register 
    userName = user.child("username").get()
    mainFeed = db.child("Users").child(uid).child("followingBZ").get()
    if mainFeed.val() == None:
        return render_template('customerMain.html', title='Customer Feed', userName=userName)
    posts = []
    for p in mainFeed:
        currPost = db.child("Businesses").child(p.val()).child("bzPost").get()
        for cp in currPost:
            posts.append(cp)
    return render_template('customerMain.html', title='Customer Feed', posts=posts, userName=userName) 

if __name__ == '__main__':
    app.run(debug=True)