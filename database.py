import sqlite3

data = 'database.db'

def create_database(data):
    conn = sqlite3.connect(data)
    query = "CREATE TABLE IF NOT EXISTS DATA (UTC TEXT, SYMBOL TEXT, BINANCE_PRICE FLOAT, BYBIT_PRICE FLOAT, DIF FLOAT, SIDE TEXT, ROWID INTEGER PRIMARY KEY AUTOINCREMENT)"
    conn.execute(query)
    conn.close()

def write_to_database(data):
    conn = sqlite3.connect(data)
    query = "INSERT INTO DATA (TYPE, UTC, DIST, DELAY, LAT, LONG) VALUES ('P', '12:54:20', 14, 0, 44.63314183, -1.088661167)"
    conn.execute(query)
    conn.commit()
    conn.close()

def read_from_database(data):
    conn = sqlite3.connect(data)
    query = "SELECT * FROM DATA"
    cursor = conn.execute(query)
    for row in cursor:
        print(row)
    conn.close()

if __name__ == '__main__':
    create_database(data)