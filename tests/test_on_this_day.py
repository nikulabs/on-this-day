from lambda_function import RequestDate

import time

import unittest


class TestDateRequestMethods(unittest.TestCase):
    def test_date_url_format(self):
        july17 = time.mktime((2013, 7, 17, 0, 0, 0, 0, 0, 0))
        url_format_date = RequestDate(july17).get_url_format()
        self.assertEqual('July_17', url_format_date)


if __name__ == '__main__':
    unittest.main()
