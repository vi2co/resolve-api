#!/usr/bin/env python3
# encoding: utf-8
import json
import time
import dns.resolver
import re
from flask import Flask,jsonify,request,abort

app = Flask(__name__)

@app.errorhandler(400)
def wrong_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route('/')
def index():
    version = '0.1.0'
    kubernetes = 'false'
    return jsonify({'version': version,
            'date': int(time.time()),
            'kubernetes': 'false'})

@app.route('/v1/tools/lookup')
def lookup():
    domain = request.args.get('domain')

    if domain is None: 
        abort(400, description="Domain parameter is not set")

    ip_address = request.remote_addr

    try:
        # configure=False - don't rely on /etc/resolv.conf
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ["1.1.1.1"]
        
        response = dns.resolver.resolve(domain, "A")
        
        records = [] 
        for ip in response:
            records.append(str(ip))
        
        return json.dumps({'addresses': records,
                           'client_ip': ip_address,
                           'created_at': int(time.time()),
                           'domain': domain})

    except:
        abort(404, description="DNS records not found!")

@app.route('/v1/tools/validate', methods=['POST'])
def validate():
    ip = request.form['ip']

    ip_regex = (
        r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    )

    status = re.search(ip_regex, ip)
    if status:
        return jsonify({'status': True })
    else:
        return jsonify({'status': False })

# return jsonify({'version': ip_address})
