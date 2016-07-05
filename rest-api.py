import datetime
import requests
import json
from pprint import pprint
import re
import  logging

logging.basicConfig(level=logging.DEBUG)

TARGET_HOST = 'https://api.github.com'

OWNER_REPO = "django"

def find_fixed(message : str):
    '''
    >>> find_fixed('Fixed #26811 -- Added addButton option to admin ')
    [26811]
    >>> find_fixed('Fixed #26811 #2777 -- Added addButton option to admin ')
    [26811, 2777]
    '''
    list_of_tickets = []
    pattern = re.compile(r'#([0-9]+)')
    for match in pattern.findall(message):
        list_of_tickets.append(int(match))

    return list_of_tickets

headers = {
    'User-Agent': 'x', # needed when POST
    'Authorization': 'token x',
    'Content-type': 'application/json'
}

req = requests.get(TARGET_HOST, headers=headers)

foo = {}
json_req = json.dumps(foo)

response_dict = req.json()

fixed_commit_list = []

if "repository_url" in response_dict:
    repo_url = str(response_dict["repository_url"]).format(owner=OWNER_REPO, repo=OWNER_REPO)

    commit_list = requests.get(repo_url + "/commits", headers=headers).json()
    for commit in commit_list:
        date = datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        if (date < (datetime.datetime.today() - datetime.timedelta(days=31))):
            continue
        if "Fixed #" in commit["commit"]["message"]:
            fixed_commit_list += find_fixed(commit["commit"]["message"])

pprint(fixed_commit_list)

#if "message" in response_dict:
#    pprint(str(response_dict["message"]))


