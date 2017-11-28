import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd
from features.feature_utils import print_error, get_number

def check_value(regex, ws, i):
    if re.search(regex,str(ws[i-1])) or re.search(regex,str(ws[i+1:i+2])) or re.search(regex,str(ws[i])):
        return True
    return False
    
def get_features(params):
    j = params.get('index')
    w = params.get('row')
    nbr = params.get('nbr')
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
                        #print("line ", j, ": ", w) #uncomment to see unparsed lines
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
            
            
    return {'j': j, 'missed_'+nbr : missed, 'strength_'+nbr : total, 'undefined_'+nbr : undefined}            
                
def get_strengths(df, column, nbr):
    df['undefined_'+nbr] = ""
    df['strength_'+nbr] = 0
    missed = 0
    
    thread_c = mp.cpu_count()
    pool = mp.Pool(thread_c)
    params = []
    for j,w in enumerate(column):  
        params.append({'index' : j, 'row' : w, 'nbr' : nbr})
        
    data = pool.imap_unordered(get_features, params)
    
    for i, v in enumerate(data, 1):
        index = v.get('j')
        df.loc[(index, 'strength_'+nbr)] = v['strength_'+nbr]
        df.loc[(index, 'undefined_'+nbr)] = v['undefined_'+nbr]
        missed = missed + v['missed_'+nbr]
    return missed
        