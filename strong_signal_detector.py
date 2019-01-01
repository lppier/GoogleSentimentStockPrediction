import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import fix_yahoo_finance as yf

data = yf.download("AAPL", start="2017-01-01", end="2018-12-6")
# data.Close.plot()


from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

# pytrends.suggestions('Apple')
# [{'mid': '/m/0k8z', 'title': 'Apple', 'type': 'Technology company'},
#  {'mid': '/m/014j1m', 'title': 'Apple', 'type': 'Fruit'},
#  {'mid': '/g/11c2659rn_', 'title': 'Apple iPhone 8', 'type': 'Topic'},
#  {'mid': '/m/0gz0jd', 'title': 'Apple TV', 'type': 'Topic'}, {'mid': '/m/01qd72', 'title': 'Apples', 'type': 'Plants'}]
kw_list = ["trade war"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
df = pytrends.interest_over_time()

# df = pd.read_csv("./data/apple_trend.csv")
# df = df[109:] # 3/1/2016
df = df['2017-01-01':]  # 1/1/2017
df = df.rename(columns={"trade war": "trade war"})
df['Week'] = df.index
df = df.reset_index()
# plt.plot(df['Week'], df['Apple: (Worldwide)'])

grid_sell_thres = [45]
lower_buy_thres = -40  # if percentage decrease is more than this, buy more <shares_to_buy> shares
upper_sell_thres = 40  # if percentage increase is more than this, sell <shares_to_sell> shares
shares_to_buy = 50  # number of shares to buy when buying opportunity
shares_to_sell = 60  # number of shares to sell when selling opportunity
best_money_earned = 0

fig = plt.figure(facecolor='w', figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(data.index, data['Close'], '.-')

for upper_sell_thres in grid_sell_thres:
    print("----- Sell percentage threshold : {0}".format(upper_sell_thres))
    prev = 0
    money = orig_money = 12000
    shares = 0  # number of shares on hand
    transactions = 0
    percent_inc = 0
    rolling_percent_inc = 0

    for idx, row in df.iterrows():
        curr = row['trade war']
        week = row['Week']
        # print(week)

        # get index 5 weeks ago
        rolling_idx = max(idx - 5, df.index[0])
        rolling_row = df.loc[[rolling_idx]]
        rolling_trend = rolling_row['trade war'].values[0]

        # Find next available trading day
        day = 1
        while True:
            datetime_object = datetime.strptime(str(week), '%Y-%m-%d %H:%M:%S') + timedelta(days=day)
            array = data[data.index.to_pydatetime() == datetime_object]['Close'].values
            if len(array) > 0:
                close = array[0]
                break
            else:
                day += 1

        if prev != 0:
            percent_inc = (curr - prev) / prev * 100
            rolling_percent_inc = (curr - rolling_trend) / rolling_trend * 100

        if percent_inc >= upper_sell_thres:
            print("* Strong Sell Alert at {0} date {1}".format(close, week))
            plt.axvline(x=week, linestyle='--', color='r')
            if shares >= shares_to_sell:
                money += shares_to_sell * close
                shares -= shares_to_sell
                print(" -- sold {0} at {1}".format(shares_to_sell, close))
            else:
                money += shares * close
                print(" -- sold {0} at {1}".format(shares, close))
                shares = 0
            transactions += 1
        # elif rolling_percent_inc >= upper_sell_thres:
        #     print("Rolling Action Alert at {0} date {1}".format(close, week))
        #     plt.axvline(x=week, linestyle='--', color='k')
        elif percent_inc <= lower_buy_thres:
            print("* Strong Buy Alert at {0} date {1}".format(close, week))
            plt.axvline(x=week, linestyle='--', color='b')

            print("-- Buy {0} at {1}".format(shares_to_buy, close))
            if money >= shares_to_buy * close:
                money -= shares_to_buy * close
                shares += shares_to_buy
                transactions += 1
            else:
                shares_i_can_still_buy = round(money / close)
                money -= shares_i_can_still_buy * close
                shares += shares_i_can_still_buy
                print("not enough money to buy! buy max {0}".format(shares_i_can_still_buy))

        prev = curr

    onhand_shares_worth = shares * close
    print("*** Lower buy threshold: {0} Upper Sell Threshold: {1}".format(lower_buy_thres, upper_sell_thres))
    print("Sell on-hand shares + {0} at {1} each".format(onhand_shares_worth, close))
    print(
        "{0} transactions, eventual money after selling all shares ${1}".format(transactions,
                                                                                money + onhand_shares_worth))
    real_money_earned = money + onhand_shares_worth - (transactions * 20)
    print(
        "including transaction fees ${0}".format(real_money_earned))
    print(
        "If you bought at original close price 170.57.. you would be able to get ${0}".format(orig_money / 170.57 * close))

plt.show()
