"""
db_manager.py - SQLite database management for the Travel Planner.

This module sets up the SQLite connection, creates the necessary tables,
and provides helper functions to insert and query time-series flight data.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

# Single authority for the database location. Data lives in /data and is gitignored.
DB_PATH = Path(__file__).parent.parent.parent / "data" / "flight_data.db"


def get_connection():
    """Returns a connection to the SQLite database, creating the data folder if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def setup_database():
    """Initializes the database schema if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            return_date TEXT,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            stops INTEGER DEFAULT 0,
            travel_time_minutes INTEGER,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indices for faster analytics queries
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_route ON flight_prices (origin, destination)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_departure ON flight_prices (departure_date)"
    )

    conn.commit()
    conn.close()


def insert_flight_prices(flights_list):
    """
    Inserts a list of flight dictionaries into the database.
    Each dictionary should contain: origin, destination, departure_date, return_date, price, currency
    """
    conn = get_connection()
    cursor = conn.cursor()

    current_time = datetime.now().isoformat()

    for flight in flights_list:
        cursor.execute(
            """
            INSERT INTO flight_prices
            (origin, destination, departure_date, return_date, price, currency, stops, travel_time_minutes, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                flight["origin"],
                flight["destination"],
                flight["departure_date"],
                flight.get("return_date"),
                flight["price"],
                flight.get("currency", "USD"),
                flight.get("stops", 0),
                flight.get("travel_time_minutes", 0),
                current_time,
            ),
        )

    conn.commit()
    conn.close()


def get_historical_prices(origin, destination, departure_date=None):
    """
    Retrieves historical prices as a Pandas DataFrame.
    """
    conn = get_connection()
    query = "SELECT * FROM flight_prices WHERE origin = ? AND destination = ?"
    params = [origin, destination]

    if departure_date:
        query += " AND departure_date = ?"
        params.append(departure_date)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if not df.empty:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"])

    return df


if __name__ == "__main__":
    setup_database()
    print(f"Database setup complete at {DB_PATH}")
