import requests
import json
import sqlite3
from datetime import datetime

# class Database :

#     def __init__(self,filename):
#         self.filename = filename
#         conn = sqlite3.connect(self.filename)
#         query = "CREATE TABLE IF NOT EXISTS DATA (UTC TEXT, SYMBOL TEXT, BINANCE_PRICE FLOAT, BYBIT_PRICE FLOAT, DIF FLOAT, SIDE TEXT, ROWID INTEGER PRIMARY KEY AUTOINCREMENT)"
#         conn.execute(query)
#         conn.close()

#     def insert(self,**kwargs):
#         conn = sqlite3.connect(self.filename)
#         query = "INSERT INTO DATA ("
#         query += ",".join(kwargs.keys())
#         query += ") VALUES ("
#         query += ",".join(kwargs.values())

#         conn.execute(query, (args))
#         conn.commit()
#         conn.close()

def create_database(data):
    conn = sqlite3.connect(data)
    query = "CREATE TABLE IF NOT EXISTS DATA (UTC TEXT, SYMBOL TEXT, BINANCE_PRICE FLOAT, BYBIT_PRICE FLOAT, DIF FLOAT, SIDE TEXT, ROWID INTEGER PRIMARY KEY AUTOINCREMENT)"
    conn.execute(query)
    conn.close()

def get_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def get_bybit_prices2():
    url = "https://api.bybit.com/spot/v3/public/quote/ticker/24hr"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def get_bybit_prices():
    url = "https://api.bybit.com/v2/public/tickers"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def calculate_percentage_gap(data):
    binance_idx = 0
    bybit_idx = 0
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    conn = sqlite3.connect(data)
    for i in (range(len(binance_prices))):
        date = datetime.now()
        for j in range(len(bybit_prices['result'])):
            if binance_prices[i]['symbol'] == bybit_prices['result'][j]['symbol']:
                if float(binance_prices[i]['price']) > float(bybit_prices['result'][j]['last_price']):
                    binance_idx += 1
                    percentage_gap = (float(binance_prices[i]['price']) - float(bybit_prices['result'][j]['last_price'])) / float(binance_prices[i]['price']) * 100
                    query = "INSERT INTO DATA (UTC, SYMBOL, BINANCE_PRICE, BYBIT_PRICE, DIF, SIDE) VALUES ('"+str(date)+"','"+binance_prices[i]['symbol']+"','"+binance_prices[i]['price']+"','"+bybit_prices['result'][j]['last_price']+"','"+str(round(percentage_gap, 15))+"','Binance')"
                    conn.execute(query)
                elif float(binance_prices[i]['price']) < float(bybit_prices['result'][j]['last_price']):
                    bybit_idx += 1
                    percentage_gap = (float(bybit_prices['result'][j]['last_price']) - float(binance_prices[i]['price'])) / float(bybit_prices['result'][j]['last_price']) * 100
                    query2 = "INSERT INTO DATA (UTC, SYMBOL, BINANCE_PRICE, BYBIT_PRICE, DIF, SIDE) VALUES ('"+str(date)+"','"+binance_prices[i]['symbol']+"','"+binance_prices[i]['price']+"','"+bybit_prices['result'][j]['last_price']+"','"+str(round(percentage_gap, 15))+"','Bybit')"
                    conn.execute(query2)
    conn.commit()
    print('\nBinance : ' + str(binance_idx))
    print('Bybit : ' + str(bybit_idx))

if __name__ == '__main__':
    filename = input('Enter database name : ')
    create_database(filename)
    calculate_percentage_gap(filename)