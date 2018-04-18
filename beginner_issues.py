from requests import get
from time import sleep

import json
import os


def get_items_from_txt(filepath):
    reader = open(filepath, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items


def main():
    NUM_RESULTS = 20
    language = "python"

    dirname = os.path.dirname(__file__)

    labels_path = os.path.join(dirname, 'labels.txt')
    results_path = os.path.join(dirname, 'results.txt')

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
        #Sleep for 6 seconds to avoid being rejected.
        sleep(6)

    issues_sorted = sorted(issues, key=lambda issue: issue['created_at'], reverse=True)

    results_file = open(results_path, 'w', encoding="utf-8")

    for i in range(1, NUM_RESULTS+1):
        issue = issues_sorted[i-1]
        results_file.write(str(i) + ". " + issue['title'] + '\n')
        results_file.write('\t' + issue['html_url'] + '\n\n')
        results_file.write('\tLabels:\n')
        for label in issue['labels']:
            results_file.write('\t\t' + label['name'] + '\n')
        results_file.write('\n\n')

    results_file.close()

    return 1


if __name__ == "__main__":
    main()
