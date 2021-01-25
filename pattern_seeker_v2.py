import sys
import time
import webbrowser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.signal import find_peaks, find_peaks_cwt
from nsetools import Nse
from nsepy import get_history
from datetime import date

# Get all the stock symbols
nse = Nse()
all_symbols = nse.get_stock_codes()
del all_symbols['SYMBOL']

print("Total symbols: %d" % (len(all_symbols)))
keys = list(all_symbols.keys())

def get_historical(start, end, sYear, sMonth, sDay, eYear, eMonth, eDay):
    for i in range(start, end):
        symbol = keys[i]
        print(symbol)
        data = get_history(symbol=symbol, start=date(sYear, sMonth, sDay), end=date(eYear, eMonth, eDay))

        # So far, this works ok in a 6 month chart.
        # TODO Tuning of the max and min calculation in get_max_min
        get_max_min(data, 1)

def get_max_min(prices, smoothing):
    prices['Close'].plot()
    print(prices)

    smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
    print(smooth_prices)

    smooth_prices.plot()
    plt.show()

    peaks, _ = find_peaks(smooth_prices)
    print(peaks)

    peak_dt = []
    for peak in peaks:
        peak_dt.append(prices.iloc[peak])
        print(prices.iloc[peak]['Close'])

    inverted = smooth_prices * -1
    valleys, _ = find_peaks(inverted)
    print(valleys)

    for valley in valleys:
        print(prices.iloc[valley]['Close'])


if __name__ == '__main__':
    if len(sys.argv) < 9:
        print("Not enough arguments")
        sys.exit(1)

    get_historical(int(sys.argv[1]), int(sys.argv[2]),
            int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]),
            int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
