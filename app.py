#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 21:20:53 2021

@author: eriohoti
"""

from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm, BusinessForm
from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
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
bcrypt = Bcrypt(app)

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {
            "username" : form.username.data,
            "email" : form.email.data,
            "password" : bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            }
        if(validate_email(form.email.data,False)):
            db.child("Users").push(data)  
            flash(f'Account successfully created', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Email already exists!', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.business.data):
            if(not validate_email(form.email.data,True) and validate_password(form.email.data, True, form.password.data)):
                flash(f'Account successfully logged in! Welcome, {form.email.data}', 'success')
                return redirect(url_for('index'))   
            else:
                flash(f'Email or password are wrong', 'danger')
        else:
            if(not validate_email(form.email.data,False) and validate_password(form.email.data, False, form.password.data)):
                flash(f'Account successfully logged in! Welcome, {form.email.data}', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Email or password are wrong', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register_business', methods=['GET', 'POST'])
def register_business():
    form = BusinessForm()
    if form.validate_on_submit():
        data = {
            "business" : form.businessname.data,
            "email" : form.email.data,
            "password" : bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            }
        if(validate_email(form.email.data,True)):
            db.child("Businesses").push(data)  
            flash(f'Account successfully created', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Email already exists!', 'danger')
    return render_template('register_business.html', title='Business Registration', form=form)


def validate_email(email,business):
    if business:
        all_users = db.child("Businesses").get()
    else:
        all_users = db.child("Users").get()
    for user in all_users.each():
        if(email == user.val().get("email")):
            return False
    return True  
             
def validate_password(email,business,password):
    if business:
        all_users = db.child("Businesses").get()
    else:
        all_users = db.child("Users").get()
    for user in all_users.each():
        if(email == user.val().get("email")):
            if(bcrypt.check_password_hash(user.val().get("password"),password)):
                return True
    return False 

if __name__ == '__main__':
    app.run(debug=True);