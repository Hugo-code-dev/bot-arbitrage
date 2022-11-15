import os
import requests
import json
import sqlite3
from datetime import datetime
from time import sleep
from os import path

DIR = os.path.dirname(os.path.abspath(__file__))

class Database():
    """Pour utiliser la class Database :
1. Créer une instance de la class Database en lui passant le nom de la base de données en paramètre
2. Créer une table avec la méthode create_table en lui passant le nom de la table et les colonnes en paramètre
3. Insérer des données avec la méthode insert en lui passant le nom de la table et les données en paramètre

Exemple :
db = Database('test.db')
db.create_table('test', ['id INTEGER PRIMARY KEY', 'name TEXT'])
db.insert('test', name='test')"""

    def __init__(self,filename='database.db'):
        self.filepath = os.path.join(DIR,filename)
        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()

    def create_table(self,table,columns):
        try: 
            request = f'''CREATE TABLE {table} ({','.join(columns)})'''
            self.cursor.execute(request)
            self.conn.commit()
        except sqlite3.OperationalError:
            return

    def insert(self,table,**kwargs):
        request = f'''INSERT INTO {table} VALUES ({','.join(['?']*len(kwargs))})'''
        request_values = tuple(kwargs.values())
        print(request)
        self.cursor.execute(request,request_values)
        self.conn.commit()

def get_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def get_bybit_prices():
    url = "https://api.bybit.com/spot/v3/public/quote/ticker/24hr"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def calculate_percentage_gap(database, name):
    binance_idx = 0
    bybit_idx = 0
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    for i in (range(len(binance_prices))):
        date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        for j in range(len(bybit_prices['result']['list'])):
            if binance_prices[i]['symbol'] == bybit_prices['result']['list'][j]['s']:
                if float(binance_prices[i]['price']) > float(bybit_prices['result']['list'][j]['lp']):
                    binance_idx += 1
                    percentage_gap = (float(binance_prices[i]['price']) - float(bybit_prices['result']['list'][j]['lp'])) / float(binance_prices[i]['price']) * 100
                    database.insert(name, UTC=date,SYMBOL= binance_prices[i]['symbol'], BINANCE_PRICE=binance_prices[i]['price'], BYBIT_PRICE=bybit_prices['result']['list'][j]['lp'], PERCENTAGE_GAP=str(round(percentage_gap,6)), SIDE = 'Binance')
                else:
                    bybit_idx += 1
                    percentage_gap = (float(bybit_prices['result']['list'][j]['lp']) - float(binance_prices[i]['price'])) / float(bybit_prices['result']['list'][j]['lp']) * 100
                    database.insert(name, UTC=date,SYMBOL= binance_prices[i]['symbol'], BINANCE_PRICE=binance_prices[i]['price'], BYBIT_PRICE=bybit_prices['result']['list'][j]['lp'], PERCENTAGE_GAP=str(round(percentage_gap,6)), SIDE = 'Bybit')
    print('Binance : ' + str(binance_idx))
    print('Bybit : ' + str(bybit_idx))

if __name__ == '__main__':
    database = Database(path.join('files','database.db'))
    while True:
        name = str(datetime.now().strftime("test"))
        database.create_table(name, ['UTC TEXT PRIMARY KEY', 'SYMBOL TEXT', 'BINANCE_PRICE TEXT', 'BYBIT_PRICE TEXT', 'DIF TEXT', 'SIDE TEXT'])
        calculate_percentage_gap(database, name)
        sleep(60)