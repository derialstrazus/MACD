from pandas import Series, DataFrame
import pandas as pd
import os

def getStocks():
    #Function reads SnP100.txt and get list of companies
    SnP100File = 'S&P100.txt'
    SnPData = open(SnP100File,'r').read()
    splitSnPData = SnPData.split('\n')
    
    stocks = []
    for eachLine in splitSnPData:
        splitLine = eachLine.split('\t')
        stocks.append(splitLine[0])
        
    return stocks

def getMvgAvg(quotes, points, title):
    #Function takes the average of points number of ticks.
    s = title
    quotes[s] = float('NaN')
    Sum = 0
    for n in range(0,points):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / points
    quotes[s][n] = float('%.4f' % (MvgAvg))
    for n in range(points,len(quotes)):
        Sum = Sum - quotes.AdjClose[n-points] + quotes.AdjClose[n]
        MvgAvg = Sum / points
        quotes[s][n] = float('%.4f' % (MvgAvg))
    return quotes

def getMACDMvgAvg(quotes, points):
    #Function takes the average of points number of ticks.
    s = 'MACDMvgAvg' + str(points)
    quotes[s] = float('NaN')
    Sum = 0
    for n in range(26,26+points):
        Sum = Sum + quotes.MACD[n]
    MvgAvg = Sum / points
    quotes[s][n] = float('%.4f' % (MvgAvg))
    for n in range(26+points,len(quotes)):
        Sum = Sum - quotes.MACD[n-points] + quotes.MACD[n]
        MvgAvg = Sum / points
        quotes[s][n] = float('%.4f' % (MvgAvg))
    return quotes
    
def getMACDSignal(quotes):
    quotes['MACD'] = float('NaN')
    for n in range(26,len(quotes)):
        MACD = quotes.MvgAvgShort[n] - quotes.MvgAvgLong[n]
        quotes['MACD'][n] = float('%.4f' % (MACD))
    return quotes
    
def getMACDTrigger(quotes):
    quotes['MACDTrigger'] = float('NaN')
    for n in range(26,len(quotes)):
        if quotes.MACD[n] > 0:
            quotes.MACDTrigger[n] = 1
        else:
            quotes.MACDTrigger[n] = 0
    return quotes

#-------------------------------------------------------------------------------
#Main():

dataPath = os.getcwd() + '\SnP100Daily'     #Sub directory to store data

stocksToAnalyze = getStocks()   #Returns list of companies

for eachStock in stocksToAnalyze[:20]:
    fileName = 'daily_' + eachStock + '.txt'
    readLine = os.path.join(dataPath,fileName)

    quotes = pd.read_csv(readLine)
    quotes.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose']
    quotes = quotes.drop(['Open','High','Low','Close','Volume'], 1)     #Drop useless columns to save space

    quotes = getMvgAvg(quotes,12,'MvgAvgShort')       #12 point moving average
    quotes = getMvgAvg(quotes,26,'MvgAvgLong')       #26 point moving average  
    quotes = getMACDSignal(quotes)
    quotes = getMACDMvgAvg(quotes,9)
    quotes = getMACDTrigger(quotes)

    saveFileName = 'output_'+eachStock+'.txt'
    saveFileLine = os.path.join(dataPath,saveFileName)
    quotes.to_csv(saveFileLine)