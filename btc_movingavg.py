import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Request data from Coingecko API
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=USD&days=1460&interval=daily"
response = requests.get(url)
data = response.json()

# Extract timestamps and values from API data
timestamps = [datetime.fromtimestamp(ts/1000) for ts, _ in data["prices"]]
prices = [price for _, price in data["prices"]]

# Calculate moving averages
sma50 = []
sma200 = []
sma300 = []

for i in range(len(prices)):
    if i >= 49:
        sma50.append(sum(prices[i-49:i+1])/50)
    if i >= 199:
        sma200.append(sum(prices[i-199:i+1])/200)
    if i >= 299:
        sma300.append(sum(prices[i-299:i+1])/300)

# Create a plot for Bitcoin price and moving averages
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(timestamps, prices, label="Price")
ax.plot(timestamps[49:], sma50, label="SMA50")
ax.plot(timestamps[199:], sma200, label="SMA200")
ax.plot(timestamps[299:], sma300, label="SMA300")
ax.set_title("Bitcoin Price and Moving Averages")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()

# Format x-axis to show dates every 365 days
ax.xaxis.set_tick_params(rotation=90)
ax.xaxis.set_major_locator(plt.MaxNLocator(10))

# Save the plot as a file
plt.tight_layout()
fig.savefig("bitcoin_movingavg.png")
