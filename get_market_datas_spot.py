import os
import requests
import json
import sqlite3
from datetime import datetime
from time import sleep
from os import system

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

def calculate_percentage_gap(data):
    binance_idx = 0
    bybit_idx = 0
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    conn = sqlite3.connect(data)
    for i in (range(len(binance_prices))):
        date = datetime.now()
        for j in range(len(bybit_prices['result']['list'])):
            if binance_prices[i]['symbol'] == bybit_prices['result']['list'][j]['s']:
                if float(binance_prices[i]['price']) > float(bybit_prices['result']['list'][j]['lp']):
                    binance_idx += 1
                    percentage_gap = (float(binance_prices[i]['price']) - float(bybit_prices['result']['list'][j]['lp'])) / float(binance_prices[i]['price']) * 100
                    query = "INSERT INTO DATA (UTC, SYMBOL, BINANCE_PRICE, BYBIT_PRICE, DIF, SIDE) VALUES ('"+str(date)+"','"+binance_prices[i]['symbol']+"','"+binance_prices[i]['price']+"','"+bybit_prices['result']['list'][j]['lp']+"','"+str(round(percentage_gap, 15))+"','Binance')"
                    conn.execute(query)
                else:
                    bybit_idx += 1
                    percentage_gap = (float(bybit_prices['result']['list'][j]['lp']) - float(binance_prices[i]['price'])) / float(bybit_prices['result']['list'][j]['lp']) * 100
                    query = "INSERT INTO DATA (UTC, SYMBOL, BINANCE_PRICE, BYBIT_PRICE, DIF, SIDE) VALUES ('"+str(date)+"','"+binance_prices[i]['symbol']+"','"+binance_prices[i]['price']+"','"+bybit_prices['result']['list'][j]['lp']+"','"+str(round(percentage_gap, 15))+"','Bybit')"
                    conn.execute(query)
    conn.commit()
    print('Binance : ' + str(binance_idx))
    print('Bybit : ' + str(bybit_idx))

if __name__ == '__main__':
    while True:
        name = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.db'
        # create_database(name)
        calculate_percentage_gap(name)
        system('mv *.db files/')
        sleep(60)