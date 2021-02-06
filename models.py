#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 04:36:04 2021

@author: eriohoti
"""


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
class Business(User):
    def __init__(self, username, email, password, businessname):
        super().__init__(username,email,password)
        self.businessname = businessname