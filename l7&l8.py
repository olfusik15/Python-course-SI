import requests
import pandas as pd
import arrow
import numpy as np
from sklearn import preprocessing, model_selection
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller


def rolling_plot(stock_data):
    rolmean = stock_data.rolling(12).mean()
    rolstd = stock_data.rolling(12).std()
    plt.plot(stock_data, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

def algorytm(stock_data):
    train_data, test_data = split(stock_data)
    train = pd.DataFrame(train_data)
    test = pd.DataFrame(test_data)
    pred = pd.DataFrame(stock_data)
    pred = test
    pred['moving_avg_forecast'] = train['CLOSE'].rolling(5).mean().iloc[-1]
    plt.figure(figsize=(16, 8))
    plt.plot(train['CLOSE'], label='Train')
    plt.plot(test['CLOSE'], label='Test')
    plt.plot(pred['moving_avg_forecast'], label='Moving Average Forecast')
    plt.legend(loc='best')
    plt.show()

def get_your_stocks_info(stock, startdate, enddate):
    begin = (pd.to_datetime(startdate)-pd.DateOffset(1) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    end = (pd.to_datetime(enddate)+pd.DateOffset(1) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{}?period1={}&period2={}&interval={}'.format(
            stock, begin,end,'1d'))
    data = res.json()
    body = data['chart']['result'][0]
    dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)
    df.columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
    return df['CLOSE']

def split(stock_data):
    train_data, test_data = stock_data[3:int(len(stock_data) * 0.9)], stock_data[int(len(stock_data) * 0.9):]
    # plt.figure(figsize=(10, 6))
    # plt.grid(True)
    # plt.xlabel('Dates')
    # plt.ylabel('Closing Prices')
    # plt.plot(stock_data, 'green', label='Train data')
    # plt.plot(test_data, 'blue', label='Test data')
    # plt.legend()
    # plt.show()
    return train_data, test_data

def arima(stock_data):
    train_data, test_data = split(stock_data)
    model = ARIMA(train_data, order=(3, 1, 2))
    fitted = model.fit(disp=-1)
    fc, se, conf = fitted.forecast(test_data.shape[0], alpha=0.05)  # na poziomie ufnosci 95%
    fc_series = pd.Series(fc, index=test_data.index)
    plt.figure(figsize=(12,5))
    plt.plot(train_data, label='training')
    plt.plot(test_data, color = 'blue', label='Actual Stock Price')
    plt.plot(fc_series, color = 'orange',label='Predicted Stock Price')
    plt.xlabel('Time')
    plt.ylabel('Actual Stock Price')
    plt.legend(loc='upper left', fontsize=6)
    plt.show()

algorytm(get_your_stocks_info('MSFT','2020-02-03','2020-05-01'))