import os
from time import sleep

from flask import request, render_template
import requests

from app import app
from models import User
from utils import *



@app.route('/', methods=['GET', 'POST'])
def index():
    dirname = os.path.dirname(__file__)
    labels = get_items_from_txt(dirname, 'labels.txt')

    SEARCHES_PER_MINUTE = 10

    if request.method == 'POST':
        language = request.form.get("language")
        issues = []
        for label in labels:
            url = "https://api.github.com/search/issues?q=label:{}+language:{}+state:open&sort=created".format(label, language)
            response = requests.get(url)
            data = response.json()
            for item in data['items']:
                if item not in issues:
                    issues.append(item)
            if not response.from_cache:
                sleep(60/SEARCHES_PER_MINUTE)

        issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

        return render_template('results.html', issues_list=issues_sorted)
    elif request.method == 'GET':
        return render_template('form.html')
