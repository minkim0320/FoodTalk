#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 21:20:53 2021
@author: eriohoti
"""

from flask import Flask, render_template,url_for,flash,redirect, session
from forms import RegistrationForm, LoginForm, BusinessForm
from flask_bcrypt import Bcrypt
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
#user
#uids = ''

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
                user = db.auth.sign_in_with_email_and_password(form.email.data, form.password.data)
                user = db.auth.refresh(user['refreshToken'])
                user_id = user['idToken']
                session['usr'] = user_id
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

@app.route('/business/items')
def business_items():
    uid = '-temp'
    user = db.child("Businesses").child(uid)
    items = user.child("items").get()
    bzName = db.child("Businesses").child("-temp").child("business").get()
    if items.val() == None:
        return render_template('businessPost.html', title='Business Post Feed', items=items)
    return render_template('businessPost.html', title='Business Post Feed', items=items, bzName=bzName)

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
        print(email == user.val().get("email"))
        if(email == user.val().get("email")):
            print(user.val().get("password"))
            if(bcrypt.check_password_hash(user.val().get("password"),password)):
                return True
    return False 

if __name__ == '__main__':
    app.run(debug=True)