from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)

DB = "keys.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            used INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def generate_key():
    return f"FEMBOY-{random.randint(100000, 999999)}"

@app.route("/generate")
def generate():
    key = generate_key()

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO keys (key) VALUES (?)", (key,))
    conn.commit()
    conn.close()

    return jsonify({"key": key})

@app.route("/validate")
def validate():
    user_key = request.args.get("key")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE key=?", (user_key,))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})

if __name__ == "__main__":
    init_db()
    app.run()
