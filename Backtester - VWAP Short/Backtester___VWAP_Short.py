import datetime
from io import IncrementalNewlineDecoder
from typing import AnyStr
from ibapi.common import BarData
from numpy import datetime64
import pandas as pd
import time
import threading

from ibapi.client import EClient
from ibapi.wrapper import EWrapper  
from ibapi.contract import Contract
from ibapi.order import *


class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle
		
        
	def historicalData(self, reqId, bar):
            self.data.append([bar.date, bar.close, bar.average, bar.volume, bar.high, bar.low, datetime.datetime.now()])
            #super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
            #self.data.append([date, open_, high, low, close, volume, count, wap])

class Backtester():
    def __init__(self, stock, funds, target, Days, Increment, FillAtOpen, endDateTime, paper=True):
        
        self.endDateTime = endDateTime
        self.Days = Days
        self.Increment = Increment
        self.stock = stock
        self.cum_vol = 0
        self.cum_num = 0
        self.position = False
        self.cum_change = 1
        self.target = target
        self.fill_at_open = FillAtOpen
        self.crossover = FillAtOpen # maybe move this elsewhere
        self.paper = paper
        self.funds = funds
        self.api = IBapi()
        self.api.nextorderId = None
        self.trades = []
        self.short_price = 0
        self.last_quantity = 0
        self. dr_percent_list = []
        self.n_days = 0
    
    def create_contract(self, stock, secType="STK", exchange="SMART", currency="USD"):
        self.contract = Contract()
        self.contract.symbol = stock
        self.contract.secType = secType
        self.contract.exchange = exchange
        self.contract.currency = currency
        self.contract.primaryExchange = "ISLAND"
        print("Selected stock is: ", stock)
    
    def req_historical_data(self):
        self.api.reqHistoricalData(1, self.contract, self.endDateTime, self.Days, self.Increment, 'TRADES', 0, 1, False, [])
        print("Parameters are: ", self.endDateTime, self.Days, self.Increment)
        time.sleep(2) #use at least 10 sec sleep for large amounts of data
        self.df = pd.DataFrame(self.api.data, columns=['DateTime', 'Close', 'WAP', 'Volume', 'High', 'Low', 'Time Received'])
        time.sleep(1) # use at least 6 sec for large amounts of data
        self.df.to_csv('historical backtest data.csv')

    def vwap(self, df_by_date):
        q = self.df_by_date['Volume']
        p = (df_by_date['Close']+df_by_date['High']+df_by_date['Low'])/3
        return self.df_by_date.assign(VWAP=(p * q).cumsum() / q.cumsum())

    def historical_vwap_calc(self, vwap):
        self.df_by_date = vwap(self.df_by_date)
        
        #self.df_by_date['WAP']
        #(df_by_date['Close']+df_by_date['High']+df_by_date['Low'])/3
        
    def remove_extended_hours(self):
 
        #self.df['DateTime'] = self.df['DateTime'].astype('datetime64[ns]')
        self.df_by_date['Time'] = pd.to_datetime(self.df_by_date['DateTime']).dt.time

        self.df_by_date.drop(self.df_by_date[self.df_by_date['Time'] < datetime.time(9,29,59)].index, inplace=True)
        self.df_by_date.drop(self.df_by_date[self.df_by_date['Time'] > datetime.time(15,59,59)].index, inplace=True)
        self.df_by_date.to_csv('historical backtest data.csv')

    def dr_percent(self):
        day_high = 0
        day_low = 1000
        for index, row in self.df_by_date.iterrows():
            if row['High'] > day_high:
                day_high = row['High']
            if row['Low'] < day_low:
                day_low = row['Low']
        dr = day_high / day_low
        self.dr_percent_list.append(dr)

    def adr_calc(self):
        adr = (sum(self.dr_percent_list)/self.n_days) - 1
        print("ADR: ", adr)

    def run_loop(self):
        self.api.run()    
        

    def run(self):

        
        self.api.connect('127.0.0.1', 7497, 130)

        #Start the socket in a thread
        api_thread = threading.Thread(target=self.run_loop, daemon=True)
        api_thread.start()
        time.sleep(1)
        self.create_contract(self.stock)

        self.req_historical_data()
       
        
        #pd.read_csv('historical backtest data.csv')
       
        
        self.df['Date'] = pd.to_datetime(self.df['DateTime']).dt.date

   
        self.df_by_date = []
        self.out_data = []
        

        #for index, row in self.df.iterrows():
        self.df['same_day'] = self.df.Date.eq(self.df.Date.shift())
        self.df['same_day'] = self.df.same_day.shift(-1)
        self.df.to_csv('rows.csv')
        
        for index, row in self.df.iterrows():
            if row['same_day'] == True:
                self.df_by_date.append([row['DateTime'], row['Close'], row['WAP'], row['Volume'], row['High'], row['Low'], row['Time Received']])
                
            else:
                self.df_by_date = pd.DataFrame(self.df_by_date, columns=['DateTime', 'Close', 'WAP', 'Volume', 'High', 'Low', 'Time Received'])
                #self.df_by_date.to_csv('first date.csv')
                #self.historical_vwap_calc(self.vwap)
               
                self.remove_extended_hours()
                self.historical_vwap_calc(self.vwap)
                self.dr_percent()

                #print(self.df_by_date)
               


                crossover = self.fill_at_open
                
        
                for index, row in self.df_by_date.iterrows():

                    if crossover == False:
                        if row['Close'] > row['VWAP']:
                            crossover = True
     
                    else:             
            
                        if row['Close'] < row['VWAP'] and self.position == False:
                            self.position = True
                
                            self.short_price = row['Close']
                            self.out_data.append([row['DateTime'],'Short', row['Close'], 0, 0, row['VWAP']])
            
            
                        elif row['Close'] <= self.target*self.short_price and self.position == True: 
                            self.position = False
                            crossover = False
                            self.cum_change = self.cum_change + (self.short_price-row['Close'])/self.short_price
                            self.out_data.append([row['DateTime'], 'Target' , row['Close'], 1+(self.short_price-row['Close'])/self.short_price, self.cum_change, row['VWAP']])
            
                        elif row['Close'] > row['VWAP'] and self.position == True:
                            self.position = False
                            self.cum_change = self.cum_change + (self.short_price-row['Close'])/self.short_price
                            self.out_data.append([row['DateTime'], 'Cover' , row['Close'], 1+(self.short_price-row['Close'])/self.short_price, self.cum_change, row['VWAP']])

                       
                if self.position == True:
                    self.position = False
                    self.cum_change = self.cum_change + (self.short_price-row['Close'])/self.short_price
                    self.out_data.append([row['DateTime'], 'Cover' , row['Close'], 1+(self.short_price-row['Close'])/self.short_price, self.cum_change, row['VWAP']])
                self.out_df = pd.DataFrame(self.out_data, columns=['Time', 'Action', 'Price', 'Change', 'Cum. Change', 'VWAP'])
                time.sleep(.05)
                self.out_df.to_csv('backtest_short.csv')
                self.df_by_date = []
                self.n_days += 1
        print(self.out_df['Cum. Change'])
        self.adr_calc()
        self.api.disconnect()

# Enter (stock, quantity, target, endDateTime, Days, Increment)
bot = Backtester('AERC', 100, 0.95, '1 D', '5 mins', True, '20220608 15:59:59')
#bot = Backtester('TSLA', 100, 0.97, '10 D', '10 mins', '20220518 15:59:59')

print()
print("Welcome to VWAP Cross Backtester")
bot.run()
    

