import argparse
import urllib
import sys
from subprocess import call, check_output
import json
import math
import random
import os
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--repo', default='value')
parser.add_argument('--name')
parser.add_argument('--email')
parser.add_argument('--init', action='store_true')
parser.add_argument('username')
args = parser.parse_args()


author_name = args.name or check_output(['git', 'config', 'user.name']).strip()
author_email = args.name or check_output(['git', 'config', 'user.email']).strip()

data = json.loads(urllib.urlopen('https://github.com/users/%s/contributions_calendar_data' % args.username).read())

active_data = [day[1] for day in data if day[1]]

def average(seq):
    return sum(seq) * 1.0 / len(seq)

def variance(seq):
    avg = average(seq)
    return [(x - avg) ** 2 for x in seq]

mu = average(active_data)
sigma = math.sqrt(average(variance(active_data)))

print 'real stats:', mu, sigma



if args.init and os.path.exists(args.repo):
    shutil.rmtree(args.repo)
if not os.path.exists(args.repo):
    call(['git', 'init', args.repo])

for date, count in data:
    if count:
        continue
    year, month, day = date.split('/')
    count = max(1, int(round(random.gauss(mu, sigma))))
    print date, count

    for minute in xrange(count):
        with open('value/value.txt', 'w') as fh:
            fh.write('%s %s\n' % (date, minute))
        call(['git', 'add', 'value.txt'], cwd='value')

        timestamp = '%s-%s-%sT01:%s:00' % (year, month, day, minute)
        call(['git', 'commit', '-m', 'Adding value.'], cwd=args.repo, env={
            'GIT_COMMITTER_DATE': timestamp,
            'GIT_COMMITTER_NAME': author_name,
            'GIT_COMMITTER_EMAIL': author_email,
            'GIT_AUTHOR_DATE': timestamp,
            'GIT_AUTHOR_NAME': author_name,
            'GIT_AUTHOR_EMAIL': author_email,
        })

