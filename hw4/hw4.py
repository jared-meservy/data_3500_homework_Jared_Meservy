import csv
file = "hw4/tsla.csv"   
buy_multi= 0.98 
sell_multi= 1.02 
window = 5                   
def read_prices(file):
    prices = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value =row.get("Close/Last") or row.get("Close") or row.get("Close Price")
            if not value:
                continue
            value = value.replace("$", "").replace(",", "").strip()
            try:
                price = round(float(value), 2)
                prices.append(price)
            except ValueError:
                continue
    prices.reverse()
    return prices
def run_strategy(prices):
    holding = False
    buy_price = None
    first_buy = None
    total_profit = 0.0
    print("TSLA Mean Reversion Strategy Output\n" + ("-" * 31))
    for x in range(window, len(prices)):
        current_price =prices[x]
        window_prices = prices[x - window : x]
        avg_price = sum(window_prices) / window
        # Thresholds
        buy_level=avg_price * buy_multi
        sell_level=avg_price * sell_multi
        # entry decsison 
        if (current_price < buy_level) and (not holding):
            # Deciding to buy
            buy_price= current_price
            holding =True
            if first_buy is None:
                first_buy =buy_price
            print(f"buying at:       {buy_price:.2f}")
        elif (current_price > sell_level) and holding:
            # Deciding to sell
            sell_price=current_price
            profit =round(sell_price-buy_price, 2)
            total_profit =round(total_profit + profit, 2)
            holding= False
            print(f"selling at:      {sell_price:.2f}")
            print(f"trade profit:    {profit:.2f}")
    # the end total summary thing
    print(f"Total profit:    {total_profit:.2f}")
    if first_buy is not None and first_buy != 0:
        final_profit_percent = round((total_profit / first_buy) * 100, 2)
        print(f"First buy:       {first_buy:.2f}")
        print(f"% return:        {final_profit_percent:.2f}%")
def main():
    prices = read_prices(file)
    run_strategy(prices)
if __name__ == "__main__":
    main()
