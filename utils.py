import os
import requests
from datetime import datetime, timedelta
import json
from flask_dance.contrib.github import github


def get_items_from_txt(dir, file):
    """Gets list of labels from a text file."""
    path = os.path.join(dir, file)
    reader = open(path, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items


def searches_per_minute():
    """Returns number of searches available per minute"""
    return github.(get("https://api.github.com/rate_limit")
                   .json()['resources']['search']['limit'])


def searches_remaining():
    """Returns number of searches remaining"""
    return github.(get("https://api.github.com/rate_limit")
                   .json()['resources']['search']['remaining'])


def github_search(labels, language):
    """Searches GitHub Issues for given label and language.

    Keyword arguments:
    labels -- list of labels
    language -- string containing language to search
    """
    issues = []
    for label in labels:
        url = ("/search/issues?q=label:{}+language:{}+state:open&sort=created"
               .format(label, language))
        raw_results = github.get(url).json()

        for issue in raw_results['items']:
            if issue not in issues:
                issue = strip_issue(issue)
                issue['name'] = repo_name_from_url(issue['repository_url'])
                issue['time_alive'] = time_since(issue['created_at'])
                issues.append(issue)
    return issues


def strip_issue(issue):
    """Strips unneeded JSON data from issue"""
    unwanted_elems = ['url', 'labels_url', 'comments_url', 'events_url', 'number', 'locked', 'assignee', 'assignees', 'milestone', 'comments', 'updated_at', 'closed_at', 'author_association']

    for elem in unwanted_elems:
        del issue[elem]

    return issue


def repo_name_from_url(url):
    name = "/".join(url.split("/")[-2:])
    return name


def time_since(moment):
    """Returns human-readable time since a moment in the past.

    Keyword arguments:
    moment -- ISO8601 formatted time.
    """
    duration = ""
    dif = datetime.utcnow() - datetime.strptime(moment, '%Y-%m-%dT%H:%M:%SZ')

    if dif.days > 0:
        duration = "{} day".format(dif.days)
    elif dif.seconds > 3600:
        duration = "{} hour".format(dif.seconds // 3600)
    elif dif.seconds > 60:
        duration = "{} minute".format(dif.seconds // 60)
    else:
        duration = "{} second".format(dif.seconds)

    if duration[:2] != "1 ":
        duration = duration + "s"

    return duration
