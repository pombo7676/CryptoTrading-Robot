import config
from binance.client import Client
from binance.enums import *
import time
import numpy as np
cliente = Client(config.API_KEY, config.API_SECRET, tld='com')


# ***** MOVING AVERAGES WITH 5 MINS CANDLESTICKS ******

# Moving Average 5 in periods of 5mins during 25 minutes


def _ma5_5():

    ma5_local = 0
    sum = 0

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_5MINUTE, "25 minute ago UTC")

    if(len(klines)==5):
        for i in range (0,5):
            sum = sum +float(klines[i][4]) # 4 refers to the closing price of the candlestick
        
        ma5_local = sum / 5

    return ma5_local

# Moving Average 10 in periods of 5mins during 50 minutes


def _ma10_5():

    ma10_local = 0
    sum = 0

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_5MINUTE, "50 minute ago UTC")

    if(len(klines)==10):
        for i in range (0,10):
            sum = sum +float(klines[i][4]) # 4 refers to the closing price of the candlestick
        
        ma10_local = sum / 10

    return ma10_local

# Moving Average 20 in periods of 5mins during 100 minutes

def _ma20_5():

    ma20_local = 0
    sum = 0

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_5MINUTE, "100 minute ago UTC")

    if(len(klines)==20):
        for i in range (0,20):
            sum = sum +float(klines[i][4]) # 4 refers to the closing price of the candlestick
        
        ma20_local = sum / 20

    return ma20_local





# ***** MOVING AVERAGES WITH 15 MINS CANDLESTICKS ******

# Moving Average 48 in periods of 15mins during 12 hours

def _ma48_15():

    ma48_local = 0
    sum = 0

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_15MINUTE, "12 hour ago UTC")

    if(len(klines)==48):
        for i in range (0,48):
            sum = sum +float(klines[i][4]) # 4 refers to the closing price of the candlestick
        
        ma48_local = sum / 48

    return ma48_local




# Trend to check if it is an Upwards Trend or Downwards Trend

def trend():
    x = []
    y = []
    sum = 0
    ma48_i = 0

    resp = False

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_15MINUTE, "18 hour ago UTC")

    if (len(klines) != 72):
        
        return False
    for i in range (1,72): # from 24 to 60, 36 candlesticks of 15 minutes are 9hs average

        for j in range (i-72,i): 
          sum = sum + float(klines[i][4])
        ma48_i = '{:.8f}'.format(sum /72)
        sum = 0
        x.append(i)
        y.append(float(ma48_i))

    modelo = np.polyfit(x,y,1)
    if (modelo[0]>0):
        resp = True
    

    return resp