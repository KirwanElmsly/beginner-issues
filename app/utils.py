import os

def get_items_from_txt(dir, file):
    path = os.path.join(dir, file)
    reader = open(path, 'r')
    items = [s.rstrip() for s in reader.readlines()]
    reader.close()
    return items

def searches_per_minute(auth_string):
    return requests.get("https://api.github.com/rate_limit" + auth_string).json()['resources']['search']['limit']

def searches_remaining(auth_string):
    return requests.get("https://api.github.com/rate_limit" + auth_string).json()['resources']['search']['remaining']
