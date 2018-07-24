from __future__ import print_function
from HTMLParser import HTMLParser
import urllib2
import json
import xml.etree.ElementTree as ET
import time
import datetime

testing = True;

def lambda_handler(event, context):

    wikipedia = "https://en.wikipedia.org/w/api.php?action=featuredfeed&feed=onthisday&feedformat=atom"
    root = ET.fromstring( urllib2.urlopen(wikipedia).read() )

    #Most current date is last in list
    #Body is second to last
    stripped = strip_tags(root[-1][-2].text)
    
    #Python zero pads days, need to remove for days 1-9 of month
    day = time.strftime("%B")+"%20"+time.strftime("%d").lstrip("0").replace("%200", "%20")
    redirecturldate = time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+"000000"
    updateDate = datetime.datetime.now().isoformat()
    
    if "More anniversaries" in stripped:
        stripped, trailer = stripped.split("More anniversaries",1)
    feed = { "uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
             "updateDate": updateDate,
             "titleText": "On This Day, "+time.strftime("%B")+" "+time.strftime("%d"),
             "mainText": stripped,
             "redirectionUrl": "https://en.wikipedia.org/wiki/Special:FeedItem/onthisday/"+redirecturldate+"/" }
    if testing:
        print(feed)
        return 0;
    else:
        return feed
    
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if testing:
    lambda_handler("1","2")
 
