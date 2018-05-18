import os

from functools import wraps
from flask import redirect, request, render_template, url_for
from flask_dance.contrib.github import github
import requests

from app import app
from utils import *


@app.route("/", methods=['GET'])
def index():
    return render_template('layout.html')


def github_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            assert False
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/search/<string:language>/<list:labels>", methods=['GET'])
@github_login_required
def search(language, labels):
    issues = github_search(labels, language)
    issues_sorted = sorted(issues,
                           key=lambda issue: issue['created_at'],
                           reverse=True)
    return render_template('results.html', issues_list=issues_sorted)


@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return redirect(url_for('index'))
