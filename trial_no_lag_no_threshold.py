import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import fix_yahoo_finance as yf

data = yf.download("AAPL", start="2013-01-01", end="2018-11-30")
#data.Close.plot()

df = pd.read_csv("./data/apple_trend.csv")
df = df[161:]
#plt.plot(df['Week'], df['Apple: (Worldwide)'])

spike_thres = 0.5
spacing = 5
prev = 0
money = orig_money = 20000
shares = 0
shares_to_buy = shares_to_sell = 25

for index, row in df.iterrows():
    curr = row['Apple: (Worldwide)']
    week = row['Week']
    print(week)

    # Find next available trading day
    day = 1
    while True:
        datetime_object = datetime.strptime(str(week), '%d/%m/%Y') + timedelta(days=day)
        array = data[data.index.to_pydatetime() == datetime_object]['Close'].values
        if len(array) > 0:
            close = array[0]
            break
        else:
            day += 1

    if curr < prev:
        print("-- Buy {0}".format(close))
        if money >= shares_to_buy * close:
            money -= shares_to_buy * close
            shares += shares_to_buy
        else:
            print("not enough money to buy!")
    else:
        if shares >= shares_to_sell:
            print("-- Sell {0}".format(close))
            money += shares_to_sell * close
            shares -= shares_to_sell
        else:
            print("just sell what i have")
            money += shares * close
            shares = 0

    prev = curr

onhand_shares_worth = shares * close
print("Sell on-hand shares + {0}".format(onhand_shares_worth))
print("{0} transactions, eventual money after selling all shares ${1}".format(index, money + onhand_shares_worth))

print("If you bought at original close price 176.. you would be able to get ${0}".format(orig_money/176.19*close))