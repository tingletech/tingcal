#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" # tingcal.py
    creates a calendar; sort of like the unix `cal` command with a couple of changes
     * there are no gaps between months
     * the 1st of each month is replaced with a enclosed numeral representing the month
     * ? YYYY-Www indicated?
     * ? 21st replaced with zodiac sign
"""
# http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm

from __future__ import unicode_literals
import argparse			# http://docs.python.org/2.7/library/argparse.html
import sys			# http://docs.python.org/2.7/library/sys.html
import calendar 		# http://docs.python.org/2/library/calendar.html 

def tingcal(year):
    import pprint		# for debugging
    c = calendar.Calendar(calendar.MONDAY)
    out = u''
    start_enclosed_alphanumeric_range = 9312  # u'①' - 1
    # header
    out = out + u'YYYY-Www  Mo Tu We Th Fr Sa Su     \n'
    # collect the days
    # this gets nested deep, will need a refactor before it can take date ranges
    # http://docs.python.org/2/library/string.html#string-formatting
    for month in range(12):
        first_week = True
        for week in c.monthdatescalendar(year, month+1):
            first_day_of_week = week[0]
            last_day_of_week = week[6]
            iso_week = first_day_of_week.isocalendar()[1]
            iso_year = first_day_of_week.isocalendar()[0]
            # show only weeks where:
            if ( first_day_of_week.month == last_day_of_week.month 	 # all days in same month
                   or first_week 					 # first week of month
                   or first_day_of_week.year != last_day_of_week.year    # last week in year
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
    parser = argparse.ArgumentParser(description='create a calendar')
    parser.add_argument('year', nargs=1, type=int, help='four digit year')
    # options for which set of enclosed characters are used
    # parser.add_argument('--start-enclosed-range' default u'①' hex 2460 decimal 9312
    # parser.add_argument('--start-zodiac-range' default 
    if argv is None:
        argv = parser.parse_args()

    tingcal(argv.year[0])

if __name__ == "__main__":
    sys.exit(main())
