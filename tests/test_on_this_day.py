import lambda_function as aut

import time

import unittest
from unittest import mock


class TestDateRequestMethods(unittest.TestCase):
    def test_get_url_format_below_10(self):
        july17 = time.mktime((2013, 7, 9, 0, 0, 0, 0, 0, 0))
        url_format_date = aut.RequestDate(july17).get_url_format()
        self.assertEqual('July_9', url_format_date)

    def test_get_url_format_above_10(self):
        july17 = time.mktime((2013, 7, 17, 0, 0, 0, 0, 0, 0))
        url_format_date = aut.RequestDate(july17).get_url_format()
        self.assertEqual('July_17', url_format_date)

    def test_get_update_format(self):
        july17 = time.mktime((2013, 7, 17, 0, 0, 0, 0, 0, 0))
        url_format_date = aut.RequestDate(july17).get_update_format()
        self.assertEqual('2013-07-17T00:00:00.0Z', url_format_date)


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({
        "query": {
            "pages": {
                "1234": {
                    "pageid": 1234,
                    "ns": 0,
                    "title": "April 3",
                    "extract": "This is a test message"
                }
            }
        }
    }, 200)


class TestWikipediaOnThisDay(unittest.TestCase):

    # Same as above
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_wikipedia_day_data(self, side_effect):
        actual_response = aut.get_wikipedia_day_data(aut.RequestDate())
        expected_response = "This is a test message"
        self.assertEqual(expected_response, actual_response)

    def test_remove_people_dates(self):
        test_input = "last event.Name1 (d. 1154) \u00b7  Name Two (b. 1926)"
        actual_result = aut.remove_people_dates(test_input)
        expected_result = "last event."
        self.assertEqual(expected_result, actual_result)

    def test_remove_people_dates_from_empty_list(self):
        test_input = []
        actual_result = aut.remove_people_dates(test_input)
        expected_result = []
        self.assertListEqual(expected_result, actual_result)

    def test_remove_people_dates_where_none(self):
        test_input = ["first event.", "last event."]
        actual_result = aut.remove_people_dates(test_input)
        expected_result = ["first event.", "last event."]
        self.assertListEqual(expected_result, actual_result)

    def test_is_event_true(self):
        test_input = "1559 Event 1"
        actual_result = aut.is_event(test_input)
        expected_result = True
        self.assertEqual(expected_result, actual_result)

    def test_is_event_false(self):
        test_input = "Not an event"
        actual_result = aut.is_event(test_input)
        expected_result = False
        self.assertEqual(expected_result, actual_result)

    def test_remove_paren_word_single(self):
        test_input = "this is a (pictured) string"
        actual_result = aut.remove_paren_word(test_input)
        expected_result = "this is a string"
        self.assertEqual(expected_result, actual_result)

    def test_remove_paren_word_multiple(self):
        test_input = "(remove) this is a (pictured) string (remove)"
        actual_result = aut.remove_paren_word(test_input)
        expected_result = "this is a string"
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
