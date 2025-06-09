import psycopg2
import csv
import os

DB_NAME = os.getenv("POSTGRES_DB", "todo")
DB_USER = os.getenv("PGPUSER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD", "123")
DB_HOST = os.getenv("HOST", "localhost")

def db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

def init_db():
    conn = db_connection()
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            ticker TEXT,
            date DATE,
            close NUMERIC
        );
    """)
    conn.commit()

    # Check if data exists
    cur.execute("SELECT COUNT(*) FROM stock_prices;")
    count = cur.fetchone()[0]

    if count == 0:
        print("Loading CSV data...")
        load_csv_data(conn, "AAPL.csv", "AAPL")
        load_csv_data(conn, "MSFT.csv", "MSFT")
    else:
        print("Database already populated.")

    conn.commit()
    conn.close()

def load_csv_data(conn, filename, ticker):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        data = [(ticker, row["Date"], row["Close"]) for row in reader]

    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO stock_prices (ticker, date, close)
            VALUES (%s, %s, %s);
        """, data)
