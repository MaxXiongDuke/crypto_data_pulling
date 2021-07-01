# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#import all the package
from binance.client import Client
import pandas as pd
import os
from datetime import datetime

with open('APIKey.txt') as f:
    f.readline()
    apiKey = f.readline().strip()
    f.readline()
    apiSecret = f.readline().strip()
f.close()
sybList = ["BTCUSDT","LTCUSDT","DOGEUSDT","ETHUSDT","XRPUSDT","BNBUSDT","DOTUSDT","ADAUSDT","BCHUSDT","BUSDUSDT"]

def binance_connection():
    # Use a breakpoint in the code line below to debug your script.
    client = Client(apiKey,apiSecret)
    print("connection successful")
    return client

def getInfo(client, symbol):
    info = client.get_symbol_info(symbol)
    for i in info:
        print(i)

def fetchKlineData(client, ticker, startDate, interval):
    if interval == "1d":
        return fetchKlineDays(client, ticker, startDate)
    elif interval == "1h":
        return fetchKlineHours(client, ticker, startDate)
    elif interval == "30m":
        return fetchKlineMinutes(client, ticker, startDate)
    else:
        print("invalid interval type")
        return
def fetchKlineDays(client, ticker, startDate):
    return client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1DAY, startDate)

def fetchKlineHours(client, ticker, startDate):
    return client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1HOUR, startDate)

def fetchKlineMinutes(client, ticker, startDate):
    return client.get_historical_klines(ticker, Client.KLINE_INTERVAL_30MINUTE, startDate)

def klineToDataFrames(kline):
    columnNames = ["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "Quote Asset Volume",
                  "Number of Trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    df = pd.DataFrame(columns = columnNames)

    for i in kline:
        i[0] = datetime.utcfromtimestamp(int(i[0])/1000).strftime('%Y-%m-%d %H:%M:%S')
        i[6] = datetime.utcfromtimestamp(int(i[6])/1000).strftime('%Y-%m-%d %H:%M:%S')
        df.loc[len(df)] = i
    return df

def saveToCSV(df, syb, interval):
    cwd = os.getcwd()
    path = cwd + "/"+syb + interval +".csv"
    df.to_csv(path)

def pullIntervalData(interval):
    for i in sybList:
        kline = fetchKlineData(client, i, "1 Dec, 2017", interval)
        df = klineToDataFrames(kline)
        saveToCSV(df,i, interval)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = binance_connection()
    #getInfo(client, "BNBBTC")
    pullIntervalData('1d')
    #pullIntervalData('1h')
    #pullIntervalData('30m')
