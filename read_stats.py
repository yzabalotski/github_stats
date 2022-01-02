#!/usr/bin/env python3

import json
import logging
from github import Github

logging.basicConfig(level=logging.INFO)

config = {}
with open('.config.json') as json_file:
    config = json.load(json_file)

g = Github(base_url=config['base_url'], login_or_token=config['access_token'])


def gather_stats(pr):
    logging.info(f'gather stats from PR#{pr.number}')


for name in config['repos']:
    logging.info(f'processing {name}')
    repo = g.get_repo(name)
    pulls = repo.get_pulls(state='all')
    for pull in pulls:
        gather_stats(pull)
