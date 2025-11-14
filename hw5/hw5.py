import json
import os
BASE_PATH= BASE_PATH = "/workspaces/data_3500_homework_Jared_Meservy/hw5"
tickers =["AAPL","GOOG","ADBE","TSLA","AMZN","MSFT","META","CSCO","CMCSA","NFLX"]
window_days= 5
def read_prices_for_ticker(ticker):
    file_path= os.path.join(BASE_PATH, f"{ticker}.txt")
    prices =[]
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            price = round(float(line), 2)
            prices.append(price)

    return prices
def mean_reversion(prices, window=window_days):
    holding=False
    buy_price = 0.0
    first_buy_price=None
    total_profit= 0.0

    for i in range(window, len(prices)):
        window_prices=prices[i - window:i]
        avg_price =sum(window_prices) / window
        current_price = prices[i]
        if current_price< avg_price * 0.98 and not holding:
            # Buy signal
            holding =True
            buy_price = current_price
            if first_buy_price is None:
                first_buy_price = buy_price
            print(f"buying at:      {buy_price:.2f}")
        elif current_price > avg_price * 1.02 and holding:
            # Sell signal
            print(f"selling at:     {current_price:.2f}")
            trade_profit = current_price - buy_price
            total_profit += trade_profit
            print(f"trade profit:   {trade_profit:.2f}")
            holding = False
    print(f"Total profit:   {total_profit:.2f}")

    if first_buy_price is not None and first_buy_price != 0:
        percent_return = (total_profit / first_buy_price) * 100
        print(f"First buy:      {first_buy_price:.2f}")
        print(f"Percent return: {percent_return:.2f}%")
    else:
        percent_return = 0.0
        print("No trades were made. Percent return: 0.00%")


    return total_profit, percent_return


def moving_average(prices, window=window_days):
    holding = False
    buy_price = 0.0
    first_buy_price = None
    total_profit = 0.0

    for i in range(window, len(prices)):
        window_prices =prices[i - window:i]
        avg_price =sum(window_prices) / window
        current_price = prices[i]
        if current_price > avg_price and not holding:
            # Buy signal
            holding = True
            buy_price = current_price
            if first_buy_price is None:
                first_buy_price= buy_price
            print(f"buying at:      {buy_price:.2f}")
        elif current_price < avg_price and holding:
            # Sell signal
            print(f"selling at:     {current_price:.2f}")
            trade_profit = current_price - buy_price
            total_profit += trade_profit
            print(f"trade profit:   {trade_profit:.2f}")
            holding = False
    print("-----------------------")
    print(f"Total profit:   {total_profit:.2f}")
    if first_buy_price is not None and first_buy_price !=0:
        percent_return = (total_profit / first_buy_price) *100
        print(f"First buy:      {first_buy_price:.2f}")
        print(f"Percent return: {percent_return:.2f}%")
    else:
        percent_return = 0.0
        print("No trades were made. Percent return: 0.00%")
    print()
    return total_profit, percent_return
def save(results_dict):
    output_path = os.path.join(BASE_PATH, "results.json")
    with open(output_path, "w") as json_file:
        json.dump(results_dict, json_file, indent=4)
def main():
    results = {}
    for ticker in tickers:
        print(f"Running strategies for {ticker}")
        prices= read_prices_for_ticker(ticker)
        results[f"{ticker}_prices"] = prices
        # SMA
        print(f"{ticker} Simple Moving Average Strategy Output:")
        sma_profit, sma_returns =moving_average(prices)
        results[f"{ticker}_sma_profit"] =sma_profit
        results[f"{ticker}_sma_returns"]= sma_returns
        # MRS
        print(f"{ticker} Mean Reversion Strategy Output:")
        mr_profit, mr_returns =mean_reversion(prices)
        results[f"{ticker}_mr_profit"]= mr_profit
        results[f"{ticker}_mr_returns"] = mr_returns
    # Save results
    save(results)
    print("All results saved to results.json")
if __name__ == "__main__":
    main()
