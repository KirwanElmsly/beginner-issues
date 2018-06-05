import os

from functools import wraps
from flask import redirect, request, render_template, url_for, jsonify
from flask_dance.contrib.github import github
from flask_cors import cross_origin

import requests

from app import app
from utils import *


def github_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for("github.login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=['GET'])
@github_login_required
def index():
    return render_template('index.html')


@app.route("/search/<string:language>/<list:labels>", methods=['GET'])
@github_login_required
def search(language, labels):
    return render_template('search.html')


@app.route("/api/search/<string:language>/<list:labels>", methods=['GET'])
@cross_origin()
@github_login_required
def api_search(language, labels):
    issues = github_search(labels, language)
    results = {}
    results['items'] = issues
    json_results = jsonify(results)
    return json_results


@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return redirect(url_for('index'))
