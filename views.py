import os

from flask import redirect, request, render_template, url_for
from flask_dance.contrib.github import github
import requests

from app import app
from models import User
from utils import *



@app.route("/", methods=['GET', 'POST'])
def index():
    dirname = os.path.dirname(__file__)
    labels = get_items_from_txt(dirname, 'labels.txt')

    language = request.form.get("language")
    if request.method == 'POST' and not language == "":

        issues = github_search(labels, language)

        if request.form.get("sort-chrono") == "ascending":
            issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=False)
        else:
            issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

        return render_template('results.html', issues_list=issues_sorted)
    else:
        return render_template('content.html')

@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])
