from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3
import json

app = FastAPI(title="SESKO B2B Intelligence Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect("b2b_intelligence.db")
    conn.row_factory = sqlite3.Row
    return conn

# ROUTE 1: Serves the User Interface
@app.get("/")
def serve_dashboard():
    return FileResponse("index.html")

# ROUTE 2: Serves the Live Database
@app.get("/v1/intelligence")
def get_intelligence_feeds(
    domain: str = Query(None),
    sub_category: str = Query(None),
    limit: int = Query(10)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, domain, sub_category, entity_name, data_payload, scrape_timestamp FROM universal_feeds WHERE 1=1"
    params = []
    
    if domain:
        query += " AND domain = ?"
        params.append(domain)
    if sub_category:
        query += " AND sub_category = ?"
        params.append(sub_category)
        
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    
    rows = cursor.execute(query, params).fetchall()
    conn.close()
    
    results = []
    for row in rows:
        record = dict(row)
        try:
            record["data_payload"] = json.loads(record["data_payload"])
        except Exception:
            pass
        results.append(record)
        
    return {"total_records": len(results), "feeds": results}