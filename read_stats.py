#!/usr/bin/env python3

import json
import logging
import matplotlib.pyplot as plt
from github import Github

logging.basicConfig(level=logging.INFO)

config = {}
with open('.config.json') as json_file:
    config = json.load(json_file)

g = Github(base_url=config['base_url'], login_or_token=config['access_token'])


def gather_stats_per_repo(repo):
    logging.info(f'gather stats for {repo.name}')
    stats = [gather_stats(pull) for pull in repo.get_pulls(state='closed')]
    return stats


def get_first_response_time(pr):
    res = pr.closed_at
    for comment in pr.get_issue_comments():
        if pr.user != comment.user and comment.created_at < res:
            res = comment.created_at
    for review in pr.get_reviews():
        if review.submitted_at < res:
            res = review.submitted_at
    return res


def gather_stats(pr):
    logging.info(f'gather stats from PR#{pr.number}')
    stats = {}
    stats['resolution_time'] = pr.closed_at - pr.created_at
    stats['merged'] = pr.merged
    stats['response_time'] = get_first_response_time(pr) - pr.created_at
    return stats


def draw_stats(stats):
    resolution_time = [stat['resolution_time'].seconds for stat in stats]
    ax = plt.subplot(2, 1, 1)
    ax.hist(resolution_time)
    ax.set_xlabel('resolution time')
    ax.set_ylabel('# of PRs')

    response_time = [stat['response_time'].seconds for stat in stats]
    ax = plt.subplot(2, 1, 2)
    ax.hist(response_time)
    ax.set_xlabel('first response time')
    ax.set_ylabel('# of PRs')

    print(f"Number of DISCARDED PRS = {stats.count(lambda x: x['merged'])}")

    plt.show()


for name in config['repos']:
    repo = g.get_repo(name)
    draw_stats(gather_stats_per_repo(repo))
