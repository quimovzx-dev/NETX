import os
import sqlite3
from datetime import datetime, timezone
from config import DATABASE_FILE, CACHE_HOURS

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
            summary TEXT,
            source_type TEXT,
            score REAL,
            created_at TEXT
        )
        """)
        columns = {row[1] for row in db.execute("PRAGMA table_info(research)")}
        for name, sql_type in {"summary": "TEXT", "source_type": "TEXT"}.items():
            if name not in columns:
                db.execute(f"ALTER TABLE research ADD COLUMN {name} {sql_type}")
        db.execute("CREATE INDEX IF NOT EXISTS idx_research_query ON research(query)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_research_created ON research(created_at)")
        db.commit()

def save_results(query, results):
    with get_database() as db:
        for item in results:
            db.execute("""
                INSERT INTO research
                (query, title, url, snippet, content, summary, source_type, score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    query=excluded.query, title=excluded.title,
                    snippet=excluded.snippet, content=excluded.content,
                    summary=excluded.summary, source_type=excluded.source_type,
                    score=excluded.score, created_at=excluded.created_at
            """, (
                query, item.get("title", ""), item.get("url", ""),
                item.get("snippet", ""), item.get("content", ""),
                item.get("summary", ""), item.get("source_type", ""),
                item.get("score", 0), datetime.now(timezone.utc).isoformat()
            ))
        db.commit()

def history(limit=10):
    with get_database() as db:
        return db.execute("""
            SELECT query, COUNT(*), MAX(created_at)
            FROM research GROUP BY query
            ORDER BY MAX(created_at) DESC LIMIT ?
        """, (limit,)).fetchall()

def stats():
    with get_database() as db:
        sources = db.execute("SELECT COUNT(*) FROM research").fetchone()[0]
        queries = db.execute("SELECT COUNT(DISTINCT query) FROM research").fetchone()[0]
        hosts = db.execute("""
            SELECT COUNT(DISTINCT
              CASE WHEN instr(url, '://') > 0
              THEN substr(url, instr(url, '://') + 3) ELSE url END)
            FROM research
        """).fetchone()[0]
        return {"sources": sources, "queries": queries, "unique_hosts": hosts}

def cached(url):
    with get_database() as db:
        row = db.execute("""
            SELECT title, url, snippet, content, summary, source_type, score
            FROM research WHERE url = ?
            AND created_at >= datetime('now', ?)
            LIMIT 1
        """, (url, f"-{CACHE_HOURS} hours")).fetchone()
    if not row:
        return None
    keys = ["title", "url", "snippet", "content", "summary", "source_type", "score"]
    return dict(zip(keys, row))
