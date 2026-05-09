import argparse
import calendar
import datetime
import http.server
import socketserver
import sys

import ephem


def tingcal(start, end, zodiac, lunar):
    start_month = start.month
    end_months = (end.year - start.year) * 12 + end.month + 1

    c = calendar.Calendar(calendar.MONDAY)
    out = ""
    start_enclosed_alphanumeric_range = 9312

    out = out + "YYYY-Www  Mo Tu We Th Fr Sa Su     \n"

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
            if (
                first_day_of_week.month == last_day_of_week.month
                or first_week
                or (year == end.year and month == end.month)
            ):
                out = out + "{}-W{:02d} ".format(iso_year, iso_week)
                zodiac_code = ""
                lunar_code = ""
                for day in week:
                    if zodiac:
                        zodiac_code = zodiac_start(day.month, day.day)
                    if lunar:
                        lunar_code = lunar_start(day.year, day.month, day.day)
                    if day.day == 1:
                        num = chr(start_enclosed_alphanumeric_range + day.month - 1)
                        out = out + "  " + num
                    elif lunar_code:
                        out = out + " " + lunar_code
                    elif zodiac_code:
                        out = out + "  " + zodiac_code
                    else:
                        out = out + "{:>3}".format(day.day)
                out = out + "     \n"
                first_week = False
    print(out)


def zodiac_start(month, day):
    signs = {
        (1, 20): "\u2652",
        (2, 18): "\u2653",
        (3, 20): "\u2648",
        (4, 20): "\u2649",
        (5, 21): "\u264A",
        (6, 21): "\u264B",
        (7, 22): "\u264C",
        (8, 23): "\u264D",
        (9, 23): "\u264E",
        (10, 23): "\u264F",
        (11, 22): "\u2650",
        (12, 22): "\u2651",
    }
    if (month, day) in signs:
        return signs[(month, day)]


def lunar_start(year, month, day):
    if (year, month, day) == ephem.next_full_moon((year, month, day)).tuple()[:3]:
        return "\U0001F315"
    elif (year, month, day) == ephem.next_first_quarter_moon(
        (year, month, day)
    ).tuple()[:3]:
        return "\U0001F313"
    elif (year, month, day) == ephem.next_last_quarter_moon((year, month, day)).tuple()[
        :3
    ]:
        return "\U0001F317"
    elif (year, month, day) == ephem.next_new_moon((year, month, day)).tuple()[:3]:
        return "\U0001F311"


def tingcal_html(start, end, zodiac, lunar):
    start_month = start.month
    end_months = (end.year - start.year) * 12 + end.month + 1

    c = calendar.Calendar(calendar.MONDAY)
    rows = []

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
            if (
                first_day_of_week.month == last_day_of_week.month
                or first_week
                or (year == end.year and month == end.month)
            ):
                row = ["{}-W{:02d}".format(iso_year, iso_week)]
                zodiac_code = ""
                lunar_code = ""
                for day in week:
                    if zodiac:
                        zodiac_code = zodiac_start(day.month, day.day)
                    if lunar:
                        lunar_code = lunar_start(day.year, day.month, day.day)
                    if day.day == 1:
                        num = chr(9312 + day.month - 1)
                        row.append(num)
                    elif lunar_code:
                        row.append(lunar_code)
                    elif zodiac_code:
                        row.append(zodiac_code)
                    else:
                        row.append(str(day.day))
                rows.append(row)
                first_week = False

    table = "<table>\n"
    headers = ["YYYY-Www", "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    table += "<tr>" + "".join("<th>{}</th>".format(h) for h in headers) + "</tr>\n"
    for row in rows:
        table += "<tr>" + "".join("<td>{}</td>".format(c) for c in row) + "</tr>\n"
    table += "</table>"
    return table


def _build_page(start, end, table_html):
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>tingcal {} to {}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2em; }}
  table {{ border-collapse: collapse; font-family: "SF Mono", "Cascadia Code", "Consolas", monospace; }}
  th, td {{ padding: 4px 10px; text-align: center; }}
  th {{ background: #f5f5f5; font-weight: 600; border-bottom: 2px solid #ddd; }}
  td {{ border-bottom: 1px solid #eee; }}
  tr:hover td {{ background: #fafafa; }}
</style>
</head>
<body>
<h1>tingcal {} to {}</h1>
{}
</body>
</html>""".format(
        start.strftime("%Y-%m"),
        end.strftime("%Y-%m"),
        start.strftime("%Y-%m"),
        end.strftime("%Y-%m"),
        table_html,
    )


def run_server(host, port, start, end, zodiac, lunar):
    html = tingcal_html(start, end, zodiac, lunar)
    page = _build_page(start, end, html)

    class CalendarHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

        def log_message(self, format, *args):
            sys.stderr.write("[tingcal] {} {} {}\n".format(*args))

    with socketserver.TCPServer((host, port), CalendarHandler) as httpd:
        print("tingcal server at http://{}:{}".format(host, port), file=sys.stderr)
        httpd.serve_forever()


def main(argv=None):
    def datearg(datestr):
        return datetime.datetime.strptime(datestr, "%Y-%m")

    parser = argparse.ArgumentParser(description="create a calendar")
    parser.add_argument("startmonth", nargs=1, type=datearg, help="start month YYYY-MM")
    parser.add_argument("endmonth", nargs=1, type=datearg, help="end month YYYY-MM")
    parser.add_argument(
        "--zodiac", action="store_const", const=True, help="print zodiac signs"
    )
    parser.add_argument(
        "--lunar", action="store_const", const=True, help="print lunar phase"
    )
    parser.add_argument("--server", action="store_true", help="start web server")
    parser.add_argument(
        "--port", type=int, default=9999, help="web server port (default: 9999)"
    )

    if argv is None:
        argv = parser.parse_args()

    if argv.server:
        run_server(
            "localhost",
            argv.port,
            argv.startmonth[0],
            argv.endmonth[0],
            argv.zodiac,
            argv.lunar,
        )
    else:
        tingcal(argv.startmonth[0], argv.endmonth[0], argv.zodiac, argv.lunar)
