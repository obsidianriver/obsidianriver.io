import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Load data from the CoinGecko API
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=max'
response = requests.get(url)
data = response.json()
prices = data['prices']

# Create dataframe
df = pd.DataFrame(prices, columns=['time', 'price'])

# Convert unix timestamps to dates
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Set index to date column
df.set_index('time', inplace=True)

# Calculate all-time high price and date
df['All-time high'] = df['price'].cummax()
df['Days since all-time high'] = (df.index.max() - df.index) / pd.Timedelta(days=1)

# Find time periods where all-time highs were reached
all_time_highs = []
for year in range(df.index.year.min() + 1, df.index.year.max() + 1):
    start_date = pd.to_datetime(str(year) + '-01-01')
    end_date = pd.to_datetime(str(year + 1) + '-01-01')
    start_price = df.loc[start_date, 'All-time high']
    end_price = df.loc[df.index < end_date, 'price'].max()
    if end_price == start_price:
        all_time_highs.append({'date': start_date, 'price': start_price})

# Create bar chart
fig, ax = plt.subplots(figsize=(16, 9))
df.plot(ax=ax, y='price', color='gray', alpha=0.5)
df.plot(ax=ax, y='All-time high', color='green')

# Plot all-time high points
for ath in all_time_highs:
    ax.scatter(ath['date'], ath['price'], marker='o', s=100, color='red')

# Linear regression for all-time high points
x = pd.to_numeric(pd.Series([ath['date'] for ath in all_time_highs])).values
y = pd.Series([ath['price'] for ath in all_time_highs]).values
slope, intercept = np.polyfit(x, y, deg=1)

# Extrapolate all-time high trend
new_x = pd.Series(pd.date_range(start='2021-01-01', end='2025-01-01', freq='YS')).values
new_slope = slope
new_intercept = intercept
new_poly_fit = pd.Series(np.poly1d([new_slope, new_intercept])(pd.to_numeric(new_x)), index=new_x)
ax.plot(new_poly_fit, color='red', linestyle='--', linewidth=2)

# Add event markers
ax.axvline(datetime(year=2016, month=7, day=9), color='blue', linestyle='--', linewidth=2)
ax.text(datetime(year=2016, month=7, day=9), 300, "2016 Halving", rotation=90)

ax.axvline(datetime(year=2020, month=5, day=11), color='purple', linestyle='--', linewidth=2)
ax.text(datetime(year=2020, month=5, day=11), 300, "2020 Halving", rotation=90)

ax.axvline(datetime(year=2024, month=4, day=27), color='orange', linestyle='--', linewidth=2)
ax.text(datetime(year=2024, month=4, day=27), 300, "2024 Projected Halving", rotation=90)

# Set y-axis to log scale
ax.set_yscale('log')

# Set y-axis label
ax.set_ylabel('Price (USD)')

# Set plot title
ax.set_title('Bitcoin New All-Time Highs Trend With Projection')

# Save plot to file
plt.savefig('bitcoin_alltimehighstrend.png')
