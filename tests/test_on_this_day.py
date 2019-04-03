from lambda_function import RequestDate

import time

import unittest


class TestDateRequestMethods(unittest.TestCase):
    def test_get_url_format(self):
        july17 = time.mktime((2013, 7, 17, 0, 0, 0, 0, 0, 0))
        url_format_date = RequestDate(july17).get_url_format()
        self.assertEqual('July_17', url_format_date)

    def test_get_update_format(self):
        july17 = time.mktime((2013, 7, 17, 0, 0, 0, 0, 0, 0))
        url_format_date = RequestDate(july17).get_update_format()
        self.assertEqual('2013-07-17T00:00:00.0Z', url_format_date)


if __name__ == '__main__':
    unittest.main()
