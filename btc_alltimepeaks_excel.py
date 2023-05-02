import requests
import datetime
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=USD&days=max&interval=daily"
response = requests.get(url)
data = response.json()

# Initialize variables for tracking all-time highs and lows
all_time_high_price = float('-inf')
all_time_high_date = None
all_time_high_days = None

# Create an empty list to store the data
all_time_highs = []

# Loop through the historical prices and track all-time highs and lows
for price in data["prices"]:
    current_price = price[1]
    current_date = datetime.datetime.fromtimestamp(price[0] / 1000).strftime('%Y-%m-%d')

    # Check for a new all-time high
    if current_price > all_time_high_price:
        if all_time_high_date:
            all_time_high_days = (datetime.datetime.strptime(current_date, '%Y-%m-%d') - datetime.datetime.strptime(all_time_high_date, '%Y-%m-%d')).days
            all_time_highs.append({"New all-time high": all_time_high_price, "Date": all_time_high_date, "Days since previous all-time high": all_time_high_days})
        all_time_high_price = current_price
        all_time_high_date = current_date
    if all_time_high_date:
        all_time_high_days = (datetime.datetime.today() - datetime.datetime.strptime(all_time_high_date, '%Y-%m-%d')).days
        all_time_highs.append({"All-time high": all_time_high_price, "Date": all_time_high_date, "Days since previous all-time high": all_time_high_days})

# Create a dataframe from the list of all-time highs and lows
df = pd.DataFrame(all_time_highs)

# Save the dataframe to an Excel file
df.to_excel("all_time_highs.xlsx", index=False)
