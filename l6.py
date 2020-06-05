import pandas as pd
import yfinance as yf
import sqlite3
from sqlite3 import Error
import requests
import arrow


def create_connection(file):
    try:
        return sqlite3.connect(file)
    except Error as e:
        print(e)

def create_table(conn):
    statement = """ CREATE TABLE IF NOT EXISTS stocks (
                                            name TEXT NOT NULL PRIMARY KEY,
                                            qty INTEGER NOT NULL
                                        ); """
    try:
        c = conn.cursor()
        c.execute(statement)
        conn.commit()
    except Error as e:
        print(e)

def add_stock(conn, stock, qty):
    if(stock_api(stock)):
        try:
            curr_qty = get_current_qty(conn, stock)
            if(curr_qty > 0):
                statement = """
                    UPDATE stocks
                    SET qty = (?)
                    WHERE name = (?);
                    """
                vals = (qty+curr_qty, stock)
                cur = conn.cursor()
                cur.execute(statement, vals)
            else:
                statement = """
                        INSERT INTO stocks (name, qty)
                        VALUES (?,?);
                        """
                vals = (stock, qty)
                cur = conn.cursor()
                cur.execute(statement, vals)
        except Error as e:
            print(e)
        finally:
            conn.commit()
    else:
        print("Tego zasobu nie ma w api. Nie dodano.")

def delete_stock(conn, stock, qty):
    curr_qty = get_current_qty(conn,stock)
    if(curr_qty != None):
        if(curr_qty > 0):
            cur = conn.cursor()
            if(qty == None or qty == curr_qty):
                cur.execute("DELETE FROM stocks WHERE name=?;", (stock,))
            else:
                if(qty<curr_qty):
                    cur.execute("UPDATE stocks SET qty=? WHERE name=?", (curr_qty-qty,stock))
                else:
                    print("Nie masz tyle zasobow.")
            conn.commit()
        else:
            print("Nie posiadasz takiego zasobu.")
    else:
        print("Nie znaleziono zasobu w Twoim inwentarzu.")

def get_current_qty(conn, stock):
    try:
        cur = conn.cursor()
        cur.execute("SELECT qty FROM stocks WHERE name=?;", (stock,))
        result=cur.fetchone()
        return result[0]
    except Exception as e:
        return 0

def get_all_stocks():
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, qty FROM stocks;")
        result = cur.fetchall()
        stocks = {}
        for row in result:
            stocks[row[0]] = row[1]
        return stocks
    except Exception as e:
        print(e)

def show_stocks(stocks):
    if(stocks != None):
        for stock, qty in stocks.items():
            print("{} ilosc: {}".format(stock, qty))
    else:
        print("Brak zasobow.")

def stock_api(stock):
    try:
        stock = yf.Ticker(stock)
        stock.info
        return True
    except Exception as e:
        return False

def get_historical_value(stock):
    try:
        stock_y = yf.Ticker(stock)
        hist = stock_y.history(period="1d")
        print(hist['Close'])
    except Exception as e:
        print(e)

def get_your_stocks_info():
    stock_names = [*get_all_stocks()]
    result = pd.DataFrame()
    for stock in stock_names:
        res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{}?range={}&interval={}'.format(
                stock, '2d','1h'))
        data = res.json()
        body = data['chart']['result'][0]
        # dt = datetime.datetime
        dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
        df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
        # dg = pd.DataFrame(body['timestamp'])
        df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
        df.dropna(inplace=True)
        df.columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
        latest = df['CLOSE'].iloc[-1]
        before = df['CLOSE'].iloc[-9]
        print("{}: aktualna: {}, 24h temu: {}, roznica: {}".format(stock, latest,before, round(latest/before/100,2)))



while(True):
    print("Co chcesz zrobic?")
    print("1. Wyswietl moje zasoby")
    print("2. Dodaj zasob")
    print("3. Usun zasob")
    print("4. Odczytaj notowania zasobow")
    print("0. Zakoncz")
    choice = int(input("Twoj wybor: "))
    if(choice > 0):
        conn = create_connection(r"lite.db")
        create_table(conn)
        if(choice == 1):
            with conn:
                show_stocks(get_all_stocks())
        elif(choice==2):
            zasob = input("Podaj nazwe zasobu: ").upper()
            ilosc = int(input("Podaj liczbe: "))
            with conn:
                add_stock(conn,zasob,ilosc)
        elif(choice==3):
            stock = input("Podaj nazwę zasobu: ").upper()
            qty = int(input("Podaj ile sztuk sprzedales: "))
            delete_stock(conn,stock,qty)
        elif(choice==4):
            get_your_stocks_info()
    else:
        break