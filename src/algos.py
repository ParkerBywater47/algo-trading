import 


def sma(prices, periods_in_average, simulation_mode, verbose_output, threshold, csv_col_idx):
    # compute the moving average to start
    prev_days = []
    for i in range(periods_in_average): 
        line = prices.readline()
        if i == 0: 
            max_purchase_amt = starting_capital / (1 + fee_rate)
            initial_coin_purchase = max_purchase_amt / float(line.split(",")[csv_col_idx]) 
#            initial_price = float(line.split(",")[csv_col_idx])
        if line != "": 
            prev_days.append(float(line.split(",")[csv_col_idx]))
        else: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)
    moving_avg = average(prev_days) 
    
    coins_owned = 0
    cash_money = starting_capital
    bought = False
    for line in prices: 
        today_price = float(line.split(",")[csv_col_idx]) 
#        if verbose_output:
#            print("today: " + format(today_price, "<10.2f")  + "avg: "  + format(moving_avg, ".2f"))

        if bought == False and today_price > moving_avg * (1 + threshold) : 
            bought = True   
            max_purchase_amt = cash_money / (1 + fee_rate)
            cash_money -= max_purchase_amt
            coins_owned += max_purchase_amt / today_price 
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))

        elif bought == True and today_price < moving_avg * (1 - threshold) : 
            bought = False
            cash_money += (coins_owned * today_price) / (1 + fee_rate)
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
            coins_owned = 0

        # update moving average  
        prev_days.append(today_price)
        prev_days.pop(0)
        moving_avg = average(prev_days)
  

    # Report stuff if this was ran in simulation mode
    if simulation_mode: 
        if bought: 
            cash_money += (coins_owned * today_price) / (1 + fee_rate)

#        print(str(periods_in_average) + ", " + format(threshold, "5.3f") + "," + format((bank_acct -1_000_000) / (today_price - initial_price), "3.2f"))
#        print(initial_coin_purchase) 
        print("algo: " + format(cash_money - starting_capital, ".2f"))
        print("market: " + format((initial_coin_purchase * today_price / (1 + fee_rate))- starting_capital, ".2f"))
