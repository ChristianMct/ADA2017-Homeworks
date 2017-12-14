import re
import calendar
import mwparserfromhell as mw
import daterangeparser as drp
import dateparser as dp
from .feature_utils import get_templates


START_DATE = "start_date"
END_DATE = "end_date"

DATE_FORMAT = "%Y-%m-%d"


def get_features(battle_json):
    if not battle_json or battle_json["infobox"].get("error"):
        return {}
    start, end = get_daterange(battle_json["infobox"].get("date", ""))

    return {
        START_DATE: start.strftime(DATE_FORMAT) if start else None,
        END_DATE: end.strftime(DATE_FORMAT) if end else None,
    }


def get_daterange(date_string):
    wt = mw.parse(date_string.strip())
    date_string_cleaned = remove_ref(replace_date(wt)).strip_code()
    return parse_date(date_string_cleaned)


def remove_ref(wikitext):
    for t in wikitext.filter():
        if t.startswith("<ref"):
            wikitext.remove(t)
    return wikitext


def replace_date(wikitext):
    for date_tpl in get_templates(wikitext, name=["start date", "end date"]):
        params = [p.value for p in filter(lambda p: p.name not in ["df", "mdy"], date_tpl.params)]
        year = str(params[0])
        month = calendar.month_name[int(str(params[1]))] if len(params) > 1 and str(params[1]).isdigit() else ""
        day = str(params[2]) if len(params) > 2 else ""
        wikitext.replace(date_tpl, "%s %s %s" % (day, month, year))

    for date_tpl in get_templates(wikitext, name=["start-date", "end-date"]):
        wikitext.replace(date_tpl, date_tpl.params[0])
    return wikitext


rangesep = re.compile("(to|until|-|–|->)")


def parse_date(date):
    if "BC" in date:
        return None, None
    date = date.split("(")[0].replace("\xa0", " ")
    if rangesep.search(date):
        try:
            return drp.parse(date)
        except:
            return None, None
    else:
        try:
            return dp.parse(date, settings={'PREFER_DAY_OF_MONTH': 'first'}), None
        except:
            return None, None
