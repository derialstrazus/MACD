MACD
====

MACD Implementation

The 4 .py files contain the script to run MACD

01_getprices_SnP100.py reads the list of companies from S&P100.txt and pulls daily stock data from Yahoo Finance.

02_generateMACD.py goes through the data files and generates the MA and MACD signals.

03_tradewithMACD.py runs a trading strategy on each of the data files.

04_detailedtradingview.py is a detailed version of 03 used to look at the details for a single company at a specific time.
