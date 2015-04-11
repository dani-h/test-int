#!/usr/bin/env python
'''
A simple program to calculate parking costs.
Supply two dates as unix timestamps.
If the dates are invalid or the `startdate` is smaller than the `enddate` the
program will terminate abnormally.

The program can also be used in python by importing `calculate_cost()` and
providing two python datetimes as args.

Usage: ./task.py <startdate> <enddate>

'''
import sys
from datetime import datetime
import math

USAGE_STR = '''Usage: task.py <startdate> <enddate>

Provide unix timestamps.
The startdate has to be smaller than the enddate'''

def parse_dates(start, end):
    '''
    Parses two unix timestamps to datetimes.
    If the dates are invalid or start > end, the program will terminate
    abnormally.
    Otherwise it parses and returns the timestamps as python datetimes.

    @type start:    datetime.datetime
    @type end:      datetime.datetime

    @rtype:         (datetime.datetime, datetime.datetime)
    '''
    try:
        startdate_int = int(start)
        enddate_int = int(end)

        if startdate_int > enddate_int:
            print "Invalid dates"
            print USAGE_STR
            raise ValueError

        else:
            startdate = datetime.fromtimestamp(startdate_int)
            enddate = datetime.fromtimestamp(enddate_int)
            return startdate, enddate

    except ValueError:
        print "Invalid dates"
        print USAGE_STR
        raise ValueError

def calculate_day_cost(start_date, end_date):
    '''
    Calculates the daily cost between two clock hours
    Returns the cost as an int

    @type start_date    datetime
    @type end_date      datetime

    @rtype:             int
    '''
    # If the times are within the "free" times, cost is 0
    if (start_date.hour < 9 and end_date.hour < 9) or (
            start_date.hour > 18 and end_date.hour > 18):
        print "Cost insufficient return 0"
        return 0

    # You always pay for a full hour, if minutes or seconds pass you pay
    if start_date.hour < 9:
        start_date = datetime(year=start_date.year, month=start_date.month,
                day=start_date.day, hour=9)
    if end_date.hour > 18:
        end_date = datetime(year=end_date.year, month=end_date.month,
                day=end_date.day, hour=18)

    total_hrs = math.ceil((end_date - start_date).total_seconds() / 3600)
    # Cost per/h is 5
    cost = total_hrs * 5
    # The cost for the first hour is always 10
    cost += 5
    # Cap the max cost
    if cost > 25: cost = 25

    return cost

def calculate_cost(unix_start, unix_end):
    '''
    Calculates the cost between two dates in a simplified manner.
    If the intervals are within a single day, the hourly cost between those are
    calculated directly.
    If the intervals span more than one day, the first and the last dates are
    calculated on an hourly basis, the rest simply use the max cost of 25/day.

    @type unix_start:   int
    @type unix_end:     int

    @rtype:             int
    '''
    start_date, end_date = parse_dates(unix_start, unix_end)
    day_diff = end_date.day - start_date.day
    cost = 0
    if day_diff == 0:
        # Calculate that single day
        cost = calculate_day_cost(start_date, end_date)

    elif day_diff > 0:
        # End for first day is same day at 23:59:59
        end_of_day_startdate = datetime(
                year=start_date.year,
                month=start_date.month,
                day=start_date.day,
                hour=23,
                minute=59,
                second=59)
        cost += calculate_day_cost(start_date, end_of_day_startdate)

        # Start for last day is the same day at 00:00
        start_of_day_enddate = datetime(
                year=end_date.year,
                month=end_date.month,
                day=end_date.day)
        cost += calculate_day_cost(start_of_day_enddate, end_date)

        # For every other day other than the start and end the cost will
        # be the maximum cost of 25
        for i in xrange(1, day_diff):
            cost += 25

    return cost


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print USAGE_STR

    startdate, enddate = parse_dates(sys.argv[1], sys.argv[2])
    print "Start date", startdate
    print "End date", enddate

    total = calculate_cost(sys.argv[1], sys.argv[2])
    print "Total cost:", total

