import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Request data from Coingecko API
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=USD&days=1&interval=hourly"
response = requests.get(url)
data = response.json()

# Extract timestamps and values from API data
timestamps = [datetime.fromtimestamp(ts/1000) for ts, _ in data["prices"]]
market_caps = [cap for _, cap in data["market_caps"]]
volumes = [vol for _, vol in data["total_volumes"]]
prices = [price for _, price in data["prices"]]

# Create three separate plots for market capitalization, volume, and price
fig, axs = plt.subplots(3, 1, figsize=(12, 12))
axs[0].plot(timestamps, market_caps, label="Market Capitalization")
axs[0].set_title("Bitcoin Market Capitalization")
axs[0].set_xlabel("Date")
axs[0].set_ylabel("Market Capitalization (USD)")
axs[1].plot(timestamps, volumes, label="Volume")
axs[1].set_title("Bitcoin Volume")
axs[1].set_xlabel("Date")
axs[1].set_ylabel("Volume (USD)")
axs[2].plot(timestamps, prices, label="Price")
axs[2].set_title("Bitcoin Price")
axs[2].set_xlabel("Date")
axs[2].set_ylabel("Price (USD)")

# Format x-axis to show dates every 365 days
for ax in axs:
    ax.xaxis.set_tick_params(rotation=90)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))

# Save the plots as files
plt.tight_layout()
axs[0].get_figure().savefig("bitcoin_marketsummary_hourly_day.png")
