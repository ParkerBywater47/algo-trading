import sys 
import time


def simulate(price_data, ema_length=3, price_movement_threshold=.03, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    if not silent: 
        print("simulating ema with length " + str(ema_length) + " and price movement threshold " + format(price_movement_threshold, ".2%"))

    # compute an sma to start
    sum_for_avg = 0 
    for i in range(ema_length): 
        try:
            sum_for_avg += price_data[i]
        except IndexError:
            print("Error: Not enough data given")
            sys.exit(1)

    sma = sum_for_avg / ema_length    
    smoothing_factor = 2
    multiplier = smoothing_factor / (ema_length + 1)
    start_day_price = price_data[i + 1]
    ema = start_day_price * multiplier + sma * (1 - multiplier) 
#    print("initial ema:", ema)
#    print("multiplier:", multiplier)
#    print("sma:", sma)
#    print("start:", start_day_price)
        
    coins_owned = 0
    cash_money = starting_capital
    bought = False
    today_price = None
    initial_coin_purchase = None
    for today_price in price_data[i+2:]: 
        if initial_coin_purchase is None: 
            max_purchase_amt = cash_money / (1 + fee_rate)
            initial_coin_purchase = max_purchase_amt / today_price

        signal_price = ema * ((1 + price_movement_threshold) if not bought else (1 - price_movement_threshold))
        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "signal price: "  + format(signal_price, ".2f"))
#            print("cash: " + str(cash_money) + "    " + "coins owned: " + str(coins_owned))

        if bought == False and today_price > signal_price: 
            bought = True   
            max_purchase_amt = cash_money / (1 + fee_rate)
            cash_money = 0
            coins_owned += max_purchase_amt / today_price 
            if verbose_output:
                print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))

        elif bought == True and today_price < signal_price: 
            bought = False
            cash_money += (coins_owned * today_price) / (1 + fee_rate)
            if verbose_output:
                print("sold " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
            coins_owned = 0

        # update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier)  
 
    if bought: 
        cash_money += (coins_owned * today_price) / (1 + fee_rate)
    
    algo_returns = (cash_money - starting_capital) / starting_capital
    market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital
    
    if not silent:
        print("algo: " + format(algo_returns, ".2%"))
        print("market: " + format(market_returns, ".2%"))

    return algo_returns - market_returns


if __name__ == "__main__": 
    main()
