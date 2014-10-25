from __future__ import division

import argparse
import datetime
import urllib
import sys
from subprocess import call, check_output
import json
import math
import random
import os
import shutil
import re


parser = argparse.ArgumentParser()
parser.add_argument('--repo', default='value')
parser.add_argument('--name')
parser.add_argument('--email')

parser.add_argument('--start')
parser.add_argument('--end')

parser.add_argument('-m', '--max', type=int, default=4)
parser.add_argument('--init', action='store_true')
parser.add_argument('-n', '--dry-run', action='store_true')

parser.add_argument('--html')
parser.add_argument('--refresh', action='store_true')

parser.add_argument('username')
args = parser.parse_args()


author_name = args.name or check_output(['git', 'config', 'user.name']).strip()
author_email = args.name or check_output(['git', 'config', 'user.email']).strip()

html_path = args.html or (args.username + '.html')
if args.refresh or not os.path.exists(html_path):
    with open(html_path, 'w') as fh:
        res = urllib.urlopen('https://github.com/%s' % args.username)
        fh.write(res.read())

existing = {}
for m in re.finditer(r'<rect.+?fill="#(.+?)" data-count="(.+?)" data-date="(.+?)"/>', open(html_path).read()):
    fill, raw_count, raw_date = m.groups()
    count = int(raw_count)
    existing[datetime.datetime.strptime(raw_date, '%Y-%m-%d').date()] = count

commit_levels = (
    1,
    2 * args.max // 4,
    3 * args.max // 4,
        args.max,
)


end = datetime.strptime(args.end, '%Y-%m-%d') if args.end else (
    (datetime.datetime.now() + datetime.timedelta(days=100)).date()
)
start = datetime.strptime(args.start, '%Y-%m-%d') if args.start else (
    (datetime.datetime.now() - datetime.timedelta(days=365 + 14 + 1)).date()
)

# Clear out the repo.
if args.init and os.path.exists(args.repo):
    shutil.rmtree(args.repo)
if not os.path.exists(args.repo):
    call(['git', 'init', args.repo])


date = start
while date <= end:

    days = (date - datetime.date(1970, 1, 1)).days
    count = commit_levels[days % 4] - existing.get(date, 0)

    for i in xrange(count):

        message = 'Commit %d/%d for %s (%d days since 1970-01-01)' % (i, count, date, days)

        with open('value/value.txt', 'w') as fh:
            fh.write(message + '\n')
        call(['git', 'add', 'value.txt'], cwd='value')

        hours, minutes = divmod(i, 60)
        timestamp = date.strftime('%Y-%m-%d') + ('T%s:%s:00' % (hours + 1, minutes))

        call(['git', 'commit', '-m', message], cwd=args.repo, env={
            'GIT_COMMITTER_DATE': timestamp,
            'GIT_COMMITTER_NAME': author_name,
            'GIT_COMMITTER_EMAIL': author_email,
            'GIT_AUTHOR_DATE': timestamp,
            'GIT_AUTHOR_NAME': author_name,
            'GIT_AUTHOR_EMAIL': author_email,
        })

    date += datetime.timedelta(days=1)

