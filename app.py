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

if __name__ == '__main__':
    app.run(debug=True);