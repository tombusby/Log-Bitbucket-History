#!/usr/bin/env python
import feedparser, sys, hashlib
from lxml import etree
from StringIO import StringIO
from datetime import datetime

def make_table_header_row(table):
	row = etree.SubElement(table, "tr")
	etree.SubElement(row, "th").text = "Published"
	etree.SubElement(row, "th").text = "Processed to Log"
	etree.SubElement(row, "th").text = "Description"

def parse_entry_summary(entry):
	tree = etree.parse(StringIO(entry["summary"]), parse_entry_summary.parser)
	return tree.find(".//body").getchildren()
parse_entry_summary.parser = etree.HTMLParser()

def make_table_row(table, hash, entry):
	row = etree.SubElement(table, "tr")
	row.attrib["hash"] = hash
	etree.SubElement(row, "td").text = entry["published"]
	etree.SubElement(row, "td").text = datetime.today().isoformat()
	summary = etree.SubElement(row, "td")
	for element in parse_entry_summary(entry):
		summary.append(element)

def get_existing_log():
	try:
		return etree.parse("work_log.html").getroot()
	except:
		table = etree.Element("table")
		table.attrib["border"] = "1"
		table.attrib["style"] = "border-collapse: collapse;"
		make_table_header_row(table)
		return table

def get_existing_hashes(tree):
	return tree.xpath(".//tr/@hash")

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: {} <user_id> <token>".format(sys.argv[0])
		exit()

	user_id, token = sys.argv[1:3]

	table = get_existing_log()
	hashes = get_existing_hashes(table)
	feed_items = feedparser.parse("https://bitbucket.org/{}/rss/feed?token={}".format(user_id, token))
	entries_for_user = filter(lambda e: user_id in e["title"], feed_items.entries)

	for entry in sorted(entries_for_user, key=lambda k: k["published_parsed"]):
		hash = hashlib.sha1(entry.published + entry.summary).hexdigest()
		if hash not in hashes:
			make_table_row(table, hash, entry)

	with open("work_log.html", "w+") as f:
		f.write(etree.tostring(table, pretty_print=True))
