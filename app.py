#!/usr/bin/env python3
# encoding: utf-8
import json
import time
import dns.resolver
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, jsonify, request, abort, Response

app = Flask(__name__)
app.config.from_pyfile("config.py")

# Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info", version="1.0.0")

# DB initialization
engine = create_engine(app.config["DB_URI"])
metadata = MetaData(engine)
DBSession = sessionmaker(bind=engine)
db = DBSession()


@app.errorhandler(400)
def wrong_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/")
def index():
    version = "0.1.0"
    kubernetes = "false"
    return jsonify(
        {"version": version, "date": int(time.time()), "kubernetes": "false"}
    )


@app.route("/v1/tools/lookup")
def lookup():
    domain = request.args.get("domain")

    if domain is None:
        abort(400, description="Domain parameter is not set")

    ip_address = request.remote_addr

    try:
        # configure=False - don't rely on /etc/resolv.conf
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [app.config["NAMESERVER"]]
        response = dns.resolver.resolve(domain, "A")

        records = []
        for ip in response:
            records.append(str(ip))

        created = int(time.time())

        lookup = Table(app.config["TABLE_NAME"], metadata, autoload=True)

        engine.execute(
            lookup.insert().values(
                addresses=",".join(records),
                client_ip=ip_address,
                created_at=created,
                domain_name=domain,
            )
        )

        return json.dumps(
            {
                "addresses": records,
                "client_ip": ip_address,
                "created_at": created,
                "domain": domain,
            }
        )
    except:
        abort(404, description="DNS records not found!")


@app.route("/v1/tools/validate", methods=["POST"])
def validate():
    ip = request.form["ip"]

    ip_regex = (
        r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    )

    status = re.search(ip_regex, ip)
    if status:
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})


@app.route("/v1/tools/history")
def history():
    output = []

    lookup = Table(app.config["TABLE_NAME"], metadata, autoload=True)
    results = db.query(lookup).order_by(lookup.c.id.desc()).limit(20)
    count = results.count()

    for r in range(0, count):
        output.append(
            {
                "addresses": results[r][1].split(","),
                "client_ip": results[r][2],
                "created_at": results[r][3],
                "domain": results[r][4],
            }
        )

    return Response(json.dumps(output), mimetype="application/json")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})
