#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 21:20:53 2021

@author: eriohoti
"""

from flask import Flask, render_template,url_for
app = Flask(__name__)

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def hello_user():
    return 'Hello, World!'

@app.route('/business')
def hello_business():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True);