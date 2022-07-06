# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 20:52:53 2022

@author: Arath Alejandro Reyes López
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
import yfinance as yf
from datetime import datetime, timedelta

def Download_Data(market, tickers, start_date = None, end_date = None):
    # Date: YYYY-MM-DD
    data = yf.download([market] + tickers, start = start_date, end = end_date)["Adj Close"]
    data = data.dropna()
    
    
    start_date = str(data.index[0])[:-9]
    end_date = str(data.index[-1])[:-9]
    log_returns = np.log(data/data.shift(1))
    
    return log_returns, start_date, end_date

def compute_portfolio_variance(x, covariance_matrix):
    variance = np.dot(x.T, np.dot(covariance_matrix, x)).item()
    return variance

def compute_sharpe_ratio(x, covariance_matrix, mean_ret, rate):
    sharpe_ratio = (np.transpose(mean_ret).dot(x).item() - rate) / np.sqrt(np.dot(x.T, np.dot(covariance_matrix, x))).item()
    return -sharpe_ratio # To maximize

def get_target(min_ret, max_ret):
    while True:
        try:
            target = float(input("\nEnter the expected target return between {0} and {1}: ".format(min_ret, max_ret)))
        except ValueError:
            print("\nValue Error! You must enter a number, try again!")
            continue
        if min_ret <= target <= max_ret:
            break
        else:
            print("\nThe target return given is not admissible. Try again!")
    return target
    
def Markowitz_Portfolio(size, cov_mat, mean_ret, target):
    # initialise optimisation
    x = np.zeros([size,1])
    # initialise constraints
    cons = [{"type": "eq", "fun": lambda x: np.transpose(mean_ret).dot(x).item() - target},\
            {"type": "eq", "fun": lambda x: sum(abs(x)) - 1}]
    bnds = [(0, None) for i in range(size)]
    # compute optimisation
    res = minimize(compute_portfolio_variance, x, args=(cov_mat), constraints=cons, bounds=bnds)
    weights =  res.x
    return weights

def Maximum_Sharpe_Ratio_Portfolio(size, cov_mat, mean_ret, rate):
    # initialise constraints
    cons = [{"type": "eq", "fun": lambda x: sum(abs(x)) - 1}]
    bnds = tuple((0,1) for i in range(size))
    # compute optimisation
    res = minimize(compute_sharpe_ratio, size*[1/size],  method = "SLSQP", args=(cov_mat, mean_ret, rate), constraints=cons, bounds=bnds)
    weights =  res.x
    return weights

def Minimum_Variance_Portfolio(size, cov_mat):
    # initialise optimisation
    x = np.zeros([size,1])
    # initialise constraints
    cons = [{"type": "eq", "fun": lambda x: sum(abs(x)) - 1}]
    bnds = [(0, None) for i in range(size)]
    # compute optimisation
    res = minimize(compute_portfolio_variance, x, args=(cov_mat), constraints=cons, bounds=bnds)
    weights =  res.x
    return weights

def get_weights(size): # For custom portfolio
    while True:
        try:
            weights = list(map(float,input("\nEnter the weights of your portfolio: ").strip().split()))#[:size]
        except ValueError:
            print("\nValue Error!, Enter decimal numbers only")
            continue
        
        if np.abs(weights).sum() != 1:
            print("\nThe sum of your weights should be equal to 1, Try again!")
            continue
        elif len(weights) != size:
            print("\nYou are not entering the same amount of numbers as the size\
                  of your portfolio!, Try again!")
            continue
        else:
            break
    return np.array(weights)

def compute_betas(log_returns, weights, market, tickers):
    from scipy.stats import linregress
    log_returns = log_returns.dropna()
    Market = log_returns[market]
    betas = []
    for name in tickers:
        Stock = log_returns[name]
        betas.append(linregress(Market, Stock)[0])
        
    
    df = pd.DataFrame({"Beta ("+market+")":betas}, index = tickers)
    x = df.T.dot(weights)["Weights"].values[0]
    betas = pd.DataFrame({"Beta ("+market+")":betas+[x]}, index = tickers+["Portfolio"])
    return betas
        

