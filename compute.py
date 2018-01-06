# to reload import importlib; importlib.reload(c)

import pandas as pd
pd.set_option('display.max_colwidth', -1)  # don't truncate lines in print x.to_html() https://stack….com/q…s/26277757/
import numpy as np
from functools import reduce
import itertools as i #import chain, combinations, product

from compute.lang_table   import lang_dict, code_to_language
from compute.preparetable import get_table

from compute import frequency as freq
from compute import compute_langs as cl
from compute import rankings as rank
from compute import graphs as g

import pickle

'''todo - es gibt noch ein paar einträge im haskell projekt
        - filter freq by language e.g. when do people want to learn english
'''
### frequency ###

def print_supply_vs_demand_stats(path, table, printfnc):
    write = printfnc
    (supplies_x_demand, (want_more,same,offer_more), (e_want,e_offer)) = cl.number_of_offer(table)

    #demand_by_supplies = a.values.tolist() # d_b_s[0] is the demands for supply=0
    #supplies_by_demand = a.values.transpose().tolist()

    write("var lang_tablecontent = \'" + supplies_x_demand.to_html().replace('\n','\\n') + "\'")

    write('var lang_want_more = %s' % want_more)
    write('var lang_same = %s' % same)
    write('var lang_offer_more = %s' % offer_more)

    write('var lang_expected_demand = %.2f' % e_want)
    write('var lang_expected_supply = %.2f' % e_offer)


def who_wants_what(table):
    df = pd.DataFrame({'demand':table.searching_reduced,
                       'supplies':table.offering_reduced})
    #a.index.get_values() #columns
    a = pd.crosstab(df.supplies, df.demand)

#def print_sparse_crosstab(df): zum bearbeiten vllt aber nicht zum veröffentlichen
def print_pairs_table(table, func):
    write=func

    def explicify(ct):
        print(ct.index[-1])
        ct.index = ct.index[:-1].map(code_to_language).insert(len(ct.index), ct.index[-1])
        return ct
        
    ct_search = explicify(g.get_crosstab_from_within_old(table.searching_reduced)) #.... crosstab
    ct_offer  = explicify(g.get_crosstab_from_within_old(table. offering_reduced))
    #TODO convert index
    write("var pairs_crosstab_intra_search = \'" + ct_search.to_html().replace('\n','\\n') + "\'")
    write("var pairs_crosstab_intra_offer  = \'" + ct_offer .to_html().replace('\n','\\n') + "\'")


### languages
expand_langs = lambda s: pd.Series(s.values, index=map(code_to_language, s.index)) #takes count series, returns new series with expanded lang

def pairs_so(table):
    tuples_of_lists = zip(table.searching_reduced, table.offering_reduced) # [([],[])]
    
    lists_of_tuples = map(lambda tup: list(i.product(*tup)), tuples_of_lists) # [[(s,o)] ]

    flat = list(i.chain.from_iterable(lists_of_tuples))
    flat_smmetric = [tuple(sorted(tup)) for tup in flat]

    directional_counts = pd.Series(flat).value_counts()
    symmetric_counts   = pd.Series(flat_smmetric).value_counts()

    return directional_counts, symmetric_counts

def pairs1(table):
    def pairs(col):
        listChoose2 = lambda l: i.combinations(l+['just_that'],2) # we've already computed total of lang -> 'just that' may be unneccessary
        col_of_2s = col.map(listChoose2)
        return pd.Series(sorted( i.chain.from_iterable( col_of_2s ) )).value_counts()

    return [pairs(c) for c in (table.searching_reduced, table.offering_reduced)]


def print_pairs_within(table,printfunc):
    out = g.print_pairs_within_to_d3(table)
    printfunc(out)


