# -*- coding: utf-8 -*-
import time
import requests


class RequestDate:
    def __init__(self, request_time):
        self.time = request_time

    def get_url_format(self):
        return self.time.strftime("%B_")+time.strftime("%d").lstrip("0")

    def get_update_format(self):
        return self.time.strftime('%Y-%m-%dT')+"00:00:00.0Z"


def lambda_handler(event, context):
    return get_on_this_day()


def get_on_this_day():
    wiki_data = get_wikipedia_day_data()
    on_this_day = process_text(wiki_data)
    feed = build_json(on_this_day)
    return feed


def get_wikipedia_day_data():
    extract_command = "format=json&action=query&prop=extracts&exintro=True&explaintext="
    wikipedia = "https://en.wikipedia.org/w/api.php?"+extract_command+"&titles="+get_url_title()
    wiki_data = requests.get(wikipedia).json()
    for key, data in wiki_data["query"]["pages"].items():
        return data["extract"]


def process_text(unicode_data):
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
    index_of_separator = last_event.index(u'·')
    index_of_open_paren = last_event[:index_of_separator].index('(')
    index_of_event_end = last_event[:index_of_open_paren].index('.')
    event_list[-1] = last_event[:index_of_event_end+1]
    return event_list


def filter_to_read_words(event_list):
    # TODO: Implement
    replace_words = ['(pictured)']
    return event_list


def build_json(on_this_day):
    return {"uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
            "updateDate": get_update_date(),
            "titleText": "On This Day, "+time.strftime("%B %d"),
            "mainText": "".join(on_this_day),
            "redirectionUrl": "https://en.wikipedia.org/wiki/"+get_url_title()}


def get_update_date():
    return time.strftime('%Y-%m-%dT')+"00:00:00.0Z"


def get_url_title():
    return "Wikipedia:Selected_anniversaries/"+get_url_date()


def get_url_date():
    return time.strftime("%B_")+time.strftime("%d").lstrip("0")

print(get_on_this_day(RequestDate(time)))
