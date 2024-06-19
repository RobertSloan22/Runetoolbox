fullstacktacodev
fullstacktacodev
Online

Cubs — Today at 8:23 PM
yeah looms are dope af
and sick
it went up another 5% in price while u watched the video lol
and tbh it might be a bad time to sell, but that's a huge W we're taking it and will ride the rest for free
my geniidata account keeps running into that scheduled job you're running lol
Image
I wonder if that script ever hits errors because I'm running other sqls
that we don't see
fullstacktacodev — Today at 8:30 PM
is that the same gini data script you gave me?
ok so i initially ran into a cursor error in the logs when i first ran that a while back i thought it was something i did so i fixed it and its been running good since i just checked the logs and system staus for the service running it on th server and we all look good i included here the corrected code im running from the updated sql query you gave me
Image
Image
  File "/home/robert/Datascience/newsql.py", line 288, in create_table_if_not_exists
    cursor.close()
    ^^^^^^
UnboundLocalError: cannot access local variable 'cursor' where it is not associated with a value
Traceback (most recent call last):
  File "/home/robert/Datascience/newsql.py", line 407, in <module>
Expand
message.txt
9 KB
import time
import json
import cloudscraper
import psycopg2
from psycopg2 import sql

# Constants
API_URL_RUN = "https://www.geniidata.com/api/dashboard/query/run"
API_URL_STATUS = "https://www.geniidata.com/api/dashboard/query/status"
API_URL_DATA = "https://www.geniidata.com/api/dashboard/chart/data"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://studio.geniidata.com",
    "referer": "https://studio.geniidata.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-csrf-token": "vACNHtxV-RXPmPf_n9dT0GU5inJhTK6zRa3A",
    "cookie": "geniidata.sid=s%3ARjPuTfc9BgJsxnNpBE-ujLretN7mkv24.xguP8Txh%2BO3%2BQF0sv4Oqx8fQNTJSRptJGxv7Ym%2Fhj%2Fw; theme=dark; _gcl_au=1.1.1524685981.1716595779.1126843500.1716595834.1716595833; _gid=GA1.2.1187319215.1717218055; _ga=GA1.1.1710745345.1711734543; _ga_3XP1XSS13R=GS1.1.1717716373.79.1.1717716376.0.0.0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "priority": "u=1, i"
}

