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

def getYearBreakLocation(quotesTime):
    #Function checks the difference between unix Times and determines where a market has closed for the day
    breakLocation = []
    for n in range(1,len(quotesTime)):
        if int(quotes['Date'][n][:4]) != int(quotes['Date'][n-1][:4]):  # current - past
            breakLocation.append(n)
    return breakLocation

def applyStrategy(quotes, bank, name, newYearIndex, resultsFile):
    shares = 0
    resultsFile.write('\nAnalysis for %s\n' % stock)
    resultsFile.write('-------------------------\n')
    startingBank = bank
    totalBank = bank
    resultsFile.write('%s %15s %15s     %s\n' % ('Year', 'Initial', 'Final', 'Performance'))
    for n in range(len(newYearIndex) - 1):
        start = newYearIndex[n]
        end = newYearIndex[n+1] - 1   
        year = int(quotes['Date'][start][:4])
        #print '%s starts at: %d and ends at: %d' % (year, start, end)

        for n in range(start,end):
            if quotes.MACDTrigger[n] == 1:
                sharesBought = int(bank / quotes.AdjClose[n])
                bankSpent = sharesBought * quotes.AdjClose[n]
                shares = shares + sharesBought
                bank = bank - bankSpent
                #if sharesBought:
                #    print '%s: Bought %d AAPL shares at %.2f per share.  Spent %d.  Bank has %.2f.  Currently %d shares.' % (quotes.Date[n], sharesBought, quotes.AdjClose[n], bankSpent, bank, shares)
            else:
                sell = int(shares)
                shares = shares - sell
                if shares != 0:
                    print 'something wrong!'
                sharesSold = sell * quotes.AdjClose[n]
                bank = bank + sharesSold
                #if sharesSold:
                #    print '%s: Sold %d AAPL shares at %.2f per share.  Bank has: %.2f.  Currently %d shares.' % (quotes.Date[n], sell, quotes.AdjClose[n], bank, shares)
            
            totalBank = bank + (shares * quotes.AdjClose[n])
        performance = 100.0 * totalBank / startingBank

        resultsFile.write('%s |  $ %10.2f |  $ %10.2f |   %d\n' % (year, startingBank, totalBank, performance))
        # resultsFile.write('Initial Investment for %d was: %10.2f\n' % (year, startingBank))
        # resultsFile.write('Final Investment for %d was  : %10.2f\n' % (year, totalBank))
        # resultsFile.write('Performance for the year %s was: %d percent\n\n' % (year, performance))

        startingBank = totalBank

    return totalBank

#-------------------------------------------------------------------------------
#Main():

dataPath = os.getcwd() + '\SnP100Daily'     #Sub directory to store data
createResultsFile = open('outputDailyResults.txt','w')
createResultsFile.close()

stocksToAnalyze = getStocks()   #Returns list of companies

for stock in stocksToAnalyze[:20]:
    fileName = 'output_' + stock + '.txt'
    readLine = os.path.join(dataPath,fileName)
    quotes = pd.read_csv(readLine)

    breakLocation = getYearBreakLocation(quotes['Date'])

    initialInvestment = 100000
    resultsFile = open('outputDailyResults.txt','a')
    finalInvestment = applyStrategy(quotes, initialInvestment, stock, breakLocation, resultsFile)
    
    print 'Invested in %s' % stock

resultsFile.close()