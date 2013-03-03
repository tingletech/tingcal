# Calendar

Playing around with a funky calendar scheme

sample calendar 
 * [pdf](http://tingletech.tumblr.com/tingcal/2013.zodiac.pdf)
 * [unicode text](http://tingletech.tumblr.com/tingcal/2013.zodiac.txt)

```
usage: tingcal.py [-h] [--zodiac] startmonth endmonth

create a calendar

positional arguments:
  startmonth  start month YYYY-MM
  endmonth    end month YYYY-MM

optional arguments:
  -h, --help  show this help message and exit
  --zodiac    print zodiac signs```

## example
```
./tingcal.py 2013-03 2013-06 --zodiac 
YYYY-Www  Mo Tu We Th Fr Sa Su     
2013-W09  25 26 27 28  ③  2  3     
2013-W10   4  5  6  7  8  9 10     
2013-W11  11 12 13 14 15 16 17     
2013-W12  18 19  ♈ 21 22 23 24     
2013-W13  25 26 27 28 29 30 31     
2013-W14   ④  2  3  4  5  6  7     
2013-W15   8  9 10 11 12 13 14     
2013-W16  15 16 17 18 19  ♉ 21     
2013-W17  22 23 24 25 26 27 28     
2013-W18  29 30  ⑤  2  3  4  5     
2013-W19   6  7  8  9 10 11 12     
2013-W20  13 14 15 16 17 18 19     
2013-W21  20  ♊ 22 23 24 25 26     
2013-W22  27 28 29 30 31  ⑥  2     
2013-W23   3  4  5  6  7  8  9     
2013-W24  10 11 12 13 14 15 16     
2013-W25  17 18 19 20  ♋ 22 23     
2013-W26  24 25 26 27 28 29 30     
```

## Why?  What?

This is how I like to see a calendar.  

I added in the [ISO 8601 calendar](http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm) weeks because of 
of [xkcd.com/1179/](http://xkcd.com/1179/).
There are also YYYY-Www-dd and YYYY-ddd that use numbers for the
day of the week of the day of the year in addition to YYYY-MM-dd.

I added in the zodiac signs for entertianment purposes only.

I might add the ISO calendar day of the year that each week starts on (for YYYY-ddd).

I might add full moons option (it would have to be exclusive to the zodiac option)
