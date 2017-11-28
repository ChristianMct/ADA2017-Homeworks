import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd
from features.feature_utils import print_error, get_number

STRENGTH_FIRST = ["strength_1", "strength_2", "strength_3"]
FEATURE = "strength"

def check_value(regex, ws, i):
    if re.search(regex,str(ws[i-1])) or re.search(regex,str(ws[i+1:i+2])) or re.search(regex,str(ws[i])):
        return True
    return False
    
def get_features_line(row):
    total = 0
    total_c = 0
    men = 0
    men_c = 0
    fromTo = 0
    fromTo_c = 0
    found = False
    undefined = ""
    missed = 0
    try:
        ws = row.split()
        for i,v in enumerate(ws):
            try:
                number = get_number(v)
                if (not found) and (number is not None):
                    if len(ws) == 1:
                        total = total + number
                        total_c = total_c+1
                        found = True
                    elif not (i == len(ws)-1):
                        if check_value('[tT]otal',ws, i) or check_value('[Aa]pprox',ws, i) or check_value('[eE]stim',ws, i) or check_value('[mM]en',ws, i) or check_value('[Pp]erson', ws, i) or check_value('[Vv]erbru', ws, i):
                            total = total + number
                            total_c = total_c + 1
                            found = True
                        elif check_value('[cC]aval',ws, i) or check_value('[Ll]egio', ws, i) or check_value('[tT]roop', ws, i) or check_value('[Mm]ercenar', ws, i) or check_value('[Ii]nfant', ws, i): 
                            men = men + number
                            men_c = men_c + 1
                        elif check_value('[fF]rom', ws, i) or check_value('[tT]o', ws, i):
                            fromTo = fromTo + number
                            fromTo_c = fromTo_c + 1  
                        else:
                            undefined = undefined + " " + str(v)
                            
            except Exception as e:
                print_error()
            
            
        if (not found) and (men == 0) and (fromTo == 0):
            try:
                number = get_number(ws[0:3]) #try with first position as it seems to be often the case
                if number is not None:
                    total = total + number
                    total_c = total_c + 1
                    found = True
            except Exception as e:
                print_error()
                undefined = undefined + " " + str(v)
            
            if not found:
                try:
                    number = get_number(ws)
                    if number is not None:
                        missed = missed + 1
                        #print("line ", j, ": ", w) #uncomment to see unparsed lines
                except Exception as e:
                    print_error()
                    undefined = undefined + " " + str(v)
                                                  
        if total == 0 or fromTo_c > 1:
            total = men 
            if fromTo_c > 1:
                total = total + int(fromTo/fromTo_c)
    except Exception as e:
        if not pd.isnull(row):
            print_error()
            undefined = undefined + str(ws)
            missed = missed + 1
            print("line ", j, ": ", row)
            
            
    return {FEATURE : total}            
                
def get_features(battle_json):
    if not battle_json or battle_json["infobox"].get("error"):
        return {}
    
    values = dict()
    values.update({STRENGTH_FIRST[i-1] : get_features_line(battle_json["infobox"].get("strength%s" % i)).get(FEATURE) for i in range(1,len(STRENGTH_FIRST)+1)})
    
    return values
        