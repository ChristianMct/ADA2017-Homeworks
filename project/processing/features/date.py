from daterangeparser import parse

def get_daterange(date_string):
    #returns start, end
    date_string = date_string.strip()
    try:
        start, end = parse(date_string)
        return {"start": start, "end":end, "source":date_string}
    except:
        return {"source":date_string}
