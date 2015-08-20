#!/usr/bin/env python
import feedparser, sys, hashlib, csv, re, os

def read_in_recorded_hashes(f):
	f.seek(0)
	hashes = []
	for row in csv.reader(f):
		hashes.append(row[0])
	return hashes

def process_summary_text(summary):
	summary = re.sub("<[^<]+?>", "", summary) # strip HTML tags
	summary = re.sub("\s+", " ", summary) # replace consecutive whitespace with single space
	return summary

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: {} <user_id> <token>".format(sys.argv[0])
		exit()

	user_id, token = sys.argv[1:3]

	feed_items = feedparser.parse("https://bitbucket.org/{}/rss/feed?token={}".format(user_id, token))

	file_dir = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(file_dir, "work_log.csv"), "a+") as f:
		hashes = read_in_recorded_hashes(f)
		writer = csv.writer(f)
		for entry in sorted(feed_items.entries, key=lambda k: k["published_parsed"]):
			if (user_id not in entry["title"]):
				continue
			hash = hashlib.sha1(entry["published"] + entry["summary"]).hexdigest()
			if hash not in hashes:
				writer.writerow([hash, entry.published, process_summary_text(entry.summary)])
