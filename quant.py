import quantstats as qs
stock = "MSFT"
portpolio = qs.utils.download_returns(stock, period='3y')
print(f"Sharpe:  {qs.stats.sharpe(portpolio)}")
print(f"best day: {qs.stats.best(portpolio)}")
qs.extend_pandas()
print(portpolio.cagr())
print(portpolio.max_drawdown())
print(portpolio.monthly_returns())
