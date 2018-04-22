from flask import Flask, render_template, request
from time import sleep

import requests
import json
import os

app = Flask(__name__)

def get_items_from_txt(dir, file):
    path = os.path.join(dir, file)
    reader = open(file, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items

def searches_per_minute(auth_string):
    return requests.get("https://api.github.com/rate_limit" + auth_string).json()['resources']['search']['limit']

def searches_remaining(auth_string):
    return requests.get("https://api.github.com/rate_limit" + auth_string).json()['resources']['search']['remaining']


@app.route('/', methods=['GET', 'POST'])
def main():
    dirname = os.path.dirname(__file__)

    labels = get_items_from_txt(dirname, 'labels.txt')
    credentials = get_items_from_txt(dirname, 'credentials.txt') #Client ID & Client Secret are stored here
    CLIENT_ID = credentials[0]
    CLIENT_SECRET = credentials[1]
    auth_string = "?client_id={}&client_secret={}".format(CLIENT_ID, CLIENT_SECRET)

    #SEARCHES_PER_MINUTE = searches_per_minute(auth_string)
    SEARCHES_PER_MINUTE = 10

    if request.method == 'POST':
        language = request.form.get("language")

        issues = []
        for label in labels:

            url = "https://api.github.com/search/issues?q=label:{}+language:{}+state:open&sort=created{}".format(label, language, auth_string)
            response = requests.get(url)
            data = response.json()
            for item in data['items']:
                if item not in issues:
                    issues.append(item)
            sleep(60/SEARCHES_PER_MINUTE)

        issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

        return render_template('main.html', issues_list=issues_sorted)
    elif request.method == 'GET':
        return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)
