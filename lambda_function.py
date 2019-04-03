# -*- coding: utf-8 -*-
import time
import requests


class RequestDate:
    def __init__(self, request_time: float = time.time()):
        self.utc_time = time.gmtime(request_time)

    def get_url_format(self) -> str:
        return time.strftime("%B_%d", self.utc_time).lstrip("0")

    def get_update_format(self) -> str:
        return time.strftime('%Y-%m-%dT', self.utc_time)+"00:00:00.0Z"


def get_on_this_day(requested_day: RequestDate = RequestDate()) -> dict:
    wiki_data = get_wikipedia_day_data(requested_day)
    on_this_day = process_text(wiki_data)
    feed = build_json(on_this_day, requested_day)
    return feed


def get_wikipedia_day_data(requested_day: RequestDate) -> str:
    query_component = {
        "format": "json",
        "action": "query",
        "prop": "extracts",
        "exintro": "True",
        "explaintext": "",
        "titles": get_url_title(requested_day)
    }

    wiki_data = requests.get("https://en.wikipedia.org/w/api.php", query_component).json()
    extracted = []
    for key, data in wiki_data["query"]["pages"].items():
        extracted.append(data["extract"])
    return extracted[0]


def process_text(unicode_data: str) -> list:
    def filter_to_events(line):
        if line and line[0].isdigit():
            return True

    data_list = unicode_data.splitlines()
    event_list = filter(filter_to_events, data_list)

    event_list = remove_people_dates(event_list)
    event_list = filter_to_read_words(event_list)

    event_list = [" In " + s for s in event_list]
    return event_list


def remove_people_dates(event_list: list) -> list:
    last_event = event_list[-1]
    index_of_separator = last_event.index(u'·')
    index_of_open_paren = last_event[:index_of_separator].index('(')
    index_of_event_end = last_event[:index_of_open_paren].index('.')
    event_list[-1] = last_event[:index_of_event_end+1]
    return event_list


def filter_to_read_words(event_list: list) -> list:
    # TODO: Implement
    replace_words = ['(pictured)']
    return event_list


def build_json(on_this_day: list, requested_day: RequestDate) -> dict:
    return {"uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
            "updateDate": requested_day.get_update_format(),
            "titleText": "On This Day, "+time.strftime("%B %d"),
            "mainText": "".join(on_this_day),
            "redirectionUrl": "https://en.wikipedia.org/wiki/"+get_url_title(requested_day)}


def get_url_title(request_time: RequestDate) -> str:
    return "Wikipedia:Selected_anniversaries/"+request_time.get_url_format()


def lambda_handler(event, context) -> dict:
    return get_on_this_day()


if __name__ == '__main__':
    print("Called with main")
