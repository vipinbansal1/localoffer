import sqlite3
from datetime import datetime

DB_FILE = "data/messages.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            message TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_message(phone, message, status="SENT"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO message_log (phone, message, status, timestamp)
        VALUES (?, ?, ?, ?)
    """, (phone, message, status, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def fetch_logs(limit=50):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT phone, message, status, timestamp
        FROM message_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN status='SENT' THEN 1 ELSE 0 END) FROM message_log")
    total, sent = cursor.fetchone()
    conn.close()
    return {"total": total, "sent": sent}
