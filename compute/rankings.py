import pandas as pd
import itertools as i

count_all_langs   = lambda searchS, offerS: count_langs_generic(searchS, offerS, lambda x: x)

count_first_langs = lambda searchS, offerS: count_langs_generic(searchS, offerS, lambda x: x[:1])

count_other_langs = lambda searchS, offerS: count_langs_generic(searchS, offerS, lambda x: x[1:])

count_last_langs  = lambda searchS, offerS: count_langs_generic(searchS, offerS, lambda x: x[-1:] if len(x) > 1 else [])

count_langs_generic = lambda searchS, offerS, fun: count_langs(searchS.map(fun), offerS.map(fun))

def count_langs(searchS, offerS):
    return (count_lang(searchS), count_lang(offerS))

def count_lang(series):
    return pd.Series(list(i.chain.from_iterable(series.values))).value_counts()
