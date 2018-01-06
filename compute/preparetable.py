import pandas as pd
import re
from ast import literal_eval
from compute.lang_table import lang_dict, code_to_language
import itertools as i #import chain, combinations, product

def fix_table(table):
    if table.loc[146,'searching']=='Englisch C1 / C2':
        table.loc[146,'searching']='Englisch (C1 / C2)'
    else:
        raise ValueError('table[\'searching\'][146] is '+table['searching'][146]+' but expected is \'englisch C1 / C2\'')

    if table.loc[426,'searching']=='Brasilianisches Portugiesisch':
        table.loc[426,'searching']=                'Portugiesisch'
    else:
        raise ValueError('table[\'searching\'][426] is '+table['searching'][426]+' but expected is \'Brasilianisches Portugiesisch\'')


def reduce_langs(table):
    table['searching_reduced'] = table.searching.map(_reduce_to_code)
    table[ 'offering_reduced'] = table.offering.map(_reduce_to_code)

_reduce_to_code = lambda l: [e[:3] for e in l] # str -> []


def _fix_langs(language_str): #str -> [str]
    """  convert offer/search string into list of strings that start with language-iso3? code """
    
    if type(language_str) is not str:
        raise ValueError("should be str, but is %s" % type(language_str))
    
    language_str = re.sub("(?<! )\(", " (", language_str) # if there is a '(' with no space before it, insert one
    for mu_spra in ['Muttersprache', '(Muttersprache)', '(Muttersprachler)', '(Mother tongue)', '(μ)']:
        language_str = language_str.replace(mu_spra,'μ')
    
    elements = _split_on_outer(language_str) # split on , / but not inside parenthesis
    def shorten_element(e):#shorten language e.g. "Englisch aber nicht so gut" -> "eng aber nicht so gut"
        e=e.strip()
        for k in lang_dict.keys():
            if e.split()[0] == k:
                e=e.replace(k,lang_dict[k])
                break
        return e

    return list(map(shorten_element, elements))

def _split_on_outer(string):#split on ,/ but not inside parenthesis
    for p in re.compile("\([^(]*\)").findall(string):
        new_p = p.replace(',',';').replace('/',';')
        string = string.replace(p,new_p)
        
    elements = re.compile("[/,]").split(string)
    return elements



def get_table():
    table = pd.read_table('data.table', sep=';', parse_dates=[1])
    table = table[table.date.notnull()] # filter out all removed entries (id;;;;;)
    
    fix_table(table)

    table['searching']=table.searching.apply(_fix_langs)
    table['offering'] =table.offering.apply(_fix_langs)
    
    reduce_langs(table) #add searching_reduced

    return table
