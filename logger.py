#!/usr/bin/env python
import feedparser, sys, hashlib, pprint

if len(sys.argv) < 3:
	print "Usage: {} <user_id> <token>".format(sys.argv[0])
	exit()

d = feedparser.parse("https://bitbucket.org/{}/rss/feed?token={}".format(*sys.argv[1:3]))

for entry in d.entries:
	entry['hash'] = hashlib.sha1(entry.published + entry.summary).hexdigest()
	pprint.pprint(entry)
	print

