# -*- coding: utf-8 -*-
import time
import requests


class RequestDate:
    def __init__(self, request_time: float = time.time()):
        self.utc_time = time.gmtime(request_time)

    def get_url_format(self) -> str:
        # TODO: Windows specific? '#' vs '-' in format
        return time.strftime("%B_%#d", self.utc_time)

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
        "titles": f"Wikipedia:Selected_anniversaries/{requested_day.get_url_format()}"
    }

    wiki_data = requests.get("https://en.wikipedia.org/w/api.php", query_component).json()
    extracted = []
    for key, data in wiki_data["query"]["pages"].items():
        extracted.append(data["extract"])
    return extracted[0]


def process_text(unicode_data: str) -> list:
    data_list = unicode_data.splitlines()

    event_list = filter(is_event, data_list)
    event_list = map(remove_people_dates, event_list)
    event_list = map(remove_paren_word, event_list)

    event_list = [" In " + s for s in event_list]
    return event_list


def is_event(line: str) -> bool:
    if line and line[0].isdigit():
        return True
    return False


def remove_people_dates(line: str) -> str:
    try:
        index_of_separator = line.index(u'·')
        index_of_open_paren = line[:index_of_separator].index('(')
        index_of_event_end = line[:index_of_open_paren].index('.')
        line = line[:index_of_event_end+1]
    except (ValueError, IndexError):
        pass
    return line


def remove_paren_word(line: str) -> str:
    import re
    removed = re.sub(r'\(.*?\)', '', line)
    condensed = ' '.join(removed.split())
    return condensed


def build_json(on_this_day: list, day: RequestDate) -> dict:
    return {
        "uid": "urn:uuid:1335c695-cfb8-4ebb-abbd-80da344efa6b",
        "updateDate": day.get_update_format(),
        "titleText": "On This Day, "+time.strftime("%B %d"),
        "mainText": "".join(on_this_day),
        "redirectionUrl": "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"+day.get_url_format()
    }


def lambda_handler(event, context) -> dict:
    return get_on_this_day()


if __name__ == '__main__':
    import json
    print(json.dumps(get_on_this_day(), indent=2))
