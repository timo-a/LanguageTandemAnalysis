import pandas as pd
import numpy as np
import itertools as i #import chain, combinations, product


def print_pairs_within_to_dot(table):
    [s,o] = pairs_within(table)
    template="""var graphs = {{\n    "within_search": "{wi_s}",\n    "within_offer": "{wi_o}"\n}}"""
    out = template.format(wi_s=_print_pairs_within_to_dot(s),
                          wi_o=_print_pairs_within_to_dot(o))
    return out

def _print_pairs_within_to_dot(col):#values
    #print(col)
    #print(type(col))
    
    l_item = lambda a,b,c : "{} -- {}[label=\"{}\"];".format(a,b,c)
    
    l_items= [l_item(a,b,c) for (a,b),c in col.iteritems()]
    links = '\n'.join(l_items)
    out = 'graph {{\n{links}\n}}'.format(links=links)
    return out


def print_pairs_within_to_d3(table):
    [s,o] = pairs_within(table)
    template="""var graphs = {{ "within_search": {wi_s},\n "within_offer": {wi_o} }}"""
    out = template.format(wi_s=_print_pairs_within_to_d3(s),
                          wi_o=_print_pairs_within_to_d3(o))
    return out


def _print_pairs_within_to_d3(col):#values
    print(col)
    print(type(col))
    nodes_raw = sorted(set(i.chain.from_iterable(col.index))) #['bul','eng',...]
    n_items = ["{{name: '{name}'}}".format(name=x) for x in nodes_raw]
    nodes = "[{}]".format(',\n'.join(n_items))
    
    l_item = lambda a,b,c : "{{source: '{}', target: '{}', value: {}}}".format(a,b,c)
    l_items= [l_item(a,b,c) for (a,b),c in col.iteritems()]
    links = "[{}]".format(',\n'.join(l_items))
    out = '{{\n "nodes": {nodes},\n "links": {links} \n}}'.format(nodes=nodes, links=links)
    return out

def pairs_within(table): #people looking for x were also looking for y

    return [pairs(c) for c in (table.searching_reduced, table.offering_reduced)]

def pairs(col):
    two_and_more = col.where(lambda x: x.map(len)>1).dropna()
    listChoose2 = lambda l : i.combinations(sorted(l),2)       #sorted so we dont get eng -> ger and ger -> eng
    col_of_2s = two_and_more.map(listChoose2)
    return pd.Series(sorted( i.chain.from_iterable( col_of_2s ) )).value_counts()


def get_crosstab_from_within(series):
    two_and_more = series.where(lambda x: x.map(len)>1).dropna()
    listChoose2  = lambda l : i.permutations(l,2)
    col_of_2s = two_and_more.map(listChoose2)
    l = list(i.chain.from_iterable( col_of_2s ))
    f,t = zip(*l)
    df = pd.DataFrame({'from':f,'to':t})
    return df #pd.crosstab(df['from'], df.to, margins=True)

def get_crosstab_from_within_old(series):#legacyyy!
    df = get_crosstab_from_within(series)
    return pd.crosstab(df['from'], df.to, margins=True)

def get_crosstab_from_interaction(series_from, series_to):
    f,t = map(i.chain.from_iterable, (zip(*i.product(a,b)) for a,b in zip(series_from, series_to)))
    
    df = pd.DataFrame({'from':f,'to':t})
    return pd.crosstab(df['from'], df.to, margins=True)

def offer_also_offers(series):#table.searching_reduced
    df = get_crosstab_from_within(series)
        
    df['number'] = df.iloc[:,0].map(lambda _:1) #add col of '1's to count combinations
    
    #group by from, sort by number
    #https://stackoverflow.com/questions/47984547/sort-a-2-index-pivot-table-values-within-group-index-based-on-values/47984755#47984755
    pt = pd.pivot_table(df, index=['from','to'], values = 'number', aggfunc=np.sum)
    #pt = pd.pivot_table(df, index = ['col1', 'col2'], values = 'col3', aggfunc = np.sum)
    pt['New'] =pt.groupby(level='from')['number'].transform('max')
    pt['New1']=pt.groupby(level='from')['number'].ngroup() #group number to combat same values in 'New'
    pt=pt.sort_values(['New','New1','number'],ascending=False)
    pt=pt.drop('New',1).drop('New1',1)
    #print(pt)
    return pt
