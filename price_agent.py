import sqlite3
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 1. The Target & The "Disguise" (Headers)
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Initiating SESKO AI Ingestion Agent...")

# 2. Extract the Data
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

products = soup.find_all('div', class_='caption')

# 3. Connect to Database
conn = sqlite3.connect('b2b_intelligence.db')
cursor = conn.cursor()

count = 0

# 4. Clean and Inject the Data
for item in products:
    # Get the raw text
    name = item.find('a', class_='title').text.strip()
    raw_price = item.find('h4', class_='price').text.strip()
    
    # Clean the price (remove the $ and turn it into a math number)
    clean_price = float(raw_price.replace('$', '').replace(',', ''))
    
    # Format the data into our flexible JSON payload
    payload = {
        "price_usd": clean_price,
        "currency": "USD",
        "market_status": "ACTIVE"
    }
    
    # Insert into our Universal Table
    cursor.execute('''
        INSERT INTO universal_feeds (domain, sub_category, entity_name, data_payload, scrape_timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', ("RETAIL", "LAPTOPS", name, json.dumps(payload), datetime.now().isoformat()))
    
    count += 1

conn.commit()
conn.close()

print(f"SUCCESS: {count} live market assets injected into Sovereign Database.")