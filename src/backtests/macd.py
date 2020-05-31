import sys 
import time


def simulate(price_data, short_ema_length=12, long_ema_length=26, signal_ema_length = 9, smoothing_factor=2, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    if not silent: 
        print(f"simulating macd({short_ema_length}, {long_ema_length}, {signal_ema_length}) with fee rate " + format(fee_rate, ".2%"))
    short_days = []
    long_days = []

    # compute the initial smas 
    for i in range(long_ema_length): 
        try:
            p = price_data[i] 
            if i >= long_ema_length - short_ema_length: 
                short_days.append(p)
            long_days.append(p)
        except IndexError: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)

    short_sma = average(short_days) 
    long_sma = average(long_days) 
    short_multiplier = smoothing_factor / (short_ema_length + 1)
    long_multiplier = smoothing_factor / (long_ema_length + 1)
    signal_line_multiplier = smoothing_factor / (signal_ema_length + 1)

    # set up the emas
    today = price_data[i + 1] 
    short_ema = today * short_multiplier + short_sma * (1 - short_multiplier)  
    long_ema = today * long_multiplier + long_sma * (1 - long_multiplier)  
    macd = short_ema - long_ema
    macdees = [macd]
    
    for j in range(i + 2, i + 2 + signal_ema_length - 1):
        today = price_data[j] 
        short_ema = today * short_multiplier + short_ema * (1 - short_multiplier)  
        long_ema = today * long_multiplier + long_ema * (1 - long_multiplier)  
        macdees.append(short_ema - long_ema) 

    macd_sma = average(macdees)
    today = price_data[j + 1] 
    short_ema = today * short_multiplier + short_ema * (1 - short_multiplier)  
    long_ema = today * long_multiplier + long_ema * (1 - long_multiplier)  
    macd_today = short_ema - long_ema
    signal_line = macd_today * signal_line_multiplier + macd_sma * (1 - signal_line_multiplier)

    cash_money = starting_capital 
    coins_owned = 0
    bought = False
    initial_coin_purchase = None
    #print("today_price" + "," + "short_ema" + "," + "long_ema" + "," + "macd" + "," + "signal_line")
    for today_price in price_data[j + 2:]: 
        #print(str(today_price) + "," + str(short_ema) + "," + str(long_ema) + "," + str(macd) + "," + str(signal_line))
        if initial_coin_purchase is None: 
            max_purchase_amt = cash_money / (1 + fee_rate)
            initial_coin_purchase = max_purchase_amt / today_price

        if verbose_output:
            print("macd: " + format(macd, "<10.2f")  + "signal line: "  + format(signal_line, ".2f"))

        if bought == False and macd > signal_line: 
            bought = True   
            max_purchase_amt = cash_money / (1 + fee_rate)
            cash_money = 0
            coins_owned += max_purchase_amt / today_price 
            if verbose_output:
                print("bought " + format(coins_owned, ".6f") + " at " + format(today_price, ".2f"))

        elif bought == True and macd < signal_line: 
            bought = False
            cash_money += (coins_owned * today_price) / (1 + fee_rate)
            if verbose_output:
                print("sold " + format(coins_owned, ".6f") + " at " + format(today_price, ".2f"))
            coins_owned = 0

        short_ema = today_price * short_multiplier + short_ema * (1 - short_multiplier)  
        long_ema = today_price * long_multiplier + long_ema * (1 - long_multiplier)  
        macd = short_ema - long_ema
        signal_line = macd * signal_line_multiplier + signal_line * (1 - signal_line_multiplier)

    # Report results
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
