import pandas as pd
from scipy.stats.mstats import chisquare

def frequency(dates):
    """
        takes series of dates
        returns (av entries per day, av time between entries)

    """
    no_entries = int(dates.count())

    #return '8'
    first=dates.iat[0]
    last =dates.iat[-1]
    av_diff = (last - first+ pd.Timedelta('1 days')) / no_entries    # av no entries a day
    av_per_day = pd.Timedelta('1 days') / av_diff # 
    #print("av", type(av_diff))

    from_to = (first.strftime('%Y-%m-%d'),
                last.strftime('%Y-%m-%d'))
    
    return (av_per_day, av_diff.round('s'), no_entries, from_to)

def count_by_day_of_week(dates):
    """ takes a series of dates
        returns a series grouping by day of the week
        e.g.   (day_of_week, count)
                0 123
                1 2
                2 8
                3 2
                4 322
                5 9
                6 1
    """ # carefull!!! 0tage nicht vergessen
    by_day = pd.DataFrame(dates.value_counts())
    by_day.columns = ['entries']
    by_day['day'] = by_day.index.map(lambda x: x.weekday())
    mean_per_day = by_day['entries'].groupby(by_day['day']).mean()
    per_weekday  = by_day['entries'].groupby(by_day['day']).sum()
    #chi square

    df = pd.DataFrame({'hits':per_weekday,
                       'dfreq':_get_adj_freqs(dates) })
    
    
    df['adjusted_expectation'] = df.dfreq.map(lambda x: x * df.hits.sum() / df.dfreq.sum())
    p = chisquare(df.hits, df.adjusted_expectation).pvalue
    
    return mean_per_day,p

def _get_adj_freqs(dates):#
    first=dates.iat[0]  #.weekday()
    last =dates.iat[-1] #.weekday()
    span = (last - first).days + 1
    freqs = [span // 7] * 7
    oneMoreSpan =  range(span % 7)
    for o in oneMoreSpan:
        i = (first.weekday() + o) % 7
        freqs[i] += 1
    return freqs


def count_by_day_of_year(dates):
    #Todo we still need to normalize by years: if we observe from april 2017 to may 2018, we'll have a jump in april
    # idea do a count, add column 'actual year'
    # map index to 2016
    # count again, somehow count the different years
    #NO! just do it aswith the weekdays
    year_to_2016 = lambda x: x - pd.DateOffset(years=(x.year - 2016)) #normalize to leap year, so feb 29th is there
    normalized = dates.map(year_to_2016)

    counts = normalized.value_counts().sort_index().asfreq('D', fill_value=0).to_frame('freq')

    #now extrapolate february 29th # count all would-be february29ths and multiply what we have

    min_d, max_d = min(dates), max(dates)
    print('minmax: {},{}'.format(min_d,max_d))
    min_f29_year = min_d.year if min_d < pd.Timestamp(min_d.year,3, 1)         else min_d.year+1
    max_f29_year = max_d.year if         pd.Timestamp(max_d.year,2,28) < max_d else max_d.year-1
    num_years = max_f29_year - min_f29_year + 1
    print('minmax_f29: {} {}'.format(min_f29_year, max_f29_year))
    leaps = len([pd.Timestamp(str(y)).is_leap_year for y in range(min_f29_year,max_f29_year+1)])
    print('#leaps i.e. feb 28th among recorded dates: {}'.format(leaps))
    factor = num_years / leaps if leaps > 0 else 1

    if "2016-02-29" in counts.index:
        counts['freq']["2016-02-29"] *= factor
    counts['freq_s7']=counts.freq.rolling(center=True,min_periods=0,window=7).mean()     
    return counts
