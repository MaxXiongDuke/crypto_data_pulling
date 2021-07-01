import pandas as pd
import pickle

#--- Crypto ---
#BTC
df = pd.read_csv("BTCUSDT1d", index_col= 0)
df1 = pd.read_csv("btc_usd.csv")
data = {'Date':df1['Date'], 'Close': df1['Close'], 'Volume': df1['Volume']}
btc_price_volume_2016 = pd.DataFrame(data)
index = 0
for i in range(len(df1['Date'])):
    if btc_price_volume_2016['Date'][i] == df['OpenTime'][0].split()[0]:
        index = i
for i in range(len(df['OpenTime'])):
    if i+index >= len(btc_price_volume_2016['Close']):
        break
    btc_price_volume_2016.iloc[i+index, 2] += df['Volume'][1]
pickle.dump(btc_price_volume_2016, open("btc", "wb"))
#ETH
df = pd.read_csv("ETHUSDT1d", index_col= 0)
df1 = pd.read_csv("eth_usd.csv")
data = {'Date':df1['Date'], 'Close': df1['Close'], 'Volume': df1['Volume']}
eth_price_volume_2016 = pd.DataFrame(data)
index = 0
for i in range(len(df1['Date'])):
    if eth_price_volume_2016['Date'][i] == df['OpenTime'][0].split()[0]:
        index = i
for i in range(len(df['OpenTime'])):
    if i+index >= len(eth_price_volume_2016['Close']):
        break
    eth_price_volume_2016.iloc[i+index, 2] += df['Volume'][1]
pickle.dump(eth_price_volume_2016, open("eth", "wb"))
#only 2017 Dec/17 and later
#DOT

#BNB

#---Bonds---
df = pd.read_csv("treasury yield.csv")
df = pd.concat([df['Date'],df['10 Yr']], axis = 1)
for i in range(len(df['Date'])):
    date_strings = df['Date'][i].split('/')
    if int(date_strings[0]) < 10:
        date_strings[0] = '0'+date_strings[0]
    if int(date_strings[1]) < 10:
        date_strings[1] = '0' + date_strings[1]
    if int(date_strings[2]) < 30:
        date_strings[2] = '20'+date_strings[2]
    else:
        date_strings[2] = '19' + date_strings[2]
    temp = date_strings[0]
    date_strings[0] = date_strings[2]
    date_strings[2] = date_strings[1]
    date_strings[1] = temp
    df.iloc[i,0] = '-'.join(date_strings)
pickle.dump(df, open("treasury","wb"))
#---Equities---
#S&P500
df = pd.read_csv("S&p500.csv")
for i in range(len(df['Date'])):
    date_strings = df['Date'][i].split('/')
    temp = date_strings[0]
    date_strings[0] = date_strings[2]
    date_strings[2] = date_strings[1]
    date_strings[1] = temp
    df.iloc[i,0] = '-'.join(date_strings)
df = pd.concat([df['Date'],df['Close/Last'],df['Volume']], axis = 1)
df.columns = [df.columns[0], 'Close',df.columns[2]]
df = df.reindex(index=df.index[::-1])
pickle.dump(df, open("sp500","wb"))
#VIX
df = pd.read_csv("VIX_History.csv")
for i in range(len(df['DATE'])):
    date_strings = df['DATE'][i].split('/')
    temp = date_strings[0]
    date_strings[0] = date_strings[2]
    date_strings[2] = date_strings[1]
    date_strings[1] = temp
    df.iloc[i,0] = '-'.join(date_strings)
df = pd.concat([df['DATE'],df['CLOSE']], axis = 1)
df.columns = ['Date', 'Close']
pickle.dump(df, open("vix","wb"))
#---Commodities---

#Brent Crude Oil
df = pd.read_csv("BZ  Brent Crude Oil.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
df.drop(df.tail(1).index,inplace=True)
pickle.dump(df, open("oil","wb"))

#Texas Oil
df = pd.read_csv("CL West Texas Intermediate Crude Oil.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
df.drop(df.tail(1).index,inplace=True)
pickle.dump(df, open("localOil","wb"))

#Gas
df = pd.read_csv("gas.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
df.drop(df.tail(1).index,inplace=True)
pickle.dump(df, open("gas","wb"))

#Gold
df = pd.read_csv("gold price.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
df.drop(df.tail(1).index,inplace=True)
pickle.dump(df, open("gold","wb"))
#Copper
df = pd.read_csv("HG Copper.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
df.drop(df.tail(1).index,inplace=True)
pickle.dump(df, open("copper","wb"))
#---Currencies
df = pd.read_csv("CAD=X.csv")
df = pd.concat([df['Date'],df['Close'],df['Volume']], axis = 1)
for i in range(len(df['Date'])):
    date_strings = df['Date'][i].split('/')
    if int(date_strings[0]) < 10:
        date_strings[0] = '0'+date_strings[0]
    if int(date_strings[1]) < 10:
        date_strings[1] = '0' + date_strings[1]
    if int(date_strings[2]) < 30:
        date_strings[2] = '20'+date_strings[2]
    else:
        date_strings[2] = '19' + date_strings[2]
    temp = date_strings[0]
    date_strings[0] = date_strings[2]
    date_strings[2] = date_strings[1]
    date_strings[1] = temp
    df.iloc[i,0] = '-'.join(date_strings)
pickle.dump(df, open("CAD","wb"))