from daterangeparser import parse
from dateutil import parser
import mwparserfromhell as mw
import re
import datetime

def get_daterange(date_string):
    #returns start, end
    date = date_string
    try:
        flagBC=("no")
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
            flagBC=("yes")
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
            
            end = ("None")
        return {"start": start, "end":end, "source":date_string, "BC":flagBC}
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
                start = ("None")
            end = ("None")
            return {"start": start, "end":end, "source":date_string, "BC":flagBC}
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
                start = ("None")
            end = ("None")
            return {"start": start, "end":end, "source":date_string, "BC":flagBC}
        elif re.search('(\d{3,4})',str(date_string)):
            year = int(re.search('(\d{3,4})',str(date_string)).group(1))
            try:
                start = datetime.date(year,1,1)
            except:
                start = ("None")
            end = ("None")
            return {"start": start, "end":end, "source":date_string, "BC":flagBC}
        return {"source":date_string}
