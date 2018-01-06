import pandas as pd
import numpy as np

def number_of_offer(table):
    
    df=pd.DataFrame({'demand':table.searching_reduced.map(len),
                     'supplies':table.offering_reduced.map(len)})

    #df.supplies.value_counts(),...
    #    offer more than supply
    
    a_m = pd.crosstab(df.supplies, df.demand, margins=True) #-> 4x4 matrix, supplies as rows -> 1st row: supply 1
    a = a_m.iloc[:-1,:-1]
    tb_u=np.triu(np.ones(a.shape), 1).astype(np.bool)   #upper triangle true -> keep
    tb_l=np.tril(np.ones(a.shape),-1).astype(np.bool)   #lower
   
    want_more  = a.where(tb_u).fillna(0).values.sum() #want more than they offer
    offer_more = a.where(tb_l).fillna(0).values.sum() #offer more than the want

    same = np.trace(a) # want as much as they offer

    
    #all_smaller = lambda aa,bb : all(a<b for a,b in zip(aa, bb))
    if a.shape != (4, 4):
        print('carefull! for number_of_offer we no longer have 4x4')

    e_dem,e_sup = _expected(a_m)
        
    return (a_m,(want_more,same,offer_more),(e_dem,e_sup))

def _expected(crosstab):
    demand = crosstab.iloc[-1,:-1].values
    supply = crosstab.iloc[:-1,-1].values
    
    indices = crosstab.index.get_values()[:-1].tolist()
    e_dem,e_sup = [np.average(indices,weights=x) for x in (demand, supply)]
    return e_dem,e_sup
