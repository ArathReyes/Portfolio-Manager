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
Now, select the type of portfolio:
```console
foo@bar:~$ whoami
foo
```
