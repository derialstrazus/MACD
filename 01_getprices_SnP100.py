import urllib2
import time
import datetime
import os

def getStocks():
    SnP100File = 'S&P100.txt'
    SnPData = open(SnP100File,'r').read()
    splitSnPData = SnPData.split('\n')
    
    stocksToPull = []
    for eachLine in splitSnPData:
        splitLine = eachLine.split('\t')
        stocksToPull.append(splitLine[0])
        
    print stocksToPull
    return stocksToPull


def pullData(stock):
    try:
        print '\nCurrently pulling',stock
        urlToVisit = 'http://real-chart.finance.yahoo.com/table.csv?s='+stock+'&d=8&e=13&f=2014&g=d&a=11&b=12&c=2000&ignore=.csv'

        fileName = 'raw_daily_'+stock+'.txt'
        filePath = os.path.join(saveDir, fileName)
        saveFile = open(filePath,'w')
        sourceCode = urllib2.urlopen(urlToVisit).read()
        saveFile.write(sourceCode)
        saveFile.close()

        print filePath
        print 'Pulled',stock
                
    except Exception,e:
        print 'main loop', str(e)

                
def csvFlipper(readFileName, saveFileName):
    readFilePath = os.path.join(saveDir, readFileName)
    readFile = open(readFilePath,'r')
    saveFilePath = os.path.join(saveDir, saveFileName)
    saveFile = open(saveFilePath, 'w')
    saveFile.write(readFile.readline())  #To keep header
    
    for line in reversed(readFile.readlines()):
        saveFile.write(line)
    
    readFile.close()
    saveFile.close()

#-------------------------------------------------------------------------------
#Main():

stocksToPull = getStocks()      #Read SnP100.txt and get list of companies

saveDir = os.getcwd()+'\SnP100Daily'
if not os.path.exists(saveDir):    #Check if saveDir exists, create if not
    os.makedirs(saveDir)

for eachStock in stocksToPull: 
    pullData(eachStock)
    readFileName = 'raw_daily_'+eachStock+'.txt'
    saveFileName = 'daily_'+eachStock+'.txt'
    csvFlipper(readFileName,saveFileName)
    readFilePath = os.path.join(saveDir, readFileName)
    os.remove(readFilePath)
    print 'Flipped',eachStock
    