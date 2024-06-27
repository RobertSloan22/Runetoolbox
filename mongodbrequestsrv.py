from pymongo import MongoClient
import pandas as pd

# MongoDB connection details
client = MongoClient('')

# Define the filter and projection for the query
filter = {}
project = {
    'rune_name': 1,
    'MarketCapUSD': 1,
    'holders': 1,
    'price_sats': 1,
    'price_usd': 1,
    'price_change': 1,
    'volume_1h_btc': 1,
    'volume_1d_btc': 1,
    'volume_7d_btc': 1,
    'volume_total_btc': 1,
    'sales_1h': 1,
    'sales_1d': 1,
    'sales_7d': 1,
    'sellers_1h': 1,
    'sellers_1d': 1,
    'sellers_7d': 1,
    'buyers_1h': 1,
    'buyers_1d': 1,
    'buyers_7d': 1,
    'listings_min_price': 1,
    'listings_max_price': 1,
    'listings_avg_price': 1,
    'listings_percentile_25': 1,
    'listings_median_price': 1,
    'listings_percentile_75': 1,
    'count_listings': 1,
    'listings_total_quantity': 1,
    'balance_change_last_1_block': 1,
    'balance_change_last_3_blocks': 1,
    'balance_change_last_10_blocks': 1
}

# Fetch the data
result = client['runes']['GinidataRunes'].find(filter, projection=project)

# Convert the MongoDB cursor to a list and then to a DataFrame
data = list(result)
df = pd.DataFrame(data)
