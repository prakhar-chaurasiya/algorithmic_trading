import datetime
import numpy as np
import pandas as pd
from urllib.request import urlopen

def loadprices(symbol, years=1):
  end = ((datetime.date.today() - datetime.date(1970, 1, 2)).days)*24*3600
  start = end - years*365*24*3600
  if(symbol[0] == '^'):
    symbol = symbol.upper()
  else:
    symbol = symbol.upper() +'.NS'
  link = 'https://query1.finance.yahoo.com/v7/finance/download/'+ symbol +'?period1='+ str(start) + '&period2='+ str(end) +'&interval=1d&events=history&includeAdjustedClose=true'
  f = urlopen(link)
  data = f.read()
  data = data.decode('utf-8')
  data = data.split('\n')
  daily_adjusted_close = []
  for line in data[1:]:
    row = line.split(',')
    try:
      daily_adjusted_close.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])])
    except:
      pass
  df_close = pd.DataFrame(daily_adjusted_close, columns=['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
  df_close['date'] = pd.to_datetime(df_close['date'])
  return df_close.set_index('date')

def saveprices(symbol, years=1):
  df = loadprices(symbol=symbol, years=years)
  if(symbol[0] == '^'):
    name = symbol[1:].upper()
  else:
    name = symbol
  df.to_csv(f'{name}.csv')