# -*- coding: utf-8 -*-
import urllib2
import json
import time
import datetime

testing = True

def lambda_handler(event, context):
    return get_on_this_day()

def get_on_this_day():
    wiki_data = get_wiki_data()
    on_this_day = process_text( wiki_data )
    feed = build_json( on_this_day )
    return feed

def get_wiki_data():
    extract_command = "format=json&action=query&prop=extracts&exintro=True&explaintext="
    wikipedia = "https://en.wikipedia.org/w/api.php?"+extract_command+"&titles="+get_url_title()
    wiki_data = json.load(urllib2.urlopen(wikipedia))
    return wiki_data["query"]["pages"].values()[0]["extract"]

def process_text( unicode_data ):
    data_list = unicode_data.splitlines()
    event_list = filter(filter_to_events, data_list)

    event_list = remove_people_dates(event_list)
    event_list = filter_to_read_words(event_list)

    event_list = [" In " + s for s in event_list]
    return event_list

def filter_to_events(line):
    if line and line[0].isdigit():
        return True

def remove_people_dates(event_list):
    last_event = event_list[-1]
    index_of_separator =  last_event.index(u'·')
    index_of_open_paren = last_event[:index_of_separator].index('(')
    index_of_event_end = last_event[:index_of_open_paren].index('.')
    event_list[-1] = last_event[:index_of_event_end+1]
    return event_list

def filter_to_read_words(event_list):
#TODO Implement
    return event_list
    replace_words = ['(pictured)']
    for event in event_list:
        print(([word for word in event.split() if word.lower() not in replace_words]))

def build_json(on_this_day):
    redirect_url_date, update_date = get_dates()
    return { "uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
             "updateDate": update_date,
             "titleText": "On This Day, "+time.strftime("%B")+" "+time.strftime("%d"),
             "mainText": "".join(on_this_day),
             "redirectionUrl": "https://en.wikipedia.org/wiki/"+get_url_title()
           }

def get_dates():
    #Python zero pads days, need to remove for days 1-9 of month
    day = time.strftime("%B")+"%20"+time.strftime("%d").lstrip("0").replace("%200", "%20")
    redirect_url_date = time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+"000000"
    update_date = datetime.datetime.now().isoformat()
    return [redirect_url_date, update_date]

def get_url_title():
    return "Wikipedia:Selected_anniversaries/"+get_url_date()

def get_url_date():
    return time.strftime("%B_")+time.strftime("%d").lstrip("0")

if True:
    print get_on_this_day()
