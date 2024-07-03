import os
import pandas as pd
import random
import time
import urllib.request
import urllib.error
import click

from bs4 import BeautifulSoup
from datetime import datetime

DATA_DIR = "data"
RANDOM_SLEEP_TIMES = (1, 5)

SP500_LIST_URL = ""
SP500_LIST_PATH = os.path.join(DATA_DIR, "constituents-financials.csv")

def _download_sp500_list():
    if os.path.exists(SP500_LIST_PATH):
        return

    try:
        with urllib.request.urlopen(SP500_LIST_URL) as response, open(SP500_LIST_PATH, 'wb') as out_file:
            print(f"Downloading ... {SP500_LIST_URL}")
            out_file.write(response.read())
    except urllib.error.URLError as e:
        print(f"Failed to download S&P 500 list: {e}")

def _load_symbols():
    _download_sp500_list()
    df_sp500 = pd.read_csv(SP500_LIST_PATH)
    df_sp500.sort_values('Market Cap', ascending=False, inplace=True)
    stock_symbols = df_sp500['Symbol'].unique().tolist()
    print(f"Loaded {len(stock_symbols)} stock symbols")
    return stock_symbols

def fetch_prices(symbol, out_name):
    now_datetime = datetime.now().strftime("%b+%d,+%Y")
    BASE_URL = "https://finance.google.com/finance/historical?output=csv&q={0}&startdate=Jan+1%2C+1980&enddate={1}"
    symbol_url = BASE_URL.format(symbol, now_datetime.replace(" ", "+"))

    print(f"Fetching {symbol} ...")
    print(symbol_url)

    try:
        with urllib.request.urlopen(symbol_url) as response, open(out_name, 'wb') as out_file:
            out_file.write(response.read())
    except urllib.error.HTTPError as e:
        print(f"Failed when fetching {symbol}: {e}")
        return False

    data = pd.read_csv(out_name)
    if data.empty:
        print(f"Remove {out_name} because the data set is empty.")
        os.remove(out_name)
    else:
        dates = data.iloc[:,0].tolist()
        print(f"# Fetched rows: {data.shape[0]} [{dates[-1]} to {dates[0]}]")

    sleep_time = random.randint(*RANDOM_SLEEP_TIMES)
    print(f"Sleeping ... {sleep_time}s")
    time.sleep(sleep_time)
    return True

@click.command(help="Fetch stock prices data")
@click.option('--continued', is_flag=True)
def main(continued):
    random.seed(time.time())
    num_failure = 0

    symbols = _load_symbols()
    for idx, sym in enumerate(symbols):
        out_name = os.path.join(DATA_DIR, f"{sym}.csv")
        if continued and os.path.exists(out_name):
            print(f"Fetched {sym}")
            continue

        succeeded = fetch_prices(sym, out_name)
        num_failure += int(not succeeded)

        if idx % 10 == 0:
            print(f"# Failures so far [{idx + 1}/{len(symbols)}]: {num_failure}")

if __name__ == "__main__":
    main()
