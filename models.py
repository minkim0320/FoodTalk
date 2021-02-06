#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 04:36:04 2021

@author: eriohoti
"""
from app import login_manager
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, username, email, password, userId):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__userId = userId


    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__userId)

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def set_userId(self, userId):
        self.__userId = userId

    def get_password(self):
        return self.__password
        
    def set_password(self, password):
        self.__password = password

    def __repr__(self):
        return f"User('{self.__userId}','{self.__username}', '{self.__email}')"
        
class Business(User):
    def __init__(self, username, email, password, businessname):
        super().__init__(username,email,password)
        self.businessname = businessname
    
    def get_businessname(self):
        return self.__businessname
    
    def set_businessname(self,businessname):
        self.__businessname = businessname