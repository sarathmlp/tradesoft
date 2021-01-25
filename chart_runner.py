import sys
import time
import webbrowser
from nsetools import Nse

# Get all the stock symbols
nse = Nse()
all_symbols = nse.get_stock_codes()
del all_symbols['SYMBOL']

print("Total symbols: %d" % (len(all_symbols)))
keys = list(all_symbols.keys())

url = 'https://chartink.com/stocks/'

def display_chart(start, end):
    for i in range(start, end):
        symbol = keys[i]
        print(i, ': ' + symbol)
        address = url + symbol + '.html'
        webbrowser.open(address)
        time.sleep(5)
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments")
        sys.exit(1)

    display_chart(int(sys.argv[1]), int(sys.argv[2]))
