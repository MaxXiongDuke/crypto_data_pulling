import pandas as pd
import pickle
from functools import reduce
import os
import scipy

import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
def geomean_calculation(ls):
    product = 1
    for i in ls:
        product = product *(1+i)
    return (np.power(product, 1/len(ls)) - 1) * 100
def year_over_year_cor(df1, list_df, names, year_range):
    cor_years = list()
    for i in list_df:
        dfs = [df1, i]
        matrix = reduce(lambda left, right: pd.merge(left, right, on='Date'), dfs)
        cors = list()
        for j in year_range:
            start = str(j)+"-01-01"
            end = ""+str(j+1)+"-01-01"
            #print(matrix[(matrix.Date>start)  & (matrix.Date<end)])
            cors.append((matrix[(matrix.Date>start)&(matrix.Date<end)]).corr(method = 'pearson').iloc[0,1])
        cor_years.append(cors)
    cor_years_df = pd.DataFrame(cor_years)
    cor_years_df.index = names
    cor_years_df.columns = year_range
    return cor_years_df
def cor_2_assets_dynamic(df1, df2, days):
    cor_list = list()
    dfs = [df1, df2]
    matrix = reduce(lambda left, right: pd.merge(left, right, on='Date'), dfs)
    print(matrix.Date)
    for i in range(len(matrix) - days):
        cor_list.append(matrix[i:i + days].corr().iloc[0, 1])
    Dates = matrix['Date'][days:]
    cor_df = pd.DataFrame({'correlation': cor_list})
    cor_df.index = Dates
    return cor_df
def clean_data_with_price(df, name):
    if name == 'treasury':
        return dropVolume(df).rename(columns = {'10 Yr':name}).dropna()
    return dropVolume(df).rename(columns = {'Close':name}).dropna()
def cleanData(df, name):
    if name == 'treasury':
        return getReturns(dropVolume(df).rename(columns = {'10 Yr':name}),name).dropna()
    return getReturns(dropVolume(df).rename(columns = {'Close':name}),name).dropna()

def dropVolume(df):
    if 'Volume' in df.columns:
        return df.drop(['Volume'],axis = 1)
    else:
        return df

def getReturns(df, name):
    change = list()
    for i in range(len(df[name])-1):
        change.append((df[name][i+1]-df[name][i])/df[name][i])
    return pd.DataFrame({'Date':df['Date'][1:],name:change})

def getCorrelationMatrix(changes):
    matrix_list = list()
    for i in changes:
        correlations = list()
        for j in changes:
            df1 = i[i.Date > "2016-01-01"]
            df2 = j[j.Date > "2016-01-01"]
            dfs = [df1, df2]
            matrix = reduce(lambda left, right: pd.merge(left, right, on='Date'), dfs)
            correlations.append(matrix.corr(method='pearson').iloc[0,1])
        matrix_list.append(correlations)
    return pd.DataFrame(matrix_list)

btc = pickle.load(open("btc","rb"))
eth= pickle.load(open("eth","rb"))
sp500= pickle.load(open("sp500","rb"))
sp500 =sp500.reset_index(drop=True)
treasury= pickle.load(open("treasury","rb"))
oil= pickle.load(open("oil","rb"))
gold= pickle.load(open("gold","rb"))
copper= pickle.load(open("copper","rb"))
gas= pickle.load(open("gas","rb"))
#VIX
vix = pickle.load((open("vix","rb")))
vix = vix[vix.Date > "2016-01-01"].reset_index(drop = True)
vix.columns = ['Date','VIX']
#CAD
cad = pickle.load((open("CAD","rb")))
#= pickle.load(open("","rb"))

