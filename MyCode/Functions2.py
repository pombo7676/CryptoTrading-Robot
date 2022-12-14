# ***** MOVING AVERAGES WITH 15 MINS CANDLESTICKS ******

# Moving Average 48 in periods of 15mins during 12 hours

def _ma48_():
    import time
    import numpy as np
    import config
    from binance.client import Client
    from binance.enums import *
    cliente = Client(config.API_KEY, config.API_SECRET, tld='com')
    ma48_local = 0
    sum = 0

    klines = cliente.get_historical_klines(simbolo, Client.KLINE_INTERVAL_15MINUTE, "12 hour ago UTC")

    if(len(klines)==48):
        for i in range (0,48):
            sum = sum +float(klines[i][4]) # 4 refers to the closing price of the candlestick
        
        ma48_local = sum / 48

    return ma48_local




# Trend to check if it is an Upwards Trend or Downwards Trend

def tendencia():
    import time
    import numpy as np
    import config
    from binance.client import Client
    from binance.enums import *
    cliente = Client(config.API_KEY, config.API_SECRET, tld='com')
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