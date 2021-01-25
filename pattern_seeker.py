import sys
import time
import webbrowser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from nsetools import Nse
from nsepy import get_history
from datetime import date

# Get all the stock symbols
nse = Nse()
all_symbols = nse.get_stock_codes()
del all_symbols['SYMBOL']

print("Total symbols: %d" % (len(all_symbols)))
keys = list(all_symbols.keys())

def get_pattern(max, min):
    for row in max:
        print(row)

    for row in min:
        print(row)

def get_historical(start, end, sYear, sMonth, sDay, eYear, eMonth, eDay):
    for i in range(start, end):
        symbol = keys[i]
        data = get_history(symbol=symbol, start=date(sYear, sMonth, sDay), end=date(eYear, eMonth, eDay))
        # So far, this works ok in a 6 month chart.
        # TODO Tuning of the max and min calculation in get_max_min
        max, min= get_max_min(data, 2, 10)
        get_pattern(max, min)
        data.reset_index()['Close'].plot()
        plt.scatter(max.index, max.values, color='green', alpha=.5)
        plt.scatter(min.index, min.values, color='red', alpha=.5)
        plt.show()

def get_max_min(prices, smoothing, window_range):
    smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]

    price_local_max_dt = []
    for i in local_max:
        if (i>window_range) and (i<len(prices)-window_range):
            price_local_max_dt.append(prices.iloc[i-window_range:i+window_range]['Close'].idxmax())

    price_local_min_dt = []
    for i in local_min:
        if (i>window_range) and (i<len(prices)-window_range):
            price_local_min_dt.append(prices.iloc[i-window_range:i+window_range]['Close'].idxmin())  

    maxima = pd.DataFrame(prices.loc[price_local_max_dt])
    minima = pd.DataFrame(prices.loc[price_local_min_dt])

    # max_min = pd.concat([maxima, minima]).sort_index()
    # XXX if you want to combine max and min in one data frame
    # similarly combine all below operations
    max = pd.concat([maxima]).sort_index()
    max.index.name = 'date'

    min = pd.concat([minima]).sort_index()
    min.index.name = 'date'

    max = max.reset_index()
    max = max[~max.date.duplicated()]

    min = min.reset_index()
    min = min[~min.date.duplicated()]

    p = prices.reset_index()   

    max['day_num'] = p[p['Date'].isin(max.date)].index.values
    max = max.set_index('day_num')['Close']
    
    min['day_num'] = p[p['Date'].isin(min.date)].index.values
    min = min.set_index('day_num')['Close']
    return max, min

if __name__ == '__main__':
    if len(sys.argv) < 9:
        print("Not enough arguments")
        sys.exit(1)

    get_historical(int(sys.argv[1]), int(sys.argv[2]),
            int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]),
            int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
