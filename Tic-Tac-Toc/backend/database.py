import sqlite3
from datetime import datetime

DB_NAME = "../game.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1 TEXT,
            player2 TEXT,
            player1_symbol TEXT,
            player2_symbol TEXT,
            first_player TEXT,
            winner TEXT,
            played_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(player1, player2, p1_sym, p2_sym, first_player, winner):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO game_results 
        (player1, player2, player1_symbol, player2_symbol, first_player, winner, played_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (player1, player2, p1_sym, p2_sym, first_player, winner, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()