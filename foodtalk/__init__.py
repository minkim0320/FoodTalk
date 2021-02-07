#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 17:08:38 2021

@author: eriohoti
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin
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
auth = firebase.auth()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from foodtalk import routes