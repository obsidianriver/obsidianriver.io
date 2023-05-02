import requests
import datetime

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=USD&days=max&interval=daily"
response = requests.get(url)
data = response.json()

# Initialize variables for tracking all-time highs and lows
all_time_high_price = float('-inf')
all_time_high_date = None
all_time_high_days = None

# Open a file for writing
with open('all_time_highs.txt', 'w') as f:
    # Loop through the historical prices and track all-time highs and lows
    for price in data["prices"]:
        current_price = price[1]
        current_date = datetime.datetime.fromtimestamp(price[0] / 1000).strftime('%Y-%m-%d')

        # Check for a new all-time high
        if current_price > all_time_high_price:
            if all_time_high_date:
                all_time_high_days = (datetime.datetime.strptime(current_date, '%Y-%m-%d') - datetime.datetime.strptime(all_time_high_date, '%Y-%m-%d')).days
                f.write(f"Days since previous all-time high: {all_time_high_days}\n")
            all_time_high_price = current_price
            all_time_high_date = current_date
            f.write(f"New all-time high: ${all_time_high_price:.3f} on {all_time_high_date}\n")

    if all_time_high_date:
        all_time_high_days = (datetime.datetime.today() - datetime.datetime.strptime(all_time_high_date, '%Y-%m-%d')).days
        f.write(f"Days since previous all-time high: {all_time_high_days}\n")
    f.write(f"\nAll-time high: ${all_time_high_price:.3f} on {all_time_high_date}")
