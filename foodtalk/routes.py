#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 17:30:03 2021

@author: eriohoti
"""
from flask import render_template,url_for,flash,redirect,session
from foodtalk import app, db, login_user, bcrypt
from foodtalk.forms import RegistrationForm, LoginForm, BusinessForm
from foodtalk.models import User,Business
from flask_login import current_user, logout_user

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    print(str(typeofUser))
    if(current_user.is_authenticated and current_user.get_business):
        return render_template('businessLayout.html')
    elif(current_user.is_authenticated and not current_user.get_business):
        return redirect(url_for('customer'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('index'))
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
    if(current_user.is_authenticated):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if(form.business.data):
            if(not validate_email(form.email.data,True) and validate_password(form.email.data, True, form.password.data)):
                all_users = db.child("Businesses").get()
                for gc in all_users.each():
                    if(form.email.data == gc.val().get("email")):
                        user = Business(uid= gc.key(),
                                        username = gc.val().get('businessname'),
                                        businessname = gc.val().get('businessname'),
                                        email = gc.val().get('email'),
                                        business = True)
                        user_id = gc.key()
                        userType = "Businesses"
                        login_user(user)
                flash(f'Account successfully logged in!', 'success')
                return business_main()
            else:
                flash(f'Email or password are wrong', 'danger')
        else:
            if(not validate_email(form.email.data,False) and validate_password(form.email.data, False, form.password.data)):
                all_users = db.child("Users").get()
                for gc in all_users.each():
                    if(form.email.data == gc.val().get("email")):
                        user = User(uid = gc.key(),
                                    username = gc.val().get('username'),
                                    email = gc.val().get('email'),
                                    business = False)
                        user_id = gc.key()
                        userType = "Users"
                        login_user(user)
                flash(f'Account successfully logged in! ', 'success')
                return customer_main()
            else:
                flash(f'Email or password are wrong', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register_business', methods=['GET', 'POST'])
def register_business():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    userType = typeofUser()
    user_id=current_user.get_id()
    bzName = db.child(userType).child(user_id).child("business").get()
    analytics = db.child(userType).child(user_id).child("analytics").get()
    if analytics.val() == None:
        return render_template('businessMain.html', title='Business Analytics', bzName=bzName)
    return render_template('businessMain.html', title='Business Analytics', analytics=analytics, bzName=bzName)

@app.route('/business/posts')
def business_posts():
    userType = typeofUser()
    user_id=current_user.get_id()
    bzPosts = db.child(userType).child(user_id).child("bzPost").get()
    bzName = db.child(userType).child(user_id).child("business").get()
    if bzPosts.val() == None:
        return render_template('businessPost.html', title='Business Post Feed', bzName=bzName)
    return render_template('businessPost.html', title='Business Post Feed', bzPosts=bzPosts, bzName=bzName)

@app.route('/business/items')
def business_items():
    userType = typeofUser()
    user_id=current_user.get_id()
    items = db.child(userType).child(user_id).child("items").get()
    bzName = db.child(userType).child(user_id).child("business").get()
    if items.val() == None:
        return render_template('itemsDisplay.html', title='Business Post Feed', items=items)
    return render_template('itemsDisplay.html', title='Business Post Feed', items=items, bzName=bzName)

@app.route('/customer')
def customer_main():
    userType = typeofUser()
    user_id=current_user.get_id()
    userName = db.child(userType).child(user_id).child("username").get()
    mainFeed = db.child(userType).child(user_id).child("followingBZ").get()
    if mainFeed.val() == None:
        return render_template('customerMain.html', title='Customer Feed', userName=userName)
    posts = []
    for p in mainFeed:
        currPost = db.child("Businesses").child(p.val()).child("bzPost").get()
        if currPost.val() is not None:
            for cp in currPost:
                posts.append(cp)
    return render_template('customerMain.html', title='Customer Feed', posts=posts, userName=userName) 

@app.route('/customer/cart')
def customer_cart():
    userType = typeofUser()
    user_id=current_user.get_id()
    #switch to currently selected USER later#####################################
    cart_items = db.child(userType).child(user_id).child("cart").get()
    if cart_items.val() == None:
        return render_template('customerCart.html', title='Customer', cart_items=cart_items)
    return render_template('customerCart.html', title='Customer Cart', cart_items=cart_items)

@app.route('/customer/business-view')
def cusotmer_view_business():
    bid = '-temp' #switch to currently selected business later#####################################
    bz = db.child("Businesses").child(bid)
    items = bz.child("items").get()
    bzName = db.child("Businesses").child("-temp").child("business").get()
    if items.val() == None:
        return render_template('userViewBZ.html', title='Viewing Business', items=items)
    return render_template('userViewBZ.html', title='Viewing Business', items=items, bzName=bzName)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'Successfully logged out', 'sucess')
    return redirect(url_for('index'))

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

def typeofUser():
    userType = current_user.get_business()
    if(not userType):
        result= "Users"
    else:
        result= "Businesses"
    return result
    
    
    
    
    
    
    
    
    