SQL_QUERY = {
    "worksheetId": 127325,
    "sql": """
-- Common Table Expressions (CTEs) to aggregate data from runes.fact_listings
WITH latest_time AS (
    SELECT
        rune_name,
        marketplace,
        MAX(time) AS latest_time
    FROM runes.fact_listings
    GROUP BY rune_name, marketplace
),
latest_data AS (
    SELECT
        f.rune_name,
        f.marketplace,
        f.time AS latest_time,
        f.price_sats,
        f.quantity
    FROM runes.fact_listings f
    JOIN latest_time l ON f.rune_name = l.rune_name AND f.marketplace = l.marketplace AND f.time = l.latest_time
),
aggregated_data AS (
    SELECT
        rune_name,
        MIN(price_sats) AS min_price,
        MAX(price_sats) AS max_price,
        AVG(price_sats) AS avg_price,
        COUNT(price_sats) AS count_listings,
        SUM(quantity) AS total_quantity
    FROM latest_data
    GROUP BY rune_name
),
percentile_ranks AS (
    SELECT
        rune_name,
        price_sats,
        NTILE(4) OVER (PARTITION BY rune_name ORDER BY price_sats) AS price_ntile
    FROM latest_data
),
percentile_agg AS (
    SELECT
        rune_name,
        MAX(CASE WHEN price_ntile = 1 THEN price_sats END) AS percentile_25,
        MAX(CASE WHEN price_ntile = 2 THEN price_sats END) AS median_price,
        MAX(CASE WHEN price_ntile = 3 THEN price_sats END) AS percentile_75
    FROM percentile_ranks
    GROUP BY rune_name
),
final_aggregated_data AS (
    SELECT
        l.rune_name,
        MAX(l.latest_time) AS latest_time,
        a.min_price,
        a.max_price,
        a.avg_price,
        p.percentile_25,
        p.median_price,
        p.percentile_75,
        a.count_listings,
        a.total_quantity
    FROM latest_data l
    JOIN aggregated_data a ON l.rune_name = a.rune_name
    JOIN percentile_agg p ON l.rune_name = p.rune_name
    GROUP BY l.rune_name, a.min_price, a.max_price, a.avg_price, p.percentile_25, p.median_price, p.percentile_75, a.count_listings, a.total_quantity
),

-- Determine the maximum block height
MaxBlockHeight AS (
    SELECT MAX(block_height) AS max_block_height
    FROM runes.fact_balance_delta
... (308 lines left)
Collapse
message.txt
16 KB
fullstacktacodev — Today at 8:39 PM
that is two different tools i had to check the status of the sql query code that is included here after i corrected it, i also had a weird error but thought it was related to something i did, basically had chat gpt debug it with me and correct the code. so the corrected code is on the bottom there under the error log from a the first run .
Image
Do we  look good on this what the fuck is with the error on the bottm
Cubs — Today at 8:56 PM
nice, yeah bro we gotttttta put all this code into github repos too so we're not copy/pasting it and always both have easy access to the latest code that's running in production. Trust me it'll make us both work faster together another one of those things that's a few minutes invested now saves us hours later
bc like for example, it should be set up so that when our github code is pushed, into the repo.. that the hosted jobs are re-deployed
best way to manage open source
fullstacktacodev
 started a call that lasted a few seconds.
 — Today at 8:58 PM
Cubs — Today at 8:58 PM
like in fact, that's better than me needing access to the code running in the server
fullstacktacodev — Today at 8:59 PM
Sorry I accidentally called just then
Yes 👍
All code goes in github starting now, my apologies I forgot completely about that
Cubs — Today at 8:59 PM
ur good bro
ur doing a lot and they aren't small things
fullstacktacodev — Today at 9:00 PM
Had a lot of domain jumping around
Yeah
Cubs — Today at 9:00 PM
I just think a lot of these small little organization things will help u be more dynamic and flexible to bounce everywhere and again when I can help with stuff too and we share our skills it's unstoppable
fullstacktacodev — Today at 9:01 PM
Agreed in full.
Cubs — Today at 9:01 PM
did I ever mention I wish there were 45 hours in the day?? 
lol
fullstacktacodev — Today at 9:05 PM
Il start tonight with adding code up to github. I am still going to get you full file system access. I did a lot of research on the Linux os, and I have all my stuff in my home directory, which is unaccessable to other users, so I’m going to move stuff to a shared directory that sits closer to the root of the system , I tried this but I made the shared directory inside my home directory and that does not work. Linux you have /root/users/Robert or ryan or who ever/ home. So il put it all in /root/shared/ and we will be good
I know that’s a fun read..
Cubs — Today at 9:05 PM
but yeah bro I don't need access to any files
if u have it all in github
fullstacktacodev — Today at 9:06 PM
Bitcoin
Node
Cubs — Today at 9:06 PM
oh
yeah
hmm
fullstacktacodev — Today at 9:06 PM
It’s not a big deal
Cubs — Today at 9:06 PM
no
not rn
fullstacktacodev — Today at 9:06 PM
It’s several lines of code
To move stuff
Cubs — Today at 9:06 PM
also that's lower priority
fullstacktacodev — Today at 9:06 PM
So it’s fine
Ok
Cubs — Today at 9:06 PM
bitcoin node will be after data stuff
bitcoin is when we need to actually automate the transactions
and trading
fullstacktacodev — Today at 9:06 PM
I just literally got that insight yesterday
Ok
Forsure. Tomorrow let’s task prioritize
I will put code to GitHub
Cubs — Today at 9:07 PM
oh reread this lol well if it's not a crazy task then yeah it's nice to have for sure, but if u get stuck in a rabbit hole skip it
yeupp sounds good ser
fullstacktacodev — Today at 9:08 PM
Cool, no I just poped out the other side of the rabbit hole lol been through it and back out again
So no digging needed
Cubs — Today at 9:08 PM
lol good
I get stuck in em sometimes
a lot of the work we do requires rabbit holes ha
fullstacktacodev — Today at 9:09 PM
I think it’s one big rabbit hole
With nodes of smaller rabbit holes tangled
Like Christmas lights
Lol.. ok so we’re good on the splitting part of that process correct ? With the runes? Did you see the pic I sent. I’m about to check magic Eden now
Yep we’re good
Image
so list and sell the two 5000 ones
Image
listed
I do need to ask, maybe tomorrow you can add some clarification, in the video you sent, you were eager to buy the bobmarley runes, when they were nearly minted out. Is that normally when you want to buy?
fullstacktacodev — Today at 9:16 PM
So, would it be better to not jump in on runes if they are in the lower quartile of the minting process or even the first half?
DSK- DOMAIN- SPECIFIC -KNOWLEDGE -
fullstacktacodev — Today at 9:29 PM
https://www.loom.com/share/dab8b9aa7df740a299dedb0afb63bc3b?sid=e80a1f41-dcc0-4f17-9180-cf2596028a56
Loom
Monitoring System Overview
Hey, in this video, I showcase our monitoring system setup. I demonstrate how I monitor services through a docker container on a remote desktop environment. I highlight the server oversight system, address recent service failures, and explain how to check service status. No action requested.
Image
Cubs — Today at 9:32 PM
sick, bro I've always wanted to be working on a hard metal server like this. AMazing stuff
fullstacktacodev — Today at 9:33 PM
Were getting there man, this will be a smooth running operation
Cubs — Today at 9:41 PM
yessirrrr
fullstacktacodev — Today at 10:08 PM
Dude I have access to the server terminal via my cell phone in this video I check the sql data status
Cubs — Today at 10:12 PM
ok now that's sick as fuck!
fullstacktacodev — Today at 10:12 PM
I know right .... pretty fuckijng dope i was geekijng out hard a few min ago
dude there are different apps for connecting to servers remotly for phones just download one and use the login address and credentials and you can prob access the GUI with one
i mean if you wanted
Cubs — Today at 10:16 PM
yeah I mean for some things I will I need to buy a phone after my surgery
oh btw u have my other number right???
lol
whoops if not
if u've been trying to text me like the last 3 weeks or so I haven't had that phone
fullstacktacodev — Today at 10:16 PM
no i dont think i do
i have not messaged you on anything other then discord in a while
Cubs — Today at 10:16 PM
lol okay sounds good phew
I've had a lot of ppl mad at me
fullstacktacodev — Today at 10:17 PM
i tried but gave up when you were on vacation
Cubs — Today at 10:17 PM
genuinely pissed
lol it broke on vaca
fullstacktacodev — Today at 10:17 PM
yeah i remember you saying that.
you did put a message up on facebook
so long as you didnt ghost your mother
i wouldnt sweat it
lol
Cubs — Today at 10:19 PM
lol no I won't
https://www.loom.com/share/e9c32bbc3c06421b9c4206a0e1e558a5?sid=300f9c7d-d2a1-440d-9326-4b0c30af5a81
Loom
Exploring Loan Offers and Collateral with Crypto 🚀
Hey there! In this video, I dive into the world of crypto loans, showcasing how I connected to the SQL Server to run API calls from a CSV file created from Google Sheets. I manually inputted data for 281 rounds, explored borrowing against collateral, and shared insights on loan amounts and repayment terms. Check it out for a deep dive into the c...
Image
fullstacktacodev — Today at 10:49 PM
hey im winding it down man. long day, so good luck at the pre op in the morning hit me up when your trying to get on a call, i got some good stuff to go over.
﻿
import time
import json
import cloudscraper
import psycopg2
from psycopg2 import sql

# Constants
API_URL_RUN = "https://www.geniidata.com/api/dashboard/query/run"
API_URL_STATUS = "https://www.geniidata.com/api/dashboard/query/status"
API_URL_DATA = "https://www.geniidata.com/api/dashboard/chart/data"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://studio.geniidata.com",
    "referer": "https://studio.geniidata.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-csrf-token": "vACNHtxV-RXPmPf_n9dT0GU5inJhTK6zRa3A",
    "cookie": "geniidata.sid=s%3ARjPuTfc9BgJsxnNpBE-ujLretN7mkv24.xguP8Txh%2BO3%2BQF0sv4Oqx8fQNTJSRptJGxv7Ym%2Fhj%2Fw; theme=dark; _gcl_au=1.1.1524685981.1716595779.1126843500.1716595834.1716595833; _gid=GA1.2.1187319215.1717218055; _ga=GA1.1.1710745345.1711734543; _ga_3XP1XSS13R=GS1.1.1717716373.79.1.1717716376.0.0.0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "priority": "u=1, i"
}

SQL_QUERY = {
    "worksheetId": 127325,
    "sql": """
-- Common Table Expressions (CTEs) to aggregate data from runes.fact_listings
WITH latest_time AS (
    SELECT
        rune_name,
        marketplace,
        MAX(time) AS latest_time
    FROM runes.fact_listings
    GROUP BY rune_name, marketplace
),
latest_data AS (
    SELECT
        f.rune_name,
        f.marketplace,
        f.time AS latest_time,
        f.price_sats,
        f.quantity
    FROM runes.fact_listings f
    JOIN latest_time l ON f.rune_name = l.rune_name AND f.marketplace = l.marketplace AND f.time = l.latest_time
),
aggregated_data AS (
    SELECT
        rune_name,
        MIN(price_sats) AS min_price,
        MAX(price_sats) AS max_price,
        AVG(price_sats) AS avg_price,
        COUNT(price_sats) AS count_listings,
        SUM(quantity) AS total_quantity
    FROM latest_data
    GROUP BY rune_name
),
percentile_ranks AS (
    SELECT
        rune_name,
        price_sats,
        NTILE(4) OVER (PARTITION BY rune_name ORDER BY price_sats) AS price_ntile
    FROM latest_data
),
percentile_agg AS (
    SELECT
        rune_name,
        MAX(CASE WHEN price_ntile = 1 THEN price_sats END) AS percentile_25,
        MAX(CASE WHEN price_ntile = 2 THEN price_sats END) AS median_price,
        MAX(CASE WHEN price_ntile = 3 THEN price_sats END) AS percentile_75
    FROM percentile_ranks
    GROUP BY rune_name
),
final_aggregated_data AS (
    SELECT
        l.rune_name,
        MAX(l.latest_time) AS latest_time,
        a.min_price,
        a.max_price,
        a.avg_price,
        p.percentile_25,
        p.median_price,
        p.percentile_75,
        a.count_listings,
        a.total_quantity
    FROM latest_data l
    JOIN aggregated_data a ON l.rune_name = a.rune_name
    JOIN percentile_agg p ON l.rune_name = p.rune_name
    GROUP BY l.rune_name, a.min_price, a.max_price, a.avg_price, p.percentile_25, p.median_price, p.percentile_75, a.count_listings, a.total_quantity
),

-- Determine the maximum block height
MaxBlockHeight AS (
    SELECT MAX(block_height) AS max_block_height
    FROM runes.fact_balance_delta
),

-- Calculate the balance changes for the last 1 block, 3 blocks, and 10 blocks
RecentBalanceChanges AS (
    SELECT
        rune_name,
        SUM(CASE WHEN block_height >= (SELECT max_block_height FROM MaxBlockHeight) - 0 THEN abs(balance_delta) ELSE 0 END) AS balance_change_last_1_block,
        SUM(CASE WHEN block_height >= (SELECT max_block_height FROM MaxBlockHeight) - 2 THEN abs(balance_delta) ELSE 0 END) AS balance_change_last_3_blocks,
        SUM(CASE WHEN block_height >= (SELECT max_block_height FROM MaxBlockHeight) - 9 THEN abs(balance_delta) ELSE 0 END) AS balance_change_last_10_blocks
    FROM runes.fact_balance_delta
    GROUP BY rune_name
)


-- Final query combining data from runes.dim_tokens_info and the aggregated data
SELECT 
    current_timestamp as timestamp,
    INFO.rune_id,
    INFO.rune_name,
    INFO.supply * INFO.price_usd as MarketCapUSD,
    INFO.rune_number,
    INFO.symbol,
    INFO.etching_time,
    INFO.etching,
    INFO.inscription_id,
    INFO.turbo,
    INFO.amount,
    INFO.supply,
    INFO.burned,
    INFO.premine,
    INFO.minted,
    INFO.mints,
    INFO.holders,
    INFO.price_sats,
    INFO.price_usd,
    INFO.price_change,
    INFO.volume_1h_btc,
    INFO.volume_1d_btc,
    INFO.volume_7d_btc,
    INFO.volume_total_btc,
    INFO.sales_1h,
    INFO.sales_1d,
    INFO.sales_7d,
    INFO.sales_total,
    INFO.sellers_1h,
    INFO.sellers_1d,
    INFO.sellers_7d,
    INFO.buyers_1h,
    INFO.buyers_1d,
    INFO.buyers_7d,
    FAD.min_price as listings_min_price,
    FAD.max_price as listings_max_price,
    FAD.avg_price as listings_avg_price,
    FAD.percentile_25 as listings_percentile_25,
    FAD.median_price as listings_median_price,
    FAD.percentile_75 as listings_percentile_75,
    FAD.count_listings,
    FAD.total_quantity as listings_total_quantity,
    balance_change_last_1_block,
    balance_change_last_3_blocks,
    balance_change_last_10_blocks
FROM runes.dim_tokens_info AS INFO
LEFT JOIN final_aggregated_data AS FAD
ON INFO.rune_name = FAD.rune_name
LEFT JOIN RecentBalanceChanges
    on RecentBalanceChanges.rune_name = INFO.rune_name
ORDER BY INFO.supply * INFO.price_usd DESC;
    """,
    "debug": False
}

# Database connection details
DB_NAME = 'sandbox'
DB_USER = 'postgres'
DB_HOST = 'runes.csxbyr0egtki.us-east-1.rds.amazonaws.com'
DB_PASSWORD = 'uIPRefz6doiqQcbpM5po'
DB_PORT = '5432'

# Initialize the scraper
scraper = cloudscraper.create_scraper()

# Function to run the initial SQL query
def run_sql_query():
    try:
        response = scraper.post(API_URL_RUN, headers=HEADERS, data=json.dumps(SQL_QUERY).encode('utf-8'))
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error during SQL query request: {e}")
        return None

# Function to check the status of the query
def check_query_status(query_id):
    try:
        response = scraper.get(f"{API_URL_STATUS}?queryId={query_id}&checkNum={int(time.time()*1000)}", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error during status check request: {e}")
        return None

# Function to fetch the result data for a specific page
def fetch_query_data(page, page_size=100):
    body = json.dumps({
        "sort": None,
        "order": None,
        "pageSize": page_size,
        "page": page,
        "debug": False,
        "searchKey": "",
        "searchValue": "",
        "type": 1,
        "worksheetId": 127325
    }).encode('utf-8')
    try:
        response = scraper.post(API_URL_DATA, headers=HEADERS, data=body)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error during data fetch request: {e}")
        return None

# Function to create the table if it doesn't exist
def create_table_if_not_exists():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS runes_token_info_genii (
        timestamp TIMESTAMPTZ,
        rune_id TEXT,
        rune_name TEXT,
        marketcap_usd NUMERIC,
        rune_number TEXT,
        symbol TEXT,
        etching_time TEXT,
        etching TEXT,
        inscription_id TEXT,
        turbo TEXT,
        amount NUMERIC,
        supply NUMERIC,
        burned NUMERIC,
        premine NUMERIC,
        minted NUMERIC,
        mints NUMERIC,
        holders NUMERIC,
        price_sats NUMERIC,
        price_usd NUMERIC,
        price_change NUMERIC,
        volume_1h_btc NUMERIC,
        volume_1d_btc NUMERIC,
        volume_7d_btc NUMERIC,
        volume_total_btc NUMERIC,
        sales_1h NUMERIC,
        sales_1d NUMERIC,
        sales_7d NUMERIC,
        sales_total NUMERIC,
        sellers_1h NUMERIC,
        sellers_1d NUMERIC,
        sellers_7d NUMERIC,
        buyers_1h NUMERIC,
        buyers_1d NUMERIC,
        buyers_7d NUMERIC,
        listings_min_price NUMERIC,
        listings_max_price NUMERIC,
        listings_avg_price NUMERIC,
        listings_percentile_25 NUMERIC,
        listings_median_price NUMERIC,
        listings_percentile_75 NUMERIC,
        count_listings NUMERIC,
        listings_total_quantity NUMERIC,
        balance_change_last_1_block NUMERIC,
        balance_change_last_3_blocks NUMERIC,
        balance_change_last_10_blocks NUMERIC
    );
    """
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to save data to the PostgreSQL database
def save_to_database(data):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()

        insert_query = sql.SQL("""
        INSERT INTO runes_token_info_genii (
            timestamp, rune_id, rune_name, marketcap_usd, rune_number, symbol, etching_time, etching,
            inscription_id, turbo, amount, supply, burned, premine, minted, mints, holders,
            price_sats, price_usd, price_change, volume_1h_btc, volume_1d_btc, volume_7d_btc,
            volume_total_btc, sales_1h, sales_1d, sales_7d, sales_total, sellers_1h, sellers_1d,
            sellers_7d, buyers_1h, buyers_1d, buyers_7d, listings_min_price, listings_max_price,
            listings_avg_price, listings_percentile_25, listings_median_price, listings_percentile_75,
            count_listings, listings_total_quantity, balance_change_last_1_block,
            balance_change_last_3_blocks, balance_change_last_10_blocks
        ) VALUES (
            %(timestamp)s, %(rune_id)s, %(rune_name)s, %(marketcap_usd)s, %(rune_number)s, %(symbol)s, %(etching_time)s, %(etching)s,
            %(inscription_id)s, %(turbo)s, %(amount)s, %(supply)s, %(burned)s, %(premine)s, %(minted)s, %(mints)s, %(holders)s,
            %(price_sats)s, %(price_usd)s, %(price_change)s, %(volume_1h_btc)s, %(volume_1d_btc)s, %(volume_7d_btc)s,
            %(volume_total_btc)s, %(sales_1h)s, %(sales_1d)s, %(sales_7d)s, %(sales_total)s, %(sellers_1h)s, %(sellers_1d)s,
            %(sellers_7d)s, %(buyers_1h)s, %(buyers_1d)s, %(buyers_7d)s, %(listings_min_price)s, %(listings_max_price)s,
            %(listings_avg_price)s, %(listings_percentile_25)s, %(listings_median_price)s, %(listings_percentile_75)s,
            %(count_listings)s, %(listings_total_quantity)s, %(balance_change_last_1_block)s,
            %(balance_change_last_3_blocks)s, %(balance_change_last_10_blocks)s
        )
        """)
        
        cursor.executemany(insert_query, data)
        connection.commit()
    except Exception as e:
        print(f"Error saving data to database: {e}")
    finally:
        cursor.close()
        connection.close()

# Main function to run the SQL query and fetch results
def main():
    create_table_if_not_exists()  # Ensure the table exists before starting the loop
    while True:
        start_time = time.time()

        run_response = run_sql_query()
        if run_response is None or run_response.status_code != 201:
            print(f"Error in running SQL query: {run_response.status_code if run_response else 'No response'}")
            if run_response:
                print(run_response.json())
            time.sleep(300)  # Wait 5 minutes before retrying
            continue
        
        run_response_json = run_response.json()
        if 'data' not in run_response_json:
            print("Error in running SQL query:", run_response_json)
            time.sleep(300)  # Wait 5 minutes before retrying
            continue
        
        query_id = run_response_json["data"]["queryId"]
        print(f"Query ID: {query_id}")
        
        while True:
            status_response = check_query_status(query_id)
            if status_response is None or 'data' not in status_response:
                print("Error in checking query status:", status_response)
                time.sleep(300)  # Wait 5 minutes before retrying
                continue
            
            query_status = status_response["data"]["queryStatus"]
            print(f"Query Status: {query_status}")
            
            if query_status == 2:  # Status 2 means ready
                data_response = fetch_query_data(1)
                if data_response is None or 'data' not in data_response:
                    print("Error in fetching query data:", data_response)
                    print("Data response:", data_response)
                    time.sleep(300)  # Wait 5 minutes before retrying
                    continue
                
                results = data_response["data"]["list"]
                total_count = data_response["data"]["resultCnt"]
                
                if total_count is None:
                    print("Error: 'resultCnt' not found in data response")
                    print("Data response:", data_response)
                    time.sleep(300)  # Wait 5 minutes before retrying
                    continue
                
                page_size = 100
                total_pages = (total_count + page_size - 1) // page_size  # Calculate the number of pages
                
                for page in range(2, total_pages + 1):
                    time.sleep(0.5)  # Adjust sleep to avoid rate limiting
                    page_data = fetch_query_data(page, page_size)
                    if page_data and 'data' in page_data and 'list' in page_data["data"]:
                        results.extend(page_data["data"]["list"])
                    else:
                        print(f"Error fetching data for page {page}: {page_data}")
                        break
                
                save_to_database(results)
                print("Data saved to the database")
                break
            
            time.sleep(1)  # Wait for 1 second before checking the status again
        
        end_time = time.time()
        run_duration = end_time - start_time
        print(f"Run duration: {run_duration} seconds")
        time.sleep(max(0, 300 - run_duration))  # Adjust sleep to account for the script's run time

if __name__ == "__main__":
    main()
robert@range
message.txt
16 KB
