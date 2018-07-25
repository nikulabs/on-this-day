from __future__ import print_function
from HTMLParser import HTMLParser
import urllib2
import json
import xml.etree.ElementTree as ET
import time
import datetime
import unicodedata

testing = True

def lambda_handler(event, context):
    print_on_this_day()

def print_on_this_day():
    wiki_data = get_wiki_data()
    on_this_day = process_text( wiki_data )
    feed = build_json( on_this_day )

    if testing:
        print(feed)
        return 0
    else:
        return feed

def get_wiki_data():
    wikipedia = "https://en.wikipedia.org/w/api.php?action=featuredfeed&feed=onthisday&feedformat=atom"
    root = ET.fromstring( urllib2.urlopen(wikipedia).read() )

    #Most current date is last in list
    #Body is second to last
    return root[-2][-2].text

def process_text( unicode_data ):
    wiki_data = strip_tags(unicode_data)

    wiki_list = wiki_data.splitlines()
    event_list = list(filter_by_year(wiki_list))
    return event_list

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MyHTMLParser()
    s.feed(html)
    return s.get_data()

def filter_by_year(seq):
    for line in seq:
        if line and line[0].isdigit(): yield line

def build_json(on_this_day):
    redirect_url_date, update_date = get_dates()
    return { "uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
             "updateDate": update_date,
             "titleText": "On This Day, "+time.strftime("%B")+" "+time.strftime("%d"),
             "mainText": "".join(on_this_day),
             "redirectionUrl": "https://en.wikipedia.org/wiki/Special:FeedItem/onthisday/"+redirect_url_date+"/" }

def get_dates():
    #Python zero pads days, need to remove for days 1-9 of month
    day = time.strftime("%B")+"%20"+time.strftime("%d").lstrip("0").replace("%200", "%20")
    redirect_url_date = time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+"000000"
    update_date = datetime.datetime.now().isoformat()
    return [redirect_url_date, update_date]


if testing:
    lambda_handler("1","2")
