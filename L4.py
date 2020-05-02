import requests
import time

def api():
    bitb = requests.get('https://bitbay.net/API/Public/BTC/USD/ticker.json')
    cex = requests.get('https://cex.io/api/ticker/BTC/USD')
    bits = requests.get('https://www.bitstamp.net/api/ticker')
    block = requests.get("https://blockchain.info/ticker")
    return bitb.json(),cex.json(),bits.json(),block.json()

def wallet(w_value, buy, sell):
    w_value[0] = w_value[0] - buy*0.01
    w_value[1] = w_value[1] - 0.01
    w_value[0] = w_value[0] + sell*0.01
    return w_value

def arbitration(w_value):
    tic_bitb, tic_cex, tic_bits, tic_block = api()
    
    bitbaysell = float(tic_bitb['bid'])
    bitbaybuy = float(tic_bitb['ask'])
    cexsell = float(tic_cex['bid'])
    cexbuy = float(tic_cex['ask'])
    bitstampsell = float(tic_bits['bid'])
    bitstampbuy = float(tic_bits['ask'])
    blockbuy = float(tic_block['USD']['sell'])
    blocksell = float(tic_block['USD']['buy'])


    buy = {'bitbay':bitbaybuy, 'cex':cexbuy, 'bitstamp':bitstampbuy, 'blockchain':blockbuy,}
    sell = {'bitbay':bitbaysell, 'cex':cexsell, 'bitstamp':bitstampsell, 'blockchain':blocksell,}

    lowest = min(buy.values())
    lowesto = min(buy,key = buy.get)

    highest = max(sell.values())
    highesto = max(sell,key = sell.get)

    if lowest < highest:
        print(f"You can buy 0,01 BTC for USD on the {lowesto} at the exchange rate of {lowest} and  sell on the {highesto}, profit: {(highest - lowest)*0.1} USD ")
        print(f"New wallet value: {wallet(w_value, lowest, highest)}")
    else:
        print("No profit-making sales!")
        
w_value = [50, 10]
new_wallet = w_value[:]

while(True):
    arbitration(new_wallet)
    if (new_wallet[0]-w_value[0]) > 0:
        print(f"You have gained from all the transactions {new_wallet[0] - w_value[0]} USD")
    time.sleep(1)