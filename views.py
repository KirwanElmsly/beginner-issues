import os

from flask import redirect, request, render_template, url_for
from flask_dance.contrib.github import github
import requests

from app import app
from utils import *


@app.route("/", methods=['GET', 'POST'])
def index():
    dirname = os.path.dirname(__file__)
    labels = get_items_from_txt(dirname, 'labels.txt')

    language = request.form.get("language")
    if request.method == 'POST' and not language == "":
        issues = github_search(labels, language)
        issues_sorted = sorted(issues,
                               key=lambda issue: issue['created_at'],
                               reverse=True)
        return render_template('results.html', issues_list=issues_sorted)
    else:
        return render_template('content.html')


@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return redirect(url_for('index'))
