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
    print(findBusiness(user_id))
    current_user_data= db.child(findBusiness(user_id)).order_by_key().equal_to(user_id).limit_to_first(1).get()
    print(findBusiness(user_id))
    if findBusiness(user_id) == "Users":
        return User(uid = user_id,
                    username = current_user_data.val()[user_id].get("username"),
                    email = current_user_data.val()[user_id].get("email"),
                    business = False)
    else:
        print("RETURNED A BUSINESS!")
        return Business(uid= user_id,
                        username = current_user_data.val()[user_id].get("businessname"),
                        businessname = current_user_data.val()[user_id].get("businessname"),
                        email = current_user_data.val()[user_id].get("email"),
                        business = True)

def findBusiness(user_id):
    userType = ["Users", "Businesses"]
    for x in userType:
        print(db.child(x).order_by_key().equal_to(user_id).limit_to_first(1).get().val())
        if db.child(x).order_by_key().equal_to(user_id).limit_to_first(1).get().val() is not None:
            return x
    
            
class User(UserMixin):

    def __init__(self, uid, username, email,business):
        self.__uid = uid
        self.__username = username
        self.__email = email
        self.__business = False

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
        
    def get_business(self):
        return self.__business


class Business(User):
    def __init__(self, uid, username, email, business, businessname):
        super().__init__(uid, username, email,business)
        self.__username = businessname
        self.__business = True
        self.__businessname = businessname
    
    def get_business(self):
        return self.__business
    
    def get_businessname(self):
        return self.__businessname
    
    def set_businessname(self,businessname):
        self.__businessname = businessname