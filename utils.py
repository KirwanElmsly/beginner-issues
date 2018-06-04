import os
import requests
from datetime import datetime, timedelta
import json
from flask_dance.contrib.github import github
from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)


def searches_per_minute():
    """Returns number of searches available per minute"""
    return github.get("/rate_limit").json()['resources']['search']['limit']


def searches_remaining():
    """Returns number of searches remaining"""
    return github.get("/rate_limit").json()['resources']['search']['remaining']


def github_search(labels, language):
    """Searches GitHub Issues for given label and language.

    Keyword arguments:
    labels -- list of labels
    language -- string containing language to search
    """
    issues = []
    labels = list(set(labels))
    if '' in labels: labels.remove('')
    for label in labels:
        url = ("/search/issues?q=label:{}+language:{}+state:open&sort=created"
               .format(label, language))
        raw_results = github.get(url).json()
        for issue in raw_results['items']:
            if issue not in issues:
                issue = strip_issue(issue)
                issue['name'] = repo_name_from_url(issue['repository_url'])
                issue['time_alive_readable'] = time_since_readable(issue['created_at'])
                issue['time_alive_seconds'] = time_since_unreadable(issue['created_at'])
                issues.append(issue)
    return issues


def strip_issue(issue):
    """Strips unneeded JSON data from issue"""
    unwanted_elems = ['body', 'url', 'labels_url', 'comments_url', 'events_url', 'number', 'locked', 'assignee', 'assignees', 'milestone', 'comments', 'updated_at', 'closed_at', 'author_association', 'user']

    for elem in unwanted_elems:
        del issue[elem]

    return issue


def repo_name_from_url(url):
    """Returns the name of a repository, given the repository URL"""
    name = "/".join(url.split("/")[-2:])
    return name


def time_since_unreadable(moment):
    """Returns unreadable time since a moment in the past.

    Keyword arguments:
    moment -- ISO8601 formatted time.
    """
    dif = datetime.utcnow() - datetime.strptime(moment, '%Y-%m-%dT%H:%M:%SZ')
    return int(dif.total_seconds())


def time_since_readable(moment):
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
