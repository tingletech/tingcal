#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" # tingcal.py
    creates a calendar; sort of like the unix `cal` command with a couple of changes
     * there are no gaps between months
     * the 1st of each month is replaced with a enclosed numeral representing the month
     * ? YYYY-Www indicated?
     * ? 21st replaced with zodiac sign
"""

from __future__ import unicode_literals
import argparse			# http://docs.python.org/2.7/library/argparse.html
import sys			# http://docs.python.org/2.7/library/sys.html
import calendar 		# http://docs.python.org/2/library/calendar.html 
				# http://pymotw.com/2/calendar/index.html

def main(argv=None):
    parser = argparse.ArgumentParser(description='create a calendar')
    parser.add_argument('year', nargs=1, type=int, help='four digit year')
    # options for which set of enclosed characters are used
    # parser.add_argument('--start-enclosed-range' default u'①' hex 2460 decimal 9312
    # parser.add_argument('--start-zodiac-range' default 
    if argv is None:
        argv = parser.parse_args()

# main() idiom for importing into REPL for debugging 
if __name__ == "__main__":
    sys.exit(main())
