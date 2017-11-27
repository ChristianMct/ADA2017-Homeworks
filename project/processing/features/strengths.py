import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd


def print_error():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

    
def get_number(string):
    number = -1
    rangeNbr = False
    if re.search("\d+(?:\,\d+)[–,-]\d+(?:\,\d+)?",str(string)):
        tmp = re.search("\d+(?:\,\d+)?[–,-]\d+(?:\,\d+)?",str(string)).group().replace(",","")
        tmps = tmp.split('–')
        rangeNbr = True
        if not len(tmps)== 2:
            tmps = tmp.split('-')
            if not len(tmps)== 2:
                rangeNbr = False
        if rangeNbr:
            number = int((int(tmps[0])+int(tmps[1]))/2)
    if (not rangeNbr) and re.search("[+-]?\d+(?:\,\d+)?",str(string)):
        number = int(re.search("[+-]?\d+(?:\,\d+)?",str(string)).group().replace(",",""))
    if (number >= 0) and (number < 10000000): 
            return number
    else :
        return None

def check_value(regex, ws, i):
    if re.search(regex,str(ws[i-1])) or re.search(regex,str(ws[i+1:i+2])) or re.search(regex,str(ws[i])):
        return True
    return False
    
def get_strengths_line(params):
    j = params.get('index')
    w = params.get('row')
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
        ws = w.split()
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
                        print("line ", j, ": ", w)
                except Exception as e:
                    print_error()
                    undefined = undefined + " " + str(v)
                                                  
        if total == 0:
            total = men 
            if fromTo_c > 1:
                total = total + int(fromTo/fromTo_c)
    except Exception as e:
        if not pd.isnull(w):
            print_error()
            undefined = undefined + str(ws)
            missed = missed + 1
            print("line ", j, ": ", w)
            
            
    return {'j': j, 'missed' : missed, 'total': total, 'undefined' : undefined}            
                
def get_strengths(df, column, nbr):
    df['undefined_'+nbr] = ""
    df['total_'+nbr] = 0
    missed = 0
    
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    params = []
    for j,w in enumerate(column):  
        params.append({'index' : j, 'row' : w})
        
    data = pool.imap_unordered(get_strengths_line, params)
    
    for i, v in enumerate(data, 1):
        index = v.get('j')
        df.loc[(index, 'total_'+nbr)] = v['total']
        df.loc[(index, 'undefined_'+nbr)] = v['undefined']
        missed = missed + v['missed']
    return missed
        