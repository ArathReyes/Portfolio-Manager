# Portfolio-Manager


Import portfolio_optimizer:

```python
from portfolio_optimizer import Portfolio
```

Define your market, tickers, start date and end date:

```python
market = "^GSPC"
tickers = ["TSLA","WMT","GOOG","AMZN"]
start_date = "2021-1-1"
end_date = "2022-4-1"
```
Construct your portfolio:

```python
MyPortfolio = Portfolio()
MyPortfolio.compute(tickers,market, start_date = start_date, end_date = end_date)
```
Now, select the type of portfolio by typing in your terminal one of the options showed in the menu:
```console
~~~~~~~~~~~~~~~~~~~~~~
        MENU
~~~~~~~~~~~~~~~~~~~~~~
[1] Markowitz
[2] PCA
[3] Maximum Sharpe Ratio
[4] Minimum Variance
[5] Equi Weighted
[6] Custom



Select your portfolio type:
```

For example, select the third option, i.e., Maximum Sharpe Ratio:

```console
~~~~~~~~~~~~~~~~~~~~~~
        MENU
~~~~~~~~~~~~~~~~~~~~~~
[1] Markowitz
[2] PCA
[3] Maximum Sharpe Ratio
[4] Minimum Variance
[5] Equi Weighted
[6] Custom



Select your portfolio type: 3
[*********************100%***********************]  5 of 5 completed
```
Now, lets plot the efficient frontier and the admissible portfolios using Monte Carlo simulation. Select the number of simulations:
```python
nsim = 7500
```
Lets run the simulation:

```python
MyPortfolio.plot_efficient_frontier(nsim)
```

You should expect a plot like follows:



Finally, show a summary with relevant metrics of the portfolio constructed:

```console
                 SUMMARY         
-------------------------------------------
+ Type of Portfolio: Maximum Sharpe Ratio
+ Stocks: ['TSLA', 'WMT', 'GOOG', 'AMZN']
+ Market: ^GSPC
+ Weights: [0. 0. 1. 0.]
+ Expect Return: 0.386
+ Volatility: 0.263
+ Risk Free Rate: 0.0
+ Notional: 1
+ Beta: 1.301
+ Sharpe Ratio: 1.47
+ Treynor Ratio: 0.297
+ Start Date: 2021-01-04
+ End Date: 2022-03-31
```


