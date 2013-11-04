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
import datetime         # http://docs.python.org/2/library/datetime.html#date-objects
import ephem		# http://rhodesmill.org/pyephem/quick.html#phases-of-the-moon
import pprint

def tingcal(start, end, zodiac, lunar):
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
            # in order to prevent double weeks at the boundry between months
            # show only weeks where:
            if ( first_day_of_week.month == last_day_of_week.month 
                          # ↖ all days in same month
                   or first_week
                          # ↖ first week of month
                   or ( year == end.year and month == end.month)
                          # ↖ last month of calendar
            ):
                # print the out ISO 8601 calendar week
                #           YYYY-Www
                out = out + u'{}-W{:02d} '.format(iso_year, iso_week)
                zodiac_code=""
                lunar_code=""
                # day below is a datetime.date 
                for day in week:
                    # check if the zodiac sign changes today
                    if zodiac:
                        zodiac_code = zodiac_start(day.month, day.day)
                    if lunar:
                        lunar_code = lunar_start(day.year, day.month, day.day)
                    # the first day of the month is a special day
                    if day.day == 1:
                        num = unichr(start_enclosed_alphanumeric_range + day.month - 1)
                        out = out + u'  ' + num
                    elif lunar_code:
                        out = out + u' ' + lunar_code + u' '
                    elif zodiac_code:
                        out = out + u'  ' + zodiac_code
                    else:
                        out = out + u'{:>3}'.format(day.day)
                out = out + u"     \n"
                first_week = False
    print out.encode("utf-8")

def zodiac_start(month, day):
    signs = { 
              (  1, 20 ): u"\u2652",
              (  2, 18 ): u"\u2653",
              (  3, 20 ): u"\u2648",
              (  4, 20 ): u"\u2649",
              (  5, 21 ): u"\u264A",
              (  6, 21 ): u"\u264B",
              (  7, 22 ): u"\u264C",
              (  8, 23 ): u"\u264D",
              (  9, 23 ): u"\u264E",
              ( 10, 23 ): u"\u264F",
              ( 11, 22 ): u"\u2650",
              ( 12, 22 ): u"\u2651",
            }
    if (month,day) in signs:
        return signs[(month,day)]

def lunar_start(year, month, day):
    #  🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘 🌑
    # >>> ephem.next_full_moon((2013, 11, 17)).tuple()[:3]
    # (2013, 11, 17)
    if (year, month, day) == ephem.next_full_moon((year, month, day)).tuple()[:3]:
        return u"🌕"
    elif (year, month, day) == ephem.next_first_quarter_moon((year, month, day)).tuple()[:3]:
        return u"🌓"
    elif (year, month, day) == ephem.next_last_quarter_moon((year, month, day)).tuple()[:3]:
        return u"🌗"
    elif (year, month, day) == ephem.next_new_moon((year, month, day)).tuple()[:3]:
        return u"🌑"

    # >>> ephem.next_full_moon((2013, 11, 17)).tuple()[:3]

# main() idiom for importing into REPL for debugging 
def main(argv=None):
    def datearg(datestr):
        # http://stackoverflow.com/a/8198170/1763984
        return datetime.datetime.strptime(datestr, '%Y-%m') 
    parser = argparse.ArgumentParser(description='create a calendar')
    parser.add_argument('startmonth', nargs=1, type=datearg, help='start month YYYY-MM') 
    parser.add_argument('endmonth', nargs=1, type=datearg, help='end month YYYY-MM')
    parser.add_argument('--zodiac', action='store_const', const=True, help='print zodiac signs')
    parser.add_argument('--lunar', action='store_const', const=True, help='print lunar phase')
    # options for which set of enclosed characters are used
    # parser.add_argument('--start-enclosed-range' default u'①' hex 2460 decimal 9312
    # parser.add_argument('--start-zodiac-range' default 
    if argv is None:
        argv = parser.parse_args()

    tingcal(argv.startmonth[0], argv.endmonth[0], argv.zodiac, argv.lunar)

if __name__ == "__main__":
    sys.exit(main())
