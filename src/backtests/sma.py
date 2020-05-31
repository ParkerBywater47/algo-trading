import sys 
import time


def simulate(price_data, sma_length=3, price_movement_threshold=.03, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    if not silent: 
        print("simulating sma with length " + str(sma_length) + ", price movement threshold " + format(price_movement_threshold, ".2%") + ", fee rate " + format(fee_rate, ".2%"))

    # compute the moving average to start
    prev_days = []
    for i in range(sma_length): 
        try:
            prev_days.append(price_data[i])
        except IndexError:
            print("Error: Not enough data given")
            sys.exit(1)

    sma = average(prev_days)
    coins_owned = 0
    cash_money = starting_capital
    bought = False
    first_simulated_day = True 
    for today_price in price_data[i+1:]: 
        if first_simulated_day: 
            max_purchase_amt = starting_capital / (1 + fee_rate)
            initial_coin_purchase = max_purchase_amt / price_data[i] 
            first_simulated_day = False

        signal_price = sma * ((1 + price_movement_threshold) if not bought else (1 - price_movement_threshold))
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

        # update moving average  
        prev_days.append(today_price)
        prev_days.pop(0)
        moving_avg = average(prev_days)

    if bought: 
        cash_money += (coins_owned * today_price) / (1 + fee_rate)

    algo_returns = (cash_money - starting_capital) / starting_capital
    market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital
    
    if not silent:
        print("algo: " + format(algo_returns, ".2%"))
        print("market: " + format(market_returns, ".2%"))

    return algo_returns - market_returns


def average(lst): 
    the_sum = 0
    for i in lst:
        the_sum += i
    return the_sum / len(lst)


if __name__ == "__main__": 
    main()


