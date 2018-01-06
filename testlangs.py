import pandas as pd
from preparetable import get_table
from lang_table import lang_table, lang_dict, code_to_language
from functools import reduce

def show_what_remains(col, verbose=True):
    shortened = col #.map(_fix_langs)# there .apply(literal_eval)
    
    known_taken_out = ([[l for l in entry if l            not in lang_dict.values()] for entry in shortened] if verbose 
                  else [[l for l in entry if l.split()[0] not in lang_dict.values()] for entry in shortened])
    filtered = list(filter(lambda x: len(x)>0, known_taken_out))
    strings = map(lambda listi:reduce(lambda a,b: a+'+'+b,listi), filtered)
    uniques = set(strings)
    return uniques


def main():
    table = get_table()
    non_trivials =  show_what_remains(pd.concat([table.searching, table.offering]))
    unknowns     =  show_what_remains(pd.concat([table.searching, table.offering]), verbose=False)
    print("non trivial language lables: %s" % non_trivials)
    print("unknown language lables: %s" % unknowns)



if __name__ == "__main__":
    main()
