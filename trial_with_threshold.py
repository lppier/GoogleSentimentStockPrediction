import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import fix_yahoo_finance as yf

data = yf.download("AAPL", start="2013-01-01", end="2018-11-30")
# data.Close.plot()

df = pd.read_csv("./data/apple_trend.csv")
df = df[109:]
# plt.plot(df['Week'], df['Apple: (Worldwide)'])

prev = 0
money = orig_money = 20000
shares = 0  # number of shares on hand
shares_to_buy = 35  # number of shares to buy when buying opportunity
shares_to_sell = 60  # number of shares to sell when selling opportunity
transactions = 0
lower_buy_thres = -20  # if percentage decrease is more than this, buy more <shares_to_buy> shares
upper_sell_thres = 50  # if percentage increase is more than this, sell <shares_to_sell> shares

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

    if prev != 0:
        percent_inc = (curr - prev) / prev * 100
        print("Percent inc/dec = {0}".format(percent_inc))

    if percent_inc <= lower_buy_thres:
        print("-- Buy {0}".format(close))
        if money >= shares_to_buy * close:
            money -= shares_to_buy * close
            shares += shares_to_buy
            transactions += 1
        else:
            print("not enough money to buy!")
    elif percent_inc >= upper_sell_thres:
        if shares >= shares_to_sell:
            print("-- Sell {0}".format(close))
            money += shares_to_sell * close
            shares -= shares_to_sell
        else:
            print("just sell what i have")
            money += shares * close
            shares = 0
        transactions += 1

    prev = curr

onhand_shares_worth = shares * close
print("Sell on-hand shares + {0}".format(onhand_shares_worth))
print(
    "{0} transactions, eventual money after selling all shares ${1}".format(transactions, money + onhand_shares_worth))

print("If you bought at original close price 176.. you would be able to get ${0}".format(orig_money / 176.19 * close))