btcChange = cleanData(btc, "btc")
ethChange = cleanData(eth,'eth')
sp500Change = cleanData(sp500,'sp500')
treasuryChange = cleanData(treasury,'treasury')
oilChange = cleanData(oil,'oil')
goldChange = cleanData(gold,'gold')
copperChange =cleanData(copper,'copper')
gasChange = cleanData(gas,'gas')
vixChange = getReturns(vix, "VIX")
cadChange = cleanData(cad,"CAD")
#VIX correlation
vix_btc_data = pd.merge(btcChange, vix, on = 'Date', how = 'inner')
print(vix_btc_data.corr().iloc[0,1])
vix_btc_change_data = pd.merge(btcChange,vixChange, on  = 'Date', how = 'inner')
print(vix_btc_change_data.corr().iloc[0,1])
#build correlation matrix from 2016
names = ['Bitcoin','Ethereum','S&P500',"10 Year Treasury","Brent Oil", "Gold", "Copper", "Gas"]
changeList = [btcChange,ethChange,sp500Change,treasuryChange,oilChange,goldChange,copperChange,gasChange]
corMatrix = getCorrelationMatrix(changeList)
corMatrix.columns = names
corMatrix.index = names
corMatrix.to_csv(os.getcwd()+"/correlationMatrixFrom2016.csv")

#plot heatmap of correlation matrix
plt.figure(figsize=(16, 6))
#mask = np.triu(np.ones_like(corMatrix, dtype=np.bool))
heatmap = sb.heatmap(corMatrix, vmin=-1, vmax=1, annot=True, square= True,cmap="YlOrRd")
heatmap.set_title('Digital Assets and Traditional Assets Correlation Matrix', fontdict={'fontsize':12}, pad=12);
heatmap.xaxis.tick_top()
plt.xticks(fontsize = 9,rotation = 24)
plt.yticks(fontsize = 9)
#heatmap.invert_yaxis()
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')

#plot monthly coorelation matrix
month_cor_btc_sp500_df = cor_2_assets_dynamic(btcChange, sp500Change,30)
month_cor_eth_sp500_df = cor_2_assets_dynamic(ethChange, sp500Change,30)
month_cor_btc_vix_df = cor_2_assets_dynamic(btcChange,vix,30)
month_cor_btc_vix_change_def = cor_2_assets_dynamic(btcChange,vixChange,30)
plt.plot(month_cor_btc_vix_df.index,month_cor_btc_vix_df['correlation'])
plt.show()
month_cor_btc_sp500_df.to_csv(os.getcwd()+"/month_cor_btc_sp500.csv")
month_cor_eth_sp500_df.to_csv(os.getcwd()+"/month_cor_eth_sp500.csv")

yoy_cor_btc = year_over_year_cor(btcChange,changeList[2:],names[2:],[2016,2017,2018,2019,2020,2021])
yoy_cor_btc.index.name = "BTC correlation with other assets year over year"
yoy_cor_btc.to_csv(os.getcwd()+"/yoy_cor_btc.csv")

yoy_cor_eth = year_over_year_cor(ethChange,changeList[2:],names[2:],[2016,2017,2018,2019,2020,2021])
yoy_cor_eth.index.name = "Assets"
yoy_cor_eth.to_csv(os.getcwd()+"/yoy_cor_eth.csv")

#summary graph generation
tempList = [btc, eth, sp500, treasury, oil, gold, copper, gas]
priceList = list()
for i in range(8):
    priceList.append(clean_data_with_price(tempList[i], names[i]))
matrix = reduce(lambda left, right: pd.merge(left, right, on='Date'), priceList)
matrix.to_csv(os.getcwd()+"/priceTogether.csv")

total_returns = list()
for i in matrix.columns:
    if i != 'Date':
        total_return = list()
        for j in range(len(matrix[i])-1):
            total_return.append(np.log(matrix[i][j+1]/matrix[i][0]))
        total_returns.append(total_return)

same_scale_price = pd.DataFrame(total_returns).transpose()
same_scale_price.columns = names
temp_date = matrix['Date'][1:].to_list()
same_scale_price.insert(0, 'Date', temp_date)
same_scale_price.loc[-1] = [matrix['Date'][0], 0,0,0,0,0,0,0,0]  # adding a row
same_scale_price.index = same_scale_price.index + 1  # shifting index
same_scale_price = same_scale_price.sort_index()  # sorting by index
same_scale_price.to_csv(os.getcwd()+"/priceTogetherSameScale.csv")