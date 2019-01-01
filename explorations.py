import matplotlib.pyplot as plt
import pandas as pd
# data = quandl.get("WIKI/AAPL", start_date="2016-01-01", end_date="2018-11-29", api_key="e5DqHU5PKNZvm--78k9_")
# data.Close.plot()
# plt.show()
#
# df = pd.DataFrame()
# df['ds'] = data.index
# df['y'] = data["Close"]
#
# from pandas_datareader import data as pdr
#
# import fix_yahoo_finance as yf
# yf.pdr_override() # <== that's all it takes :-)
#
# # download dataframe
# data = pdr.get_data_yahoo("SPY", start="2018-01-01", end="2018-11-30")
#
# # download Panel
# data = pdr.get_data_yahoo(["SPY", "IWM"], start="2018-01-01", end="2018-11-30")

import fix_yahoo_finance as yf
data = yf.download("AAPL", start="2013-01-01", end="2018-11-30")
data.Close.plot()

import pandas as pd

df = pd.DataFrame()
data['date'] = data.index
df = data.filter(['date','Close'], axis=1)
df = df.reset_index().drop('Date', axis=1)
df = df.rename(columns={'Close': 'y', 'date':'ds'})
df_train = df[:-5]
df_test = df[-5:]

from fbprophet import Prophet
opts = {"daily_seasonality": False, "yearly_seasonality": True, "weekly_seasonality": False}
m = Prophet(**opts, seasonality_mode='multiplicative')
m.fit(df_train)

future = m.make_future_dataframe(periods=3)
future.tail(10)
# need to drop weekends here
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)