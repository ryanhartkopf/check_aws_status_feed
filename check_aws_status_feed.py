#!/usr/bin/env python26

# Copyright 2014 AppliedTrust / Ryan Hartkopf
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import feedparser
import argparse

# Parse some args up in here.
# Note: 'route53', 'management-console', and 'all' do not need a region
parser = argparse.ArgumentParser(description='Check current status information from the AWS Service Health Dashboard (status.aws.amazon.com).')
parser.add_argument('service', choices=['s3', 'elasticache', 'management-console', 'cloudwatch', 'ec2', 'elb', 'rds', 'route53', 'vpc', 'iam', 'all'])
parser.add_argument('--region', choices=['us-east-1', 'us-west-1', 'us-west-2', 'us-standard'])
args = parser.parse_args()

if args.region == None or args.service == 'management-console' or args.service == 'route53':
  feed = args.service
else:
  feed = args.service + '-' + args.region

# Parse the feed and return value from the first entry. Return UNKNOWN to Nagios if error.
try:
  d = feedparser.parse('http://status.aws.amazon.com/rss/'+feed+'.rss')
  if d.entries:
    title = d.entries[0]['title']
    pubdate = d.entries[0]['published']
    dsc = d.entries[0]['description']
  elif d['feed']['title']:
    print 'AWS OK: No events to display.'
    exit(0)
except KeyError:
  print 'AWS UNKNOWN: Feed http://status.aws.amazon.com/rss/'+feed+'.rss could not be parsed. Check command options.'
  exit(3)

# Determine the state of the feed
if title.startswith("Service is operating normally"):
  status = 0
  msg = "AWS OK: "
elif (title.startswith("Informational message") or title.startswith("Performance issues") ):
  status = 1
  msg = "AWS WARNING: "
elif (title.startswith("Service disruption")):
  status = 2
  msg = "AWS CRITICAL: "
else:
  status = 3
  msg = "AWS UNKNOWN: "

# Return message and exit code to Nagios
msg += title
print msg
print pubdate
print dsc

exit(status)
