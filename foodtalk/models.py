#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 04:36:04 2021

@author: eriohoti
"""
from foodtalk import login_manager,db
from flask_login import UserMixin

@login_manager.user_loader 
def load_user(user_id):

    #c_u = auth.current_user['idToken']
    current_user_data= db.child("Users").order_by_key().equal_to(user_id).limit_to_first(1).get()
    
    return User(uid = user_id,
                username = current_user_data.val().get("username"),
                email = current_user_data.val().get("email"))

class User(UserMixin):

    def __init__(self, uid, username, email):
        self.__uid = uid
        self.__username = username
        self.__email = email

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__uid
    
    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email
    
    def set_uid(self, uid):
        self.__uid = uid


class Business(User):
    def __init__(self, username, email, businessname):
        super().__init__(username,email)
        self.username = businessname
        self.businessname = businessname
    
    def get_businessname(self):
        return self.__businessname
    
    def set_businessname(self,businessname):
        self.__businessname = businessname