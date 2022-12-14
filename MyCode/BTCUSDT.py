import config
from binance.client import Client
from binance.enums import *
import time
import numpy as np
import pandas as pd

from Functions import trend, _ma48_15


cliente = Client(config.API_KEY,config.API_SECRET, tld='com')

simbolo = 'BTCUSDT'
cantidad_orden = 0.0012        # Quantity of BTC I am going to buy per operation. Around 20$...


### THIS BOT IS GOING TO OPERATE WITH TRENDS AND LONG TERM MOBILE LINES

while 1:
    ordenes = cliente.get_open_orders(symbol = simbolo)
    print("Actual Open Orders: ")          # If there is open orders the bot is not going to open a new order
    print(ordenes)

    if(len(ordenes) != 0):
        print("Open orders already exist, no more buys")
        time.sleep(10)
        continue

    # Bring actual price of the cryptocoin

    list_of_tickers = cliente.get_all_tickers()
    for tick_2 in list_of_tickers:
        if tick_2['symbol'] == simbolo:
            PrecioSimbolo = float(tick_2['price'])      # Price

    ma48 = _ma48_15()
    if (ma48 == 0): continue

    print("---------" + simbolo + "-----------")
    print(" Actual price of MA48 " + str('{:.8f}'.format(ma48)))     #The .8 is for the decimals Binance's API is going to return us
    print(" Crypto's actual price  "+ str('{:.8f}'.format(PrecioSimbolo)))
    print(" Price to buy at "+ str('{:.8f}'.format(ma48*0.995)))    # 0.995 represents security value to execute an operation

    if (not trend()):
        print("Downwards trend, no buy orders are going to be executed")

        time.sleep(10)
        continue
    else:
        print("Upwards trennd, buy if no open orders already")
    
    if(PrecioSimbolo > ma48 * 0.995):
        print("***  BUYING  ***")
    
    orden = cliente.order_market_buy(
        #API = local
            symbol = simbolo,
            quantity = cantidad_orden
        )
    time.sleep(5)

    # Put OCO order (One cancells other)

    order_OCO = cliente.create_oco_order(
            symbol = simbolo,
            side = SIDE_SELL,
            stopLimitPrice = str('{:.8f}'.format(PrecioSimbolo*0.994)),
            stopLimitTimeInForce = TIME_IN_FORCE_GTC,
            quantity = cantidad_orden*0.999,             # We are going to put 0.999 as Binance charges a fee for the operation, so if there is tight funds Binance will return 'Insuficient funds'
            stopPrice = str('{:.8f}'.format(PrecioSimbolo*0.995)),
            price = str('{:.8f}'.format(PrecioSimbolo*0.995))
            )

    time.sleep(20)      # Sleep, as theoretically it placed an order, so we let the market flow

