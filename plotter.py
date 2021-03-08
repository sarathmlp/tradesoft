import sys
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

base_url= "https://www.screener.in/company/"

class Plotter:
    def __init__ (self):
        self.t_list = []

    def open_url (self, con, symbol):
        if con == 1:
            address = base_url + symbol + '/consolidated'
        else:
            address = base_url + symbol
        try:
            url = urllib.request.urlopen(address)
        except:
            print("Address not found: " + address)
            sys.exit(1)
        resp = url.read()
        soup = BeautifulSoup(resp, 'html.parser')
        tables = soup.findAll("table")

        for table in tables:
            try:
                df = pd.read_html(str(table))[0]
                df = df.T # transpose
                new_header = df.iloc[0] # grab the first row for the header
                df = df[1:] # take the data less the header row
                df.columns = new_header # set the header row as the df header
                df.columns = df.columns.str.replace('[#,@,&,+,\xa0]', '') # remove special characters
            except:
                break
            self.t_list.append(df)

        tc = len(self.t_list)
        self.qresults = self.t_list[0]
        self.pnl = self.t_list[1]
        if tc > 6:
            self.balance = self.t_list[6]
        if tc > 9:
            self.holding = self.t_list[9]

    def get_qpnl (self):
        df = self.qresults
        if "Operating Profit" not in df.columns:
            df["Operating Profit"] = pd.to_numeric(df["Financing Profit"])
        else:
            df["Operating Profit"] = pd.to_numeric(df["Operating Profit"])

        df["Net Profit"] = pd.to_numeric(df["Net Profit"])

        pdf = pd.DataFrame({"Earnings":df["Net Profit"]}, index=df.index)
        return pdf

    def get_apnl (self):
        df = self.pnl
        if "Operating Profit" not in df.columns:
            df["Operating Profit"] = pd.to_numeric(df["Financing Profit"])
        else:
            df["Operating Profit"] = pd.to_numeric(df["Operating Profit"])

        df["Net Profit"] = pd.to_numeric(df["Net Profit"])

        pdf = pd.DataFrame({"Earnings":df["Net Profit"]}, index=df.index)
        return pdf

    def get_balance_sheet (self):
        df = self.balance
        df["Reserves"] = pd.to_numeric(df["Reserves"])
        df["Borrowings"] = pd.to_numeric(df["Borrowings"])

        pdf = pd.DataFrame({"Reserves": df["Reserves"], "Borrowings": df["Borrowings"]}, index=df.index)
        return pdf

    def get_holding (self):
        df = self.holding
        df["Promoters"] = pd.to_numeric(df["Promoters"])
        df["DIIs"] = pd.to_numeric(df["DIIs"])
        df["Public"] = pd.to_numeric(df["Public"])
        if "FIIs" in df.columns:
            df["FIIs"] = pd.to_numeric(df["FIIs"])
            pdf = pd.DataFrame({"Promoters": df["Promoters"], "FIIs": df["FIIs"], "DIIs": df["DIIs"], "Public": df["Public"]}, index=df.index)
        else:
            pdf = pd.DataFrame({"Promoters": df["Promoters"], "DIIs": df["DIIs"], "Public": df["Public"]}, index=df.index)
        return pdf

    def plot (self):
        ypnl = self.get_apnl()
        qpnl = self.get_qpnl()
        tc = len(self.t_list)
        if tc > 6:
            balance = self.get_balance_sheet()
        if tc > 9:
            holding = self.get_holding()

        fig, axs = plt.subplots(2, 2)
        fig.tight_layout()
        axs[0,0].tick_params(axis="x", labelsize=8)
        axs[0,1].tick_params(axis="x", labelsize=8)
        axs[1,0].tick_params(axis="x", labelsize=8)
        axs[1,1].tick_params(axis="x", labelsize=8)

        try:
            ypnl.plot(ax=axs[0, 0], kind='bar', color = 'royalblue')
            qpnl.plot(ax=axs[0, 1], kind='bar', color = 'darkorange')
            tc = len(self.t_list)
            if tc > 6:
                balance.plot(ax=axs[1, 0], kind='bar', color = ['#2ECC71','#E74C3C'])
            if tc > 9:
                holding.plot(ax=axs[1, 1], kind='bar', color = ['#8E44AD', '#2ECC71','#FFBF00', '#85929E'])

            plt.show()
        except:
            print("** Failed to plot. Try toggling consolidation")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("not enough arguments\n")
        sys.exit(1)

    plotter = Plotter()
    plotter.open_url(int(sys.argv[1]), sys.argv[2])
    plotter.plot()
