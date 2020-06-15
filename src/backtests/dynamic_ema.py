import find_optimal_ema


def simulate(price_data, lookback_length, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    update_time = 27
    if not silent: 
        print("simulating dynamic ema with readjustment time " + str(update_time) + " and lookback length " + str(lookback_length) + ", fee rate " + format(fee_rate, ".2%"))

    lookback_days = price_data[:lookback_length]
    #print(len(lookback_days))
    ema_length, price_movement_threshold, python_needs_this = find_optimal_ema.optimize(lookback_days, fee_rate=fee_rate, verbose_output=False, silent=True)[-1]    

    # compute an sma to start
    sum_for_avg = 0 
    for i in range(lookback_length, lookback_length + ema_length): 
        try:
            p = price_data[i]
            sum_for_avg += p
        except IndexError:
            print("Error: Not enough data given")
            sys.exit(1)

    sma = sum_for_avg / ema_length    
    smoothing_factor = 2
    multiplier = smoothing_factor / (ema_length + 1)
    start_day_price = price_data[i + 1]
    ema = start_day_price * multiplier + sma * (1 - multiplier) 
    lookback_days = price_data[i - lookback_length + 2:i+2]

#    print(ema_length, lookback_length + ema_length -1 )
#    print(i - lookback_length + 2, i+2 - 1)
#    print("start_day_idx: " + str(i + 2))
    
    coins_owned = 0
    cash_money = starting_capital
    bought = False
    today_price = None
    initial_coin_purchase = None
    days_since_update = 0
    for today_price in price_data[i+2:]: 
        if initial_coin_purchase is None: 
            max_purchase_amt = cash_money / (1 + fee_rate)
            initial_coin_purchase = max_purchase_amt / today_price
#            print("initial buy of", initial_coin_purchase, "@", today_price, "at")

        signal_price = ema * ((1 + price_movement_threshold) if not bought else (1 - price_movement_threshold))
        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "signal price: "  + format(signal_price, ".2f"))
#            print("cash: " + str(cash_money) + "    " + "shares owned: " + str(coins_owned))

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
        
        lookback_days.append(today_price)
        lookback_days.pop(0)

        days_since_update += 1
        if days_since_update % update_time == 0: 
#            print("first and last of lookback_days: " + str(lookback_days[0]) + " " + str(lookback_days[len(lookback_days) - 1]))
            ema_length, price_movement_threshold, python_needs_this = find_optimal_ema.optimize(lookback_days, fee_rate=fee_rate, verbose_output=False, silent=True)[-1]    
#            print("updated ema to " + str(ema_length) +  ", " + format(price_movement_threshold, ".1%"))
            multiplier = smoothing_factor / (ema_length + 1)

        # update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier)  
 

    if bought: 
        cash_money += (coins_owned * today_price) / (1 + fee_rate)
    
    algo_returns = (cash_money - starting_capital) / starting_capital
    market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital
   
    if not silent:
        print("algo: " + format(algo_returns, ".2%"))
        print("market: " + format(market_returns, ".2%"))

    #print(format(algo_returns - market_returns, ".2%") + ", " + ("+" if algo_returns > 0 else "-"))
    return algo_returns - market_returns



