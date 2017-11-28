import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd

# Print the error, line and information
def print_error():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

# Retrieve a number or a number range
def get_number(string):
    rangeNbr = False
    number = -1
    if re.search("\d+(?:\,\d+)[–,-]\d+(?:\,\d+)?",str(string)):
        tmp = re.search("\d+(?:\,\d+)?[–,-]\d+(?:\,\d+)?",str(string)).group().replace(",","")
        tmps = tmp.split('–') #not a usual "-" in most cases
        rangeNbr = True
        if not len(tmps)== 2: #if the split doesn't work, we try with usual "-"
            tmps = tmp.split('-')
            if not (len(tmps)== 2):
                rangeNbr = False #if the split fail, we still try to retrieve one number
        if rangeNbr:
            number = int((int(tmps[0])+int(tmps[1]))/2) #if split succeed then we do the average
    if (not rangeNbr) and re.search("[+-]?\d+(?:\,\d+)?",str(string)):
        number = int(re.search("[+-]?\d+(?:\,\d+)?",str(string)).group().replace(",",""))
    if number >= 0 and number < 10000000: 
            return number
    else :
        return None
        