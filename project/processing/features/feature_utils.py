import re
import multiprocessing as mp
import json
import sys, os
import pandas as pd


# Checks if string can be converted to a floating point value
def isfloat(param):
    try:
        float(str(param))
        return True
    except ValueError:
        return False


# Print the error, line and information
def print_error():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def remove_ref(wikitext):
    for t in wikitext.filter():
        if t.startswith("<ref"):
            wikitext.remove(t)
    return wikitext


def get_templates(tree, name):
    return [t for t in tree.filter_templates() if t.name.matches(name)]