class Portfolio:
    
    def __init__(self):
        
        self.expected_return = None
        self.volatility = None
        self.tickers = None # Mandatory
        self.weights = None 
        self.notional= None # Mandatory (1 dflt)
        self.type = None # Mandatory
        self.sharpe = None # Output
        self.start_date = None # Input
        self.end_date = None # Input
        self.betas = None
        self.rate = None # Risk Free Rate, for Sharpe Calculations
        self.market = None # For Beta Calculations
        self.target = "Only available for Markowitz portfolios" # Markowwitz
        self.variance_explained = "Only available for PCA portfolios" # for PCA
        self.alpha = None
        self.VaR = None
        self.CVaR = None
        self.risk_summary = None
        self.mean_returns = None
        self.cov_mat = None

        
        
    def compute(self, tickers, market, rate = 0.0, notional = 1, start_date = None,\
                end_date = None):
        
        menu = {1:"Markowitz",2:"PCA",3:"Maximum Sharpe Ratio",4:"Minimum Variance",\
                5:"Equi Weighted",6: "Custom"}
        message = "\n~~~~~~~~~~~~~~~~~~~~~~\n\
        MENU\n\
~~~~~~~~~~~~~~~~~~~~~~\n\
[1] Markowitz\n\
[2] PCA\n\
[3] Maximum Sharpe Ratio\n\
[4] Minimum Variance\n\
[5] Equi Weighted\n\
[6] Custom"
        while True:
            print(message)
            try:
                print("\n")
                portfolio_type = int(input("Select your portfolio type: "))
            except ValueError:
                print("\nValue Error!, Select a number from above")
                continue
            if portfolio_type in menu.keys():
                break
            else:
                print("\nInvalid Portfolio Type!, Select a number from above\n")
        self.type = menu[portfolio_type]
        
        # Download Data
        self.market = market
        self.tickers = tickers
        
        log_returns, self.start_date, self.end_date = Download_Data(market,\
                                                             tickers,\
                                                             start_date = start_date,\
                                                             end_date = end_date)
        log_returns = log_returns[[market]+tickers]
        size = len(tickers)


        market_returns = log_returns[[market]]
        tickers_returns = log_returns[tickers]
        mean_ret = tickers_returns.mean()*252 # Rendimientos
        min_ret = min(mean_ret)
        max_ret = max(mean_ret)
        cov_mat = tickers_returns.cov()*252 # Matriz de covarianzas
        cov_mat = cov_mat.values
        
        if portfolio_type == 1:
            target = get_target(min_ret, max_ret)
            weights = Markowitz_Portfolio(size, cov_mat, mean_ret, target)
        elif portfolio_type == 2:
            pass
        elif portfolio_type == 3:
            weights = Maximum_Sharpe_Ratio_Portfolio(size, cov_mat, mean_ret, rate)
        elif portfolio_type == 4:
            weights = Minimum_Variance_Portfolio(size, cov_mat)
        elif portfolio_type == 5:
            weights = np.array(size*[1/size])
        else:
            weights = get_weights(size)
        
        self.weights = pd.DataFrame({"Weights":weights}, index = tickers)
        self.expected_return = np.transpose(mean_ret).dot(weights).item()
        self.volatility = np.sqrt(compute_portfolio_variance(weights, cov_mat))
        self.Sharpe = -compute_sharpe_ratio(weights, cov_mat, mean_ret, rate)
        self.betas = compute_betas(log_returns, self.weights, market, tickers)
        self.Treynor = (self.expected_return - rate) / self.betas["Beta ("+market+")"]["Portfolio"]
        self.cov_mat = cov_mat
        self.mean_returns = mean_ret
        self.rate = rate
        self.notional = notional
        return None
    
    def plot_efficient_frontier(self, nsim = 2500):
        size = len(self.tickers)
        min_ret = min(self.mean_returns)
        max_ret = max(self.mean_returns)
        returns = min_ret + np.linspace(0.01,0.99,1000) * (max_ret-min_ret)
        volatilities = np.zeros([len(returns),1])
        counter = 0
        for target in returns:
            w = Markowitz_Portfolio(size, self.cov_mat, self.mean_returns, target)
            volatilities[counter] = np.sqrt(np.dot(w.T, np.dot(self.cov_mat, w)))
            counter += 1
        volatilities = [i[0] for i in volatilities]
        #frontera = pd.DataFrame({"Volatility":volatilities,"Return":returns})
        port_returns = []
        port_vol = []
        port_w = []
        for _ in range(nsim):
            w = np.random.random(size)
            w /= np.sum(w)
            port_w.append(w)
            port_returns.append(np.sum(w *self.mean_returns))
            port_vol.append(np.sqrt(np.dot(w.T, np.dot(self.cov_mat, w))))
                    
        port_returns = np.array(port_returns)
        port_vol = np.array(port_vol)     
        portfolios = pd.DataFrame({"Weights":port_w,'Return': port_returns, 'Volatility':port_vol})
        portfolios["Sharpe"] = (portfolios["Return"] - self.rate)/portfolios["Volatility"]
        myPort = pd.DataFrame({"Volatility":[self.volatility], "Return":self.expected_return})
        
        sns.set_style("darkgrid")
        plt.figure(figsize = (15,15))
        ax = sns.scatterplot(x = "Volatility",y = "Return",data = portfolios, hue = "Sharpe",\
                             palette='plasma',linewidth=0)
        sns.scatterplot(x = volatilities,y = returns, linewidth=0, color = "black", s = 15)
        sns.scatterplot(x = "Volatility",y = "Return", data = myPort, color = "#0D88F5",\
                        label = "My Portfolio",s = 350, marker="*", linewidth = 1)
        ax.set_title("Admissible Portfolios",fontsize = '25')
        ax.set_ylabel("Expected Returns",fontsize = "15")
        ax.set_xlabel("Expected Volatility\nTickers: {0} | Market: {1}\nRisk Free Rate: {2} | Start Date: {3} | End Date: {4}\nType: {5} | Weights: {6} | #Simulations: {7}\n\
                      Sharpe: {8} | Beta: {9} | Treynor: {10}".format(self.tickers, self.market, self.rate, self.start_date,\
                      self.end_date, self.type, np.round(self.weights["Weights"].values,3),\
                      nsim, np.round(self.Sharpe,3), np.round(self.betas.iloc[-1,0],3), np.round(self.Treynor,3) ),fontsize = "15")
        plt.show()
              
        return None
    
    def __str__(self):
        string ="\n                 SUMMARY         \n\
-------------------------------------------\n\
+ Type of Portfolio: {0}\n\
+ Stocks: {1}\n\
+ Market: {2}\n\
+ Weights: {3}\n\
+ Expect Return: {4}\n\
+ Volatility: {5}\n\
+ Risk Free Rate: {6}\n\
+ Notional: {7}\n\
+ Beta: {8}\n\
+ Sharpe Ratio: {9}\n\
+ Treynor Ratio: {10}\n\
+ Start Date: {11}\n\
+ End Date: {12}".format(self.type,self.tickers, self.market,\
np.round(self.weights["Weights"].values, 3),np.round(self.expected_return,3),\
np.round(self.volatility,3), self.rate, self.notional, np.round(self.betas.iloc[-1,0],3),\
np.round(self.Sharpe,3), np.round(self.Treynor,3), self.start_date, self.end_date)

        return string
