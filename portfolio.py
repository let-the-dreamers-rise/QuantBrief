import quantstats as qs
import pandas as pd
import os


if not os.path.exists("output"):
    os.makedirs("output")

# Extend pandas functionality
qs.extend_pandas()

stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"]
weights = [0.2, 0.2, 0.2, 0.2, 0.2]

portfolio_dict = dict(zip(stocks, weights))

print("\n === STOCK UNIVERSE ===")
print(portfolio_dict)

returns_df = pd.DataFrame()

for stock in stocks:
    returns_df[stock] = qs.utils.download_returns(stock)

print("\n Downloaded returns successfully")
print("\n=== INDIVIDUAL STOCK STATS ===")

performance = {}

for stock in stocks:
    data = returns_df[stock]

    cagr = qs.stats.cagr(data)
    sharpe = qs.stats.sharpe(data)
    drawdown = qs.stats.max_drawdown(data)
    vol = qs.stats.volatility(data)

    performance[stock] = cagr
    print(f"\n--- {stock} ---")
    print("CAGR:", round(cagr, 4))
    print("Sharpe:", round(sharpe, 4))
    print("Max Drawdown:", round(drawdown, 4))
    print("Volatility:", round(vol, 4))

ranking = sorted(performance.items(), key= lambda x: x[1], reverse=True)

print("\n=== STOCK RANKING (CAGR BASED) ===")
for r in ranking:
    print(r)

portfolio_returns = qs.utils.make_index(portfolio_dict, period="3y")
print("\nPortfolio created successfully")

print("\n=== CORRELATION WITH PORTFOLIO===")

for stock in stocks:
    corr = portfolio_returns.corr(returns_df[stock])
    print(stock, ":", round(corr, 4))

cov_matrix = returns_df.cov()
print("\n === COVARIANCE MATRIX ===")
print(cov_matrix)

cov_matrix.to_csv("output/ covariance_matrix.csv")

print("\n=== PORTFOLIO METRICS ===")
print("Portfolio CAGR:", qs.stats.cagr(portfolio_returns))
print("Portfolio Sharpe:", qs.stats.sharpe(portfolio_returns))
print("Portfolio Max DD:", qs.stats.max_drawdown(portfolio_returns))
print("Portfolio Volatility:", qs.stats.volatility(portfolio_returns))

qs.reports.html(portfolio_returns, benchmark="SPY", output="output/ full_portfolio_report.html")
portfolio_returns.plot_earnings(start_balance = 10000, savefig="output/portfolio_earnings.png")

portfolio_returns.plot_monthly_heatmap(savefig="output/portfolio_heatmap.png")

print("\nALL REPORTS SAVED INSIDE OUTPUT FOLDER")
print("\nAI INVESTOR PROTOTYPE READY ")

data["Return"] = data["Close"].pct_change()
data["Target"] = (data["Return"].shift(-1) > 0).astype(int)
data = data.dropna()

features = ["RSI", "SMA", "MACD_12_26_9"]



#Train ML Model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X = data[features]
y = data["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestClassifier()
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Prediction Accuracy:", accuracy_score(y_test, pred))

latest_data = data[features].iloc[-1].values.reshape(1, -1)
prediction = model.predict(latest_data)

if prediction[0] == 1:
    print("📈 Model says: PRICE WILL GO UP")
else:
    print("📉 Model says: PRICE WILL GO DOWN")