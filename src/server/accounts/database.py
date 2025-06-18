# Beispiel: src/server/db.py

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('datenbank.db')
    conn.row_factory = sqlite3.Row
    return conn

# Beispielnutzung in einer Route (z.B. FastAPI oder Flask)
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def read_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return [dict(user) for user in users]