#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" # tingcal.py
    creates a calendar; sort of like the unix `cal` command with a
    couple of changes
     * there are no gaps between months
     * the 1st of each month is replaced with a enclosed numeral
       representing the month
     * ? YYYY-Www indicated?
     * ? 21st replaced with zodiac sign
"""
# http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm

from __future__ import unicode_literals
import argparse		# http://docs.python.org/2.7/library/argparse.html
import sys		# http://docs.python.org/2.7/library/sys.html
import calendar 	# http://docs.python.org/2/library/calendar.html 
import datetime         # 
import pprint

def tingcal(start, end):
    # http://stackoverflow.com/a/4040204/1763984
    start_month=start.month
    end_months=(end.year-start.year)*12 + end.month+1

    c = calendar.Calendar(calendar.MONDAY)
    out = u''
    start_enclosed_alphanumeric_range = 9312  # u'①' - 1
    # header
    out = out + u'YYYY-Www  Mo Tu We Th Fr Sa Su     \n'
    # collect the days
    # this gets nested deep, will need a refactor before it can take date ranges
    # http://docs.python.org/2/library/string.html#string-formatting
    for month in range(start_month, end_months):
        factor = (month - 1) // 12
        year = start.year + factor
        month = month - (factor * 12)
        first_week = True
        for week in c.monthdatescalendar(year, month):
            first_day_of_week = week[0]
            last_day_of_week = week[6]
            iso_week = first_day_of_week.isocalendar()[1]
            iso_year = first_day_of_week.isocalendar()[0]
            # show only weeks where:
            if ( first_day_of_week.month == last_day_of_week.month 
                          # all days in same month
                   or first_week
                          # first week of month
                   or ( year == end.year and month == end.month)
                          # last month of calendar
            ):
                out = out + u'{}-W{:02d} '.format(iso_year, iso_week)
                # day below is a datetime.date http://docs.python.org/2/library/datetime.html#date-objects
                for day in week:
                    # the first day of the month is a special day
                    if day.day == 1:
                        num = unichr(start_enclosed_alphanumeric_range + day.month - 1)
                        out = out + u'  ' + num
                    else:
                        out = out + u'{:>3}'.format(day.day)
                out = out + u"     \n"
                first_week = False
    print out.encode("utf-8")

# main() idiom for importing into REPL for debugging 
def main(argv=None):
    def datearg(datestr):
        # http://stackoverflow.com/a/8198170/1763984
        return datetime.datetime.strptime(datestr, '%Y-%m') 
    parser = argparse.ArgumentParser(description='create a calendar')
    parser.add_argument('startmonth', nargs=1, type=datearg, help='start month YYYY-MM') 
    parser.add_argument('endmonth', nargs=1, type=datearg, help='end month YYYY-MM')
    # options for which set of enclosed characters are used
    # parser.add_argument('--start-enclosed-range' default u'①' hex 2460 decimal 9312
    # parser.add_argument('--start-zodiac-range' default 
    if argv is None:
        argv = parser.parse_args()

    tingcal(argv.startmonth[0], argv.endmonth[0])

if __name__ == "__main__":
    sys.exit(main())
