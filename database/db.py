import os
import sqlite3
from datetime import datetime, timezone
from config import DATABASE_FILE

def get_database():
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)

def create_tables():
    with get_database() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            title TEXT,
            url TEXT UNIQUE,
            snippet TEXT,
            content TEXT,
            score REAL,
            created_at TEXT
        )
        """)
        db.commit()

def save_results(query, results):
    with get_database() as db:
        for item in results:
            db.execute("""
                INSERT OR IGNORE INTO research
                (query, title, url, snippet, content, score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                query,
                item.get("title", ""),
                item.get("url", ""),
                item.get("snippet", ""),
                item.get("content", ""),
                item.get("score", 0),
                datetime.now(timezone.utc).isoformat(),
            ))
        db.commit()
