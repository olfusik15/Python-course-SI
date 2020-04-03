import requests

def bitbay_orders():
    r = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")
    return r.json()

orders = bitbay_orders()
bids = orders["bids"]
asks = orders["asks"]

print("Oferty kupna:")
for i in bids[:10]:
    print(i)

print("\n Oferty sprzedaży: ")
for i in asks[:10]:
    print(i)