def time_diff2str(diff):
    diff_between_entries = ''
    val=[diff.days, diff.seconds // 3600, (diff.seconds % 3600) // 60, (diff.seconds % 3600) % 60]
    str=['days', 'hours', 'minutes', 'seconds']
    strings = ["%s %s" % (v,s) for v,s in zip(val,str) if v > 0]
    return ', '.join(strings[:-1])+ ' and '+ strings[-1]


def print_freqs(path, dates, printfnc):
    write = printfnc

    #pretext, how many entries, how many per day, intervall
    hits, diff, no_entries, (start, end) = freq.frequency(dates)
    write("var no_valid_entries = %s" % no_entries)
    write("var hits_per_day = %.2f" % hits)
    write("var time_between_hits = '%s'" % time_diff2str(diff))

    write("var from = \"{}\"".format(start))
    write("var to   = \"{}\"".format(end))
    
    #compare frequency by day of week #
    counts_dow_df, pval  = freq.count_by_day_of_week(dates)
    counts_dow = counts_dow_df.values
    write("var week_day_all = %s" % ['%.2f' % el for el in list(counts_dow)])
    write("var p_val = {:.3f}".format(pval))
    #TODO also by japanese and swedish, maybe by most numerous country

    #compare frequency by days of the year TODO normalize for days we've seen more than once
    counts_doy = freq.count_by_day_of_year(dates)
    first, last = map(lambda x: (pd.Timestamp(counts_doy.index[x]) - pd.Timestamp("2016-01-01")).days, (0,-1))
    all_dates = [pd.Timestamp("2016-01-01") + pd.DateOffset(days=i) for i in range(first, last+1)]
    all_date_strings =  [d.strftime('%Y-%m-%d') for d in all_dates]

    all_values    = [0 if date not in counts_doy.index else counts_doy.freq[date]    for date in all_dates]
    all_values_s7 = [0 if date not in counts_doy.index else counts_doy.freq_s7[date] for date in all_dates]
    doy_ticks = [d.strftime('%Y-%m-%d') for d in all_dates if d.day is 1]
    ty_strings    = ("{t: '%s', y: %s}" % (d,v) for d,v in zip(all_date_strings, all_values))
    ty_strings_s7 = ("{t: '%s', y: %s}" % (d,v) for d,v in zip(all_date_strings, all_values_s7))
    write("var doy_data    = [%s]" % ','.join(ty_strings))
    write("var doy_data_s7 = [%s]" % ','.join(ty_strings_s7)) #smoothed by 7 days (±3)
    write("var doy_labels= %s" % doy_ticks )

def print_remaining_demand(search_counts, offer_counts, printfnc):
    write = printfnc
    df=pd.DataFrame({'demand'  :search_counts,
                     'supplies': offer_counts})
    df=df.fillna(0)
    remainingDemand = df['demand'] - df['supplies']
    remainingDemand = remainingDemand.sort_values(ascending=False)
    remaining_demand = remainingDemand[remainingDemand > 0]
    remaining_supply = remainingDemand[remainingDemand < 0].abs().sort_values(ascending=False)
    remaining_same   = remainingDemand[remainingDemand == 0].index.tolist()

    for series, name in ((remaining_demand, 'dem'),(remaining_supply,'sup')):
        content = _print_2_col_table(series.index, map(int,series.values))
        write("var table_remaining_"+name+" = \'" + content + "\'")

    list2str = lambda l : ', '.join(l[:-2] + [' and '.join(l[-2:])])
    
    write("var str_remaining_same = '%s'" % list2str(remaining_same))
    
def print_language_rankings(table, printfnc):
    write = printfnc
    _write_lang_ranking(write, table, rank.count_all_langs,   'overall')
    _write_lang_ranking(write, table, rank.count_first_langs, 'first')
    _write_lang_ranking(write, table, rank.count_other_langs, 'additional')
    _write_lang_ranking(write, table, rank.count_last_langs,  'last')

    
def _write_lang_ranking(write, table, filter, varname):
    d,s = filter(table.searching_reduced, table.offering_reduced)
    for series, name in ((d, 'dem'),(s,'sup')):
        content = _print_2_col_table(map(code_to_language,series.index), map(int,series.values))
        write("var table_" + varname + "_"+name+" = \'" + content + "\'")


        
def main(path='website/data.js'):
    f = open(path, 'w')
    table = get_table()
    write = lambda x : print(x, file=f)
    
    dates = table.date
    print_freqs(path, dates, write)
    print_supply_vs_demand_stats(path, table, write)
    
    (search_counts, offer_counts) = rank.count_langs(table.searching_reduced, table.offering_reduced)    
    (search_counts, offer_counts) = map(expand_langs, (search_counts, offer_counts))
    
    write("var search_labels = %s" % list(search_counts.index))
    write("var search_values = %s\n" % list(search_counts.values))
    
    write("var offer_labels = %s" % list(offer_counts.index))
    write("var offer_values = %s\n" % list(offer_counts.values))
    
    print_remaining_demand(search_counts, offer_counts, write)

    print_language_rankings(table, write)
    
    print_pairs_within(table, write)
    print_pairs_table(table, write)
    print_offer_also_offers(table, write)
    
    f.close()
    
###########
def print_offer_also_offers(table, writefunc):
    write = writefunc
    pt = g.offer_also_offers(table.offering_reduced)
    
    ppt = pt.reset_index()
    #ppt.to_pickle('computed')

    def df_to_str(group):
        l1 = group.iloc[:,1].tolist()
        col2 = group.iloc[:,2]
        col2 = (col2 / col2.sum()*100).astype(int)
        l2 = col2.tolist()
        tail = ', '.join("{}_{}%".format(a,b) for a,b in zip(l1,l2) if b >= 2) #filter out 1% or 0%
        return tail

    total = lambda group : group.iloc[:,2].sum()
    
    a =list( (name, total(group), df_to_str(group)) for name, group in ppt.groupby('from', sort=False))
    names, totals, tails = zip(* a  )
    
    out =   pd.DataFrame({'lang':names,
                          'total':totals,
                          'partners':tails})
    
    out = out[out.total >= 2]
    out = out[['lang', 'total', 'partners']]

    s=out.to_html(index=False,justify='left' )
    pickle.dump(s,open('htmlled','wb'))

    cellspacing = dict( props=[ ('border-collapse', 'separate'),      #cellspacing https://stackoverflow.com/a/5667535/3014199
                                ('border-spacing',  '10px 5px') ] )
    hide_index =       {'selector': '.row_heading',  'props': [('display', 'none')]} #style.hide_index()\ from 0.23 on
    hide_corner_cell = {'selector': '.blank.level0', 'props': [('display', 'none')]}
    styles = [ cellspacing, hide_index, hide_corner_cell ]

    html_pretty = out.style.set_properties(subset=out.columns[[1]],   **{'text-align':'right'})\
                           .set_properties(subset=out.columns[[0,2]], **{'text-align':'left'})\
                           .set_table_styles(styles)
    
    write("var pairs_list_offer_offer = \'" + html_pretty.render().replace('\n','\\n') + "\'")
    
#ct.index  = ct.index[:-1].map(code_to_language).insert(len(ct.index), ct.index[-1])

#TODO convert index
#write("var pairs_crosstab_intra_search = \'" + ct_search.to_html().replace('\n','\\n') + "\'")
#write("var pairs_crosstab_intra_offer  = \'" + ct_offer .to_html().replace('\n','\\n') + "\'")

#####
    
def _print_2_col_table(col1, col2):
    indices, values = list(col1),list(col2)
    toRow = lambda l,v : '<tr><td class="alignleft">%s</td><td class="alignright">%s</td></tr>' % (l,v)
    content = '\\n'.join(toRow(l,v) for l,v in zip(indices, values))
    return content
    

if __name__ == "__main__":
    main()
