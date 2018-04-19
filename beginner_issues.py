from flask import Flask, render_template
from requests import get
from time import sleep

import json
import os

app = Flask(__name__)

def get_items_from_txt(filepath):
    reader = open(filepath, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items


@app.route('/')
def main():
    NUM_RESULTS = 100
    SEARCHES_PER_MINUTE = 10
    language = "python"

    dirname = os.path.dirname(__file__)
    labels_path = os.path.join(dirname, 'labels.txt')
    labels = get_items_from_txt(labels_path)

    issues = []

    for label in labels:
        response = get("https://api.github.com/search/issues?q=label:" +
                                label + "+language:" + language + "+state:open&sort=created")
        data = response.json()
        for item in data['items']:
            if item not in issues:
                issues.append(item)
        #GitHub search API has limit of 10 searches per minute (Unauthenticated)
        #Sleep to avoid being rejected.
        sleep(60/SEARCHES_PER_MINUTE)

    issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

    return render_template('main.html', issues_list=issues_sorted)


if __name__ == "__main__":
    app.run(debug=True)
