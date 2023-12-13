import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_stock_data(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            price = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text
            volume = soup.find('td', {'data-test': 'TD_VOLUME-value'}).text
            market_cap = soup.find('td', {'data-test': 'MARKET_CAP-value'}).text

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return {
                'Symbol': stock_symbol,
                'Price': price,
                'Volume': volume,
                'Market Cap': market_cap,
                'Timestamp': now
            }
        else:
            print(f"Failed to fetch data for {stock_symbol}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching data for {stock_symbol}: {e}")
        return None

# List of 50 stock symbols to scrape (you can add more if needed)
stock_symbols = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'BABA', 'NVDA', 'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD',
    'UNH', 'DIS', 'PYPL', 'INTC', 'CMCSA', 'NFLX', 'VZ', 'ADBE', 'CRM', 'BAC', 'KO', 'PEP', 'TM', 'NKE', 'ABBV',
    'CSCO', 'PFE', 'XOM', 'CVX', 'MRK', 'ABT', 'QCOM', 'T', 'WFC', 'MDT', 'BA', 'MMM', 'IBM', 'GE', 'CAT', 'HON',
    'LMT', 'GS', 'FDX', 'MS'
]

scraped_data = []
for symbol in stock_symbols:
    data = scrape_stock_data(symbol)
    if data:
        scraped_data.append(data)

# Create DataFrame
df = pd.DataFrame(scraped_data)
print(df)

# Save to CSV
df.to_csv('stock_data.csv', index=False)
