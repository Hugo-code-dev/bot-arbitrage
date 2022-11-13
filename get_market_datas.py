import requests
import json

def get_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data

def get_bybit_prices():
    url = "https://api.bybit.com/v2/public/tickers"
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    return json_data


def compare_prices():
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    for i in range(len(binance_prices)):
        for j in range(len(bybit_prices['result'])):
            if binance_prices[i]['symbol'] == bybit_prices['result'][j]['symbol']:
                if float(binance_prices[i]['price']) > float(bybit_prices['result'][j]['last_price']):
                    print('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'])
                    print('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'])
                    print('Binance is more expensive than Bybit')
                    print('------------------------------------')
                if float(binance_prices[i]['price']) < float(bybit_prices['result'][j]['last_price']):
                    print('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'])
                    print('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'])
                    print('Bybit is more expensive than Binance')
                    print('------------------------------------')

if __name__ == '__main__':
    compare_prices()