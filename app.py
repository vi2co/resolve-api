#!/usr/bin/env python3
# encoding: utf-8
import json
import time
from flask import Flask,jsonify
app = Flask(__name__)

version = '0.1.0'
kubernetes = 'false'

@app.route('/')
def index():
    date = int(time.time())
    return jsonify({'version': version,
            'date': date,
            'kubernetes': 'false'})
