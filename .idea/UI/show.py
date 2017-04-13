# -*- coding: utf-8 -*-
# !/usr/bin/env python
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import sys

sys.path.append('../')

from DB.mongoDBCilent import MongoDB
from Manager.proxyManager import Manager

app = Flask(__name__)
db = MongoDB('useful_proxy', 'localhost', 27017)

@app.route('/')
def index(proxylist=None):
    return render_template("index.html", proxylist=db.getAll())

@app.route('/refresh/')
def refresh():
    ma = Manager()
    ma.refresh()
    return "success"

@app.route('/get_all/')
def get_all():
    return jsonify(db.getAll())

@app.route('/delete/',methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    db.delete(proxy)
    return "success"

@app.route('/get/')
def get():
    return jsonify(db.get())

if __name__ == "__main__":
    app.run()



