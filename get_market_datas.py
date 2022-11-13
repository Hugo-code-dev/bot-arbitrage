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

def calculate_percentage_gap():
    binance_idx = 0
    bybit_idx = 0
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    for i in range(len(binance_prices)):
        for j in range(len(bybit_prices['result'])):
            if binance_prices[i]['symbol'] == bybit_prices['result'][j]['symbol']:
                if float(binance_prices[i]['price']) > float(bybit_prices['result'][j]['last_price']):
                    binance_idx += 1
                    percentage_gap = (float(binance_prices[i]['price']) - float(bybit_prices['result'][j]['last_price'])) / float(binance_prices[i]['price']) * 100
                    print('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'])
                    print('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'])
                    print('Binance is more expensive than Bybit')
                    print('Percentage Gap : ' + str(percentage_gap))
                    print('------------------------------------')
                    with open('result.txt', 'a') as f:
                        f.write('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'] + '\n')
                        f.write('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'] + '\n')
                        f.write('Binance is more expensive than Bybit' + '\n')
                        f.write('Percentage Gap : ' + str(percentage_gap) + '\n')
                        f.write('------------------------------------' + '\n')
                elif float(binance_prices[i]['price']) < float(bybit_prices['result'][j]['last_price']):
                    bybit_idx += 1
                    percentage_gap = (float(bybit_prices['result'][j]['last_price']) - float(binance_prices[i]['price'])) / float(bybit_prices['result'][j]['last_price']) * 100
                    print('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'])
                    print('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'])
                    print('Bybit is more expensive than Binance')
                    print('Percentage Gap : ' + str(percentage_gap))
                    print('------------------------------------')
                    with open('result.txt', 'a') as f:
                        f.write('Binance : ' + binance_prices[i]['symbol'] + ' ' + binance_prices[i]['price'] + '\n')
                        f.write('Bybit : ' + bybit_prices['result'][j]['symbol'] + ' ' + bybit_prices['result'][j]['last_price'] + '\n')
                        f.write('Bybit is more expensive than Binance' + '\n')
                        f.write('Percentage Gap : ' + str(percentage_gap) + '\n')
                        f.write('------------------------------------' + '\n')            

    print('\nBinance : ' + str(binance_idx))
    print('Bybit : ' + str(bybit_idx))

if __name__ == '__main__':
    calculate_percentage_gap()