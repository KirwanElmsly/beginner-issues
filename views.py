import os
from time import sleep

from flask import request, render_template, url_for
import requests

from app import app
from models import User
from utils import *



@app.route('/', methods=['GET', 'POST'])
def index():
    dirname = os.path.dirname(__file__)
    labels = get_items_from_txt(dirname, 'labels.txt')

    language = request.form.get("language")
    if request.method == 'POST' and not language == "":
        issues = []
        for label in labels:
            url = ("https://api.github.com/search/issues?q=label:{}+language:{}+state:open&sort=created"
            .format(label, language))
            response = requests.get(url)
            data = response.json()

            for item in data['items']:
                if item not in issues:
                    issues.append(item)

            if request.form.get("sort-chrono") == "ascending":
                issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=False)
            else:
                issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

        return render_template('results.html', issues_list=issues_sorted)
    else:
        return render_template('content.html')
