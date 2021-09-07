import sys
import time, threading
import webbrowser
from nsetools import Nse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

nse = Nse()
all_symbols = nse.get_stock_codes()
del all_symbols['SYMBOL']

print("Total symbols: %d" % (len(all_symbols)))
keys = list(all_symbols.keys())

url = 'https://finance.yahoo.com/chart/%5ENSEI'
pause_execution = False
stop_thread = False

base_url= "https://www.screener.in/company/"

class Driver:
    def __init__ (self):
        chromeOptions = Options()
        # start fullscreen
        # chromeOptions.add_argument("--kiosk")
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.driver.get(url)

    def set_view (self):
        input("Enter any key when ready!")
        return

    def __del__ (self):
        print("Cleaning up!")
        self.driver.close()

    def display_chart(self, start, end):
        i = start
        while i < end:
            try:
                if pause_execution == True:
                    print("*", end="", flush=True)
                    time.sleep(10)
                    continue

                symbol = keys[i]
                print(i, ': ' + all_symbols[symbol] + ' (' + base_url + symbol + '/consolidated' + ')')
                symbol = symbol + ".NS"

                self.driver.find_element_by_xpath("//*[@id='main-1-FullScreenChartIQ-Proxy']/section/header/div[3]/div/div/div/fieldset/input").send_keys(symbol)
                time.sleep(0.5) # to fix the drop down list display issue
                self.driver.find_element_by_xpath("//*[@id='main-1-FullScreenChartIQ-Proxy']/section/header/div[3]/div/div/div/fieldset/input").send_keys(Keys.ENTER)
                time.sleep(10)
                i += 1
            except KeyboardInterrupt:
                sys.exit(1)


def toggle_pause_execution():
    global pause_execution
    lock = threading.Lock()
    print("Enter any key to toggle pause!")
    print("------------------------------")

    while True:
        with lock:
            input()
            pause_execution = not pause_execution

            if stop_thread:
                break

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments\n")
        sys.exit(1)

    driver = Driver()
    driver.set_view()

    thread = threading.Thread(target = toggle_pause_execution)
    thread.start()

    driver.display_chart(int(sys.argv[1]), int(sys.argv[2]))

    stop_thread = True
    thread.join()

