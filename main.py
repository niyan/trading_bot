import requests, json
import pandas as pd
from config import api_key, api_secret
from client import Client

posFrame = pd.read_csv('positionCheck')

client = Client(api_key, api_secret)

def get_hourly_data(symbol, period):
    df = pd.DataFrame(client.get_candles(symbol, period))
    df = df[['timestamp', 'close']]
    df.close = df.close.astype(float)
    return df

def apply_sma(df):
    df['FastSMA'] = df.close.rolling(5).mean()
    df['SlowSMA'] = df.close.rolling(75).mean()
    return df

def change_position(symbol, order, buy=True):
    if buy:
        posFrame.loc[posFrame.symbol == symbol, 'position'] = 1
        quantity = float(order['quantity'])
        posFrame.loc[posFrame.symbol == symbol, 'quantity'] = quantity
    else:
        posFrame.loc[posFrame.symbol == symbol, 'position'] = 0
        posFrame.loc[posFrame.symbol == symbol, 'quantity'] = 0
    return order

def run_trade_bot():
    for symbol in posFrame[posFrame.position == 1].symbol:
        df = get_hourly_data(symbol)
        apply_sma(df)
        last_row = df.iloc[-1]
        if last_row.SlowSMA > last_row.FastSMA:
            quantity = posFrame[posFrame.symbol == symbol].quantity.values[0]
            order = client.send_order(symbol, 'sell', quantity, 'market')
            print(order)
            change_position(symbol, order, buy=False)

    for symbol in posFrame[posFrame.position == 0].symbol:
        df = get_hourly_data(symbol, period='M30')
        apply_sma(df)
        last_row = df.iloc[-1]
        if last_row.FastSMA > last_row.SlowSMA:
            quantity = 100 / df.iloc[:1].close # THIS IS WRONG
            order = client.send_order(symbol, 'buy', quantity, 'market')
            print(order)
            change_position(symbol, order, buy=True)
        else:
            print(f'buy condition not met for {symbol}')
            
while True:
    try:
        run_trade_bot()
    except:
        continue
