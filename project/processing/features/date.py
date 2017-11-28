from daterangeparser import parse
from dateutil import parser
import mwparserfromhell as mw
import re
import datetime

START_DATE = "start_date"
END_DATE = "end_date"
BC = "dates_bc"

DATE_FORMAT = "%Y-%m-%d"


def get_features(battle_json):
    if not battle_json or battle_json["infobox"].get("error"):
        return {}
    start, end, bc = get_daterange(battle_json["infobox"].get("date"))
    return {
        START_DATE: start.strftime(DATE_FORMAT) if start else None,
        END_DATE: end.strftime(DATE_FORMAT) if end else None,
        BC: bc
    }


def get_daterange(date_string):
    #returns start, end
    date = date_string
    flagBC = False
    try:
        date_string = date_string.strip()
        if re.search('^(.*\d{1})?\{',str(date_string)):
            date_string = re.search('^(.*\d{1})?\{',str(date_string)).group(1)
            date_string = date_string.strip()
        if re.search('^(.*\d{1})?\<',str(date_string)):
            date_string = re.search('^(.*\d{1})?\<',str(date_string)).group(1)
            date_string = date_string.strip()
        if re.search('^(.*\d{1})?\}',str(date_string)):
            date_string = re.search('^(.*\d{1})?\}',str(date_string)).group(1)
            date_string = date_string.strip()
        if re.search('(.*)\s\(.*\)(.*)',str(date_string)):
            date_string = re.search('(.*)\s\(.*\)(.*)',str(date_string)).group(1)+re.search('(.*)\(.*\)(.*)',str(date_string)).group(2)
            date_string = date_string.strip()
        if re.search('^(\d{1,2}|\w{3,9})(\sor|\sand|/)(.*)',str(date_string)):
            date_string = re.search('^(\d{1,2}|\w{3,9})(\sor|\sand|/)(.*)',str(date_string)).group(3)
            date_string = date_string.strip()
        if re.search('^(.*)BC',str(date_string)):
            date_string = re.search('^(.*)BC',str(date_string)).group(1)
            date_string = date_string.strip()
            flagBC = True
        try:
            date_string = mw.parse(date_string)
            date_string = date_string.strip()
            start, end = parse(date_string) 
        except:
            start = parser.parse(date_string)
            if start.year<=2066:
                start = start.replace(year=start.year-2000)
            else:
                start = start.replace(year=start.year-1900) 
            
            end = None
        return start, end, flagBC
    except:
        date_string = date
        if re.search('(\w{3,9})(.*)(\d{4})',str(date_string)):
            year = int(re.search('(\w{3,9})(.*)(\d{4})',str(date_string)).group(3))
            month = re.search('(\w{3,9})(.*)(\d{4})',str(date_string)).group(1)
            try:
                if re.search('(Spring|Winter|Autumn|Summer|Fall)',month):
                    month=1
                else:
                    month = datetime.datetime.strptime(month[:3], '%b').month
                start = datetime.date(year, month, 1)
            except:
                start = None
            end = None
            return start, end, flagBC
        if re.search('(\w{3,9})(.*)(\d{3})',str(date_string)):
            year = int(re.search('(\w{3,9})(.*)(\d{3})',str(date_string)).group(3))
            month = re.search('(\w{3,9})(.*)(\d{3})',str(date_string)).group(1)
            try:
                if re.search('(Spring|Winter|Autumn|Summer|Fall)',month):
                    month=1
                else:
                    month = datetime.datetime.strptime(month[:3], '%b').month
                start = datetime.date(year, month, 1)
            except:
                start = None
            end = None
            return start, end, flagBC
        elif re.search('(\d{3,4})',str(date_string)):
            year = int(re.search('(\d{3,4})',str(date_string)).group(1))
            try:
                start = datetime.date(year,1,1)
            except:
                start = None
            end = None
            return start, end, flagBC
        return None, None, None
