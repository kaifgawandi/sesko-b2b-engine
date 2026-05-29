import sqlite3
import json
from datetime import datetime

# 1. Connect to the new Universal Database (it will create the file if it doesn't exist)
conn = sqlite3.connect('b2b_intelligence.db')
cursor = conn.cursor()

# 2. Create the flexible table
cursor.execute('''
CREATE TABLE IF NOT EXISTS universal_feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT,
    sub_category TEXT,
    entity_name TEXT,
    data_payload TEXT, 
    scrape_timestamp TEXT
)
''')
conn.commit()

print("SUCCESS: Sovereign B2B Database Created!")
conn.close()