# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:29:11 2022

@author: Arath Reyes
"""
import importlib
from portfolio_optimizer import Portfolio
#import portfolio_optimizer
#importlib.reload(portfolio_optimizer)

# Test
    
#market = "^IXIC"
market = "^GSPC"
#tickers = ["TSLA","WMT","GOOG","AMZN"]
#tickers = ["MSFT","C","META","NVDA", "JPM", "WMT", "AMZN"]
#tickers = ["MSFT","NVDA","META","AMD","AAPL","IBM","INTC","NFLX","ORCL","PYPL"]
#tickers = ["BAC","BRK.B","BLK","C","CB","BEN","GS","JPM","MS","WFC"]
tickers = ["JPM","BAC","C","MS","WFC"]
start_date = "2021-1-1"
end_date = "2022-4-1"


MyPortfolio = Portfolio()
MyPortfolio.compute(tickers,market, start_date = start_date, end_date = end_date)

nsim = 7500
MyPortfolio.plot_efficient_frontier(nsim)

print(MyPortfolio)
