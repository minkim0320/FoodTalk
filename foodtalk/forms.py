#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 00:17:51 2021

@author: eriohoti
"""


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators= [DataRequired(), 
                                        Length(min=3, max=20,message="Username must be between 3 and 20 chars")])
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email(message="Invalid email!")])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('password',message="Passwords must match!")])
    submit = SubmitField("Sign up")
    
   
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email(message="Are you sure this email exists?")])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    submit = SubmitField("Login")  
    business = BooleanField("Are you signing in as a business?")


class BusinessForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email(message="Invalid email!")])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('password',message="Passwords must match!")])
    businessname = StringField('Business',
                               validators = [Length(min=3, max=20, message="Input your business name")])
    submit = SubmitField("Register")
    
class ItemForm(FlaskForm):
    itemname = StringField('Item name',
                           validators = [DataRequired()])
    prive = StringField('Price',
                        validators = [DataRequired()])
    add = SubmitField("Add item")
                                                                                    