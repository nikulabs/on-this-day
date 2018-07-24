from __future__ import print_function
from HTMLParser import HTMLParser
import urllib2
import json
import xml.etree.ElementTree as ET
import time
import datetime

def lambda_handler(event, context):
    wikipedia = "https://en.wikipedia.org/w/api.php?action=featuredfeed&feed=onthisday&feedformat=atom"
    print(urllib2.urlopen(wikipedia).read())
    root = ET.fromstring( urllib2.urlopen(wikipedia).read() )
    print( root.tag )
    
    for child in root:
        print( child.tag, child.attribute )
    
    return 0
    #test = newdata[     
    
    #Python zero pads days, need to remove for days 1-9 of month
    day = time.strftime("%B")+"%20"+time.strftime("%d").lstrip("0").replace("%200", "%20")
    redirecturldate = time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+"000000"
    updateDate = datetime.datetime.now().isoformat()
    
    yahoo = "https://query.yahooapis.com/v1/public/yql"
    select = "?q=select%20description%20from%20rss%20where%20url%3D"
    wikipedia = "'http%3A%2F%2Fen.wikipedia.org%2Fw%2Fapi.php%3Faction%3Dfeaturedfeed%26feed%3Donthisday%26feedformat%3Drss'"
    tables = "%20%20and%20title%3D'On%20this%20day%3A%20" + day +"'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    url = yahoo+select+wikipedia+tables
    rssdata = json.load(urllib2.urlopen(url))
    description = rssdata['query']['results']['item']['description']
    stripped = strip_tags(description)

    if "More anniversaries" in stripped:
        stripped, trailer = stripped.split("More anniversaries",1)
    feed = { "uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
             "updateDate": updateDate,
             "titleText": "On This Day, "+time.strftime("%B")+" "+time.strftime("%d"),
             "mainText": stripped,
             "redirectionUrl": "https://en.wikipedia.org/wiki/Special:FeedItem/onthisday/"+redirecturldate+"/" }
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

lambda_handler("1","2")
