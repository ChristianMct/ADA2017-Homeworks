import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd
from features.feature_utils import print_error, get_number

CASUALTY_FIRST = [" casualties_1", "casualties_2", "casualties_3", "casualties_4"]
FEATURE_LIST = ["killed", "wounded", "missing", "captured", "casualties"]

# check around the value for an indicator of interest (e.g. killed)
def check_value(regex, ws, i):
    if re.search(regex,str(ws[i+1:i+2])) or re.search(regex+'.{0,5}\:',str(ws[i-1])):
        return True
    return False

# get the information for one row, or one casualties description
def get_features_line(row):
    kills = 0
    kills_c = 0
    wounds = 0
    wounds_c = 0
    total = 0
    total_c = 0
    totalAll = 0
    missing = 0
    missing_c = 0
    captured = 0
    captured_c = 0
    found = False
    undefined = ""
    missed = 0
    try:
        ws = row.split()
        for i,v in enumerate(ws):
            try:
                number = get_number(v)
                if number is not None:
                    if re.search("\'\'\'.{0,20}\'\'\'", str(v)):
                        totalAll = number
                        found = True
                    elif len(ws) == 1:
                        total = total + number
                        total_c = total_c+1
                        found = True
                    elif not (i == len(ws)-1):
                        if check_value('[kK]ill',ws, i) or check_value('[Dd]ead', ws, i) or check_value('[Dd]ie', ws, i):
                            kills = kills + number
                            kills_c = kills_c + 1
                            found = True
                        elif check_value('[wW]ounded',ws, i) or check_value('[iI]njur', ws, i): 
                            wounds = wounds + number
                            wounds_c = wounds_c + 1
                            found = True
                        elif check_value('[cC]asualt', ws, i) or check_value('[t]otal', ws, i) or check_value('[mM]en',ws, i): 
                            if re.search('Total.{0,5}\:',str(ws[i-1])):
                                totalAll = number
                            else:             
                                total = total + number
                                total_c = total_c + 1
                            found = True
                        elif check_value('[mM]issing', ws, i):
                            missing = missing + number
                            missing_c = missing_c + 1
                            found = True
                        elif check_value('[cC]aptur', ws, i) or check_value('[Pp]rison', ws, i): 
                            captured = captured + number
                            captured_c = captured_c + 1
                            found = True
                        else:
                            undefined = undefined + " " + str(v)
            except Exception as e:
                print_error()
                
                
        if not found:
            try:
                number = get_number(ws[0:3]) #try with first position as it seems to be often the case
                if number is not None:
                    total = total + number
                    total_c = total_c + 1
                    found = True
            except Exception as e:
                print_error()
                undefined = undefined + " " + str(v)
            
            if not found: #if still not found, we check in the whole line, if there is a number we count it as a failed parse
                try:
                    number = get_number(ws)
                    if number is not None:
                        missed = missed + 1
                        #print("line ", j, ": ", w) #uncomment to see unparsed lines
                except Exception as e:
                    print_error()
                    undefined = undefined + " " + str(v)
        
        # if the text contains one of these keywords, there is a high probability that it contains number from multiple sources
        # we then divide by the number of appearances for kills, ...
        if re.search('sources',str(ws)) or re.search('estimate',str(ws)) or re.search('per',str(ws)):
            if not kills_c == 0:
                kills = int(kills/kills_c)
            if not wounds_c == 0:
                wounds = int(wounds/wounds_c)
            if not missing_c == 0:
                missing = int(missing/missing_c)
            if not captured_c == 0:
                captured = int(captured/captured_c)
            if not total_c == 0:
                total = int(total/total_c)
            
        # if we didn't find a total estimation we create it from the other information                                         
        if not totalAll == 0:
            total = totalAll
        elif total == 0:
            total = kills + wounds + missing + captured
            
    except Exception as e:
        if not pd.isnull(row): #if not nan, we indicate the error and count it as a parsing fail
            print_error()
            undefined = undefined + str(ws)
            missed = missed + 1
            print("line ", j, ": ", w)
    
    #print("line containing a number but cannot be parsed : ", missed)
    return {FEATURE_LIST[0] : kills, FEATURE_LIST[1] : wounds, FEATURE_LIST[2] : missing, FEATURE_LIST[3] : captured, FEATURE_LIST[4] : total}            
                

def get_features(battle_json):
    if not battle_json or battle_json["infobox"].get("error"):
        return {}
    
    values = dict()
    values.update({CASUALTY_FIRST[i-1] : get_features_line(battle_json["infobox"].get("casualties%s" % i)) for i in range(1,len(CASUALTY_FIRST)+1)})
    
    values_final = dict()
    for n in range(1, len(CASUALTY_FIRST)+1):
         for i in range(1,len(FEATURE_LIST)+1):
            values_final.update({FEATURE_LIST[i-1]+"_"+str(n) : values.get(CASUALTY_FIRST[n-1]).get(FEATURE_LIST[i-1])})
   
    return values_final
        