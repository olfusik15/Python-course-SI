import requests

def bitbay_orders():
    r = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")
    return r.json()

def bitbay_ticker():
    r = requests.get("https://bitbay.net/API/Public/BTCPLN/ticker.json")
    return r.json()

def blockchain_ticker():
    r = requests.get("https://blockchain.info/ticker")
    return r.json()

bitbay = bitbay_orders()
bb_ticker = bitbay_ticker()
bc_ticker = blockchain_ticker()

print("Oferty kupna:")
for i in bitbay["bids"][:10]:
    print(i)

print("\n Oferty sprzedaży: ")
for i in bitbay["asks"][:10]:
    print(i)

if bb_ticker["bid"]>bc_ticker["PLN"]["buy"]:
    print("Buy price is better on bitbay.net: ", bb_ticker["bid"])
else:
        print("Buy price is better on blockchain.info:" , bc_ticker["PLN"]["buy"])

if bb_ticker["ask"]>bc_ticker["PLN"]["sell"]:
    print("Sell price is better on bitbay.net: " , bb_ticker["ask"])
else:
        print("Sell price is better on blockchain.info: " , bc_ticker["PLN"]["sell"])