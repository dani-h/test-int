#!/usr/bin/env python
'''
Tests for the calculator

Note that all timestamps provided here are unix timestamps according to GMT+1
'''
import unittest
from task import calculate_cost
from datetime import datetime

class TestTask(unittest.TestCase):

    def test_invalid_dates(self):
        # Start > end
        # 2015-04-11 : 14:10:31
        start = 1428754231
        # 2015-04-11 : 12:10:31
        end = 1428747031

        with self.assertRaises(ValueError):
            calculate_cost(start, end)
            calculate_cost("foo", end)

    def test_dates_within_day(self):
        # 2013:01:04 : 09:03:02
        start = 1357286582
        # 2013:01:04 : 12:59:02
        end = 1357300742
        self.assertEqual(4 * 5 + 5, calculate_cost(start, end))

        # 2013:01:04 : 14:59:02
        start = 1357307942
        # 2013:01:04 : 16:23:02
        end = 1357312982
        self.assertEqual(5 * 2 + 5, calculate_cost(start, end))


    def test_dates_1_day_apart(self):
        # 2015-03-08 : 12:55:03
        start = 1425815703

        # 2015-03-09 : 09:55:55
        end = 1425891355
        self.assertEqual(25 + 10, calculate_cost(start, end))

    def test_dates_multiple_days_apart(self):
        # 2015-06-05 : 20:03:04
        start = 1433527384
        # 2015-06-08 : 12:55:03
        end = 1433760903
        self.assertEqual(25 + 25 + 4 * 5 + 5, calculate_cost(start, end))

    def test_free_hours(self):
        # 2015-04-11 : 05:14:56
        start = 1428722096
        # 2015-04-11 : 07:44:23
        end = 1428731063
        self.assertEqual(0, calculate_cost(start, end))

    def test_less_than_an_hour(self):
        # 2015-04-11 : 17:00:00
        start = 1428764400
        # 2015-04-11 : 17:07:04
        end = 1428764824
        self.assertEqual(10, calculate_cost(start, end))

    def test_minute_over(self):
        # 2015-04-11 : 11:01:00
        start = 1428742860
        # 2015-04-11 : 12:00:00
        end = 1428746400
        self.assertEqual(10, calculate_cost(start, end))

    def test_second_over(self):
        # 2015-04-11 : 13:01:23
        start = 1428750083
        # 2015-04-11 : 16:00:23
        end = 1428760823
        self.assertEqual(5 + 3 * 5, calculate_cost(start, end))

    def test_hours_exceed_max(self):
        # 2015-04-11 : 08:03:04
        start = 1428732184
        # 2015-04-11 : 20:03:04
        end = 1428775384
        self.assertEqual(25, calculate_cost(start,end))

if __name__ == '__main__':
    unittest.main()
