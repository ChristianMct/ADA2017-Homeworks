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

# check around the value for an indicator of interest (e.g. killed)
def check_value(regex, ws, i):
    if re.search(regex,str(ws[i+1:i+2])) or re.search(regex+'*\:',str(ws[i-1])):
        return True
    return False

# get the information for one row, or one casualties description
def get_casualties_line(params):
    j = params.get('index')
    w = params.get('row')
    kills = 0
    kills_c = 0
    wounds = 0
    wounds_c = 0
    total = 0
    total_c = 0
    missing = 0
    missing_c = 0
    captured = 0
    captured_c = 0
    found = False
    undefined = ""
    missed = 0
    try:
        ws = w.split()
        for i,v in enumerate(ws):
            try:
                number = get_number(v)
                if number is not None:
                    if len(ws) == 1:
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
                        elif check_value('[cC]asualt', ws, i) or check_value('[tT]otal', ws, i) or check_value('[mM]en',ws, i): 
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
                        print("line ", j, ": ", w)
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
        if total == 0:
            total = kills + wounds + missing + captured
            
    except Exception as e:
        if not pd.isnull(w): #if not nan, we indicate the error and count it as a parsing fail
            print_error()
            undefined = undefined + str(ws)
            missed = missed + 1
            print("line ", j, ": ", w)
            
    return {'j': j, 'missed': missed, 'kills' : kills, 'wounds' : wounds, 'missing' : missing, 'captured' : captured, 'total' : total, 'undefined' : undefined}            
                
def get_casualties(df, column, nbr):
    df['kills_'+nbr] = 0
    df['wounds_'+nbr] = 0
    df['missing_'+nbr] = 0
    df['undefined_'+nbr] = ""
    df['captured_'+nbr] = 0
    df['total_'+nbr] = 0
    missed = 0
    
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    params = []
    for j,w in enumerate(column):  
        params.append({'index' : j, 'row' : w})
        
    data = pool.imap_unordered(get_casualties_line, params)
    
    for i, v in enumerate(data, 1):
        try:
            index = v.get('j')
            df.loc[(index, 'kills_'+nbr)] = v['kills']
            df.loc[(index, 'wounds_'+nbr)] = v['wounds']
            df.loc[(index, 'total_'+nbr)] = v['total']
            df.loc[(index, 'missing_'+nbr)] = v['missing']
            df.loc[(index, 'captured_'+nbr)] = v['captured']
            df.loc[(index, 'undefined_'+nbr)] = v['undefined']
            missed = missed + v['missed']
        except Exception as e:
            print_error()
            print("error at ", v)
    return missed
        