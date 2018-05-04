import os
import requests
from flask_dance.contrib.github import github

def get_items_from_txt(dir, file):
    path = os.path.join(dir, file)
    reader = open(path, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items

def searches_per_minute():
    return github.get("https://api.github.com/rate_limit").json()['resources']['search']['limit']

def searches_remaining():
    return github.get("https://api.github.com/rate_limit").json()['resources']['search']['remaining']

def github_search(labels, language):
    issues = []
    for label in labels:
        url = ("/search/issues?q=label:{}+language:{}+state:open&sort=created"
        .format(label, language))
        # response = requests.get(url)
        # results = response.json()
        results = github.get(url).json()

        for item in results['items']:
            if item not in issues:
                issues.append(item)
    return issues
