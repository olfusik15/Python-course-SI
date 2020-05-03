import requests
import time


def api():
    btc = requests.get('https://www.bitstamp.net/api/v2/ticker/btcusd/')
    bch = requests.get('https://www.bitstamp.net/api/v2/ticker/bchusd/')
    eth = requests.get('https://www.bitstamp.net/api/v2/ticker/ethusd/')
    ltc = requests.get('https://www.bitstamp.net/api/v2/ticker/ltcusd/')
    xrp = requests.get('https://www.bitstamp.net/api/v2/ticker/xrpusd/')
    return btc.json(), bch.json(), eth.json(), ltc.json(), xrp.json()


def transaction(investment_amount):
    while True:
        btc_ticker, bch_ticker, eth_ticker, ltc_ticker, xrp_ticker = api()

        percentage = {
            'btc': float(btc_ticker['high'])/float(btc_ticker['low']) - 1,
            'bch': float(bch_ticker['high'])/float(bch_ticker['low']) - 1,
            'eth': float(eth_ticker['high'])/float(eth_ticker['low']) - 1,
            'ltc': float(ltc_ticker['high'])/float(ltc_ticker['low']) - 1,
            'xrp': float(xrp_ticker['high'])/float(xrp_ticker['low']) - 1,
        }

        volumes = {
            'btc': float(btc_ticker['volume']),
            'bch': float(bch_ticker['volume']),
            'eth': float(eth_ticker['volume']),
            'ltc': float(ltc_ticker['volume']),
            'xrp': float(xrp_ticker['volume']),
        }

        low = {
            'btc': float(btc_ticker['low']),
            'bch': float(bch_ticker['low']),
            'eth': float(eth_ticker['low']),
            'ltc': float(ltc_ticker['low']),
            'xrp': float(xrp_ticker['low']),
        }

        table = sorted(percentage, key=percentage.get, reverse=True)

        for crypto in table:
            print(f'{crypto} {percentage[crypto]*100:.2f}%')

        for crypto in table:
            if investment_amount > 0:
                if volumes[crypto]*low[crypto] < investment_amount:
                    investment_amount = investment_amount - \
                        volumes[crypto]*low[crypto]
                        
                    print(f"Purchased: {volumes[crypto]*low[crypto]:.2f} {crypto}")
                    print(f"Amount of funds: {investment_amount:.2f} USD")
                    
                else:
                    print(f"Purchased: {investment_amount/low[crypto]:.2f} {crypto}")
                    investment_amount = 0
                    print(f"No more found: {investment_amount:.2f} USD")

        time.sleep(300)


transaction(9999999)