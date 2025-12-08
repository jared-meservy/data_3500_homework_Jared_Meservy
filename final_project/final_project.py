import csv
import json
from datetime import datetime, timezone
from statistics import mean
import requests
import os

# CONFIG
api= "CG-HJTHvNVmQezAZu3VrLfk4UCk"
coins =["bitcoin", "ethereum","litecoin","ripple","bitcoin-cash","eos"]
currency_type= "usd"
days=365
fastW= 20
slowW=50
def timestamp(ts_ms):
    #Convert milliseconds
    dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")
def csv_filename(coin_id):
    return f"{coin_id}.csv"
def load(coin_id):
    #load existing CSV
    filename= csv_filename(coin_id)
    if not os.path.exists(filename):
        return [], []
    dates, prices= [], []
    with open(filename, "r", newline="", encoding="utf-8") as  f:
        reader= csv.DictReader(f)
        for row in reader:
            dates.append(row["date"])
            prices.append(float(row["price_usd"]))
    return dates, prices
def appendtocsv(coin_id, rows):
    #Append rows to CSV creates new file
    filename = csv_filename(coin_id)
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "price_usd"])
        for row in rows:
            writer.writerow(row)
# api calls no more than 5-6 per min shouldnt be an issue for me
def chart(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params= {"vs_currency": currency_type,"days": days,"x_cg_demo_api_key": api}
    response =requests.get(url, params=params, timeout=30)

    return response.json()
# update CVS (Make sure to fix it so makes a new file if it doesn't have one originally)
def update_data(coin_id):
    existing_dates, _ =load(coin_id)
    last_date=max(existing_dates) if existing_dates else None
    data=chart(coin_id)
    price= data.get("prices", [])
    new_rows =[]
    for ts, cost in price:
        date= timestamp(ts)
        if last_date is None or date > last_date:
            new_rows.append((date, cost))
    if new_rows:
        appendtocsv(coin_id, new_rows)
    return load(coin_id)
# strats
def strategy1(prices):
    #just a holding strat This will show that most "strategeies" are pretty useless
    if len(prices)< 2:
        return {"name": "buy_and_hold", "profit": 0.0}
    buy_price =prices[0]
    sell_price= prices[-1]

    investment=1000
    amount= investment / buy_price
    profit= amount * (sell_price - buy_price)
    return {"name": "buy_and_hold", "profit": profit, "amount": amount}
def strategy_sma(prices):
    #Just a simple crossover strat specifically a 20/50 SMA crossover strategy.
    n = len(prices)
    if n < slowW:
        return {"name": "sma_crossover", "profit": 0.0, "last_signal": "HOLD", "trades": 0}

    holding = False
    entry_price= 0.0
    amount= 0.0
    profit =0.0
    trades =0
    last_signal = "HOLD"

    prev_fast = None
    prev_slow=None
    for i in range(n):
        if i + 1 >= fastW:
            fast_sma =mean(prices[i - fastW + 1:i + 1])
        else:
            fast_sma= None

        if i + 1 >= slowW:
            slow_sma =mean(prices[i - slowW + 1:i + 1])
        else:
            slow_sma =None

        if fast_sma is None or slow_sma is None:
            continue
        price = prices[i]
        # buying
        if prev_fast is not None and prev_slow is not None:
            if prev_fast <= prev_slow and fast_sma > slow_sma:
                if not holding:
                    holding =True
                    entry_price= price
                    amount = 1000 / price
                    trades+= 1
                    last_signal = "BUY"
            # selling
            elif prev_fast >= prev_slow and fast_sma < slow_sma:
                if holding:
                    holding = False
                    profit += (price - entry_price) * amount
                    trades += 1
                    last_signal = "SELL"
        prev_fast = fast_sma
        prev_slow = slow_sma
    if holding:
        profit += (prices[-1] - entry_price) * amount
    return {"name": "sma_crossover","profit": profit,"last_signal": last_signal,"trades": trades    }
# analysis/ end part
def analysis():
    results = {"coins": {}}
    most_money=None
    best_coin=None
    best_strat=None
    for coin in coins:
        dates, prices=update_data(coin)
        if len(prices)<2:
            print("Not enough data.")
            continue
        s1 =strategy1(prices)
        s2 =strategy_sma(prices)
        print(f"{coin.upper()}:")
        print(f"  Buy & Hold Profit: {s1['profit']:.2f}")
        print(f"  SMA Crossover Profit: {s2['profit']:.2f}")

        # store results
        results["coins"][coin]= {"num_points": len(prices),"start": dates[0],"end": dates[-1],"buy_and_hold": s1,"sma_crossover": s2}
        for s in (s1, s2):
            if most_money is None or s["profit"] >most_money:
                most_money= s["profit"]
                best_coin =coin
                best_strat= s["name"]
    results["best"] = {"coin": best_coin,"strategy": best_strat,"profit": most_money}
    # write results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print("\nSUMMARY")

    print(f"Best overall: {best_strat} on {best_coin} with profit {most_money:.2f}")
if __name__ == "__main__":
    analysis()
