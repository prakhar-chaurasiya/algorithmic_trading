from yahoo_finance import loadprices

loadprices("^NSEI", 10).to_csv('NIFTY50.csv')