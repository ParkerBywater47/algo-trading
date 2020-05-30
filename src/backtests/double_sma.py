import sys 
import time


def simulate(price_data, short_sma_length, long_sma_length, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    if not silent: 
        print("simulating double sma with lengths " + str(short_sma_length) + "," + str(long_sma_length))

    # compute the moving averages to start
    prev_periods_short_sma = []
    prev_periods_long_sma = []
    for i in range(long_sma_length): 
        try:
            p = price_data[i]
            if i >= long_sma_length - short_sma_length: 
                prev_periods_short_sma.append(p)
            prev_periods_long_sma.append(p) 
        except IndexError: 
            print("Error: Not enough data given")
            sys.exit(1)
   
    # print(len(prev_periods_short_sma), len(prev_periods_long_sma))      
    short_sma = average(prev_periods_short_sma) 
    long_sma = average(prev_periods_long_sma) 
     
    coins_owned = 0
    cash_money = starting_capital
    bought = False
    first_simulated_day = True
    for today_price in price_data[long_sma_length:]: 
        if first_simulated_day: 
            initial_coin_purchase = (cash_money / (1 + fee_rate)) / today_price 
            first_simulated_day = False            

        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "short sma: "  + format(short_sma, "<10.2f") + "long sma: " + format(long_sma, ".2f"))

        if bought == False and short_sma > long_sma: 
            bought = True   
            max_purchase_amt = cash_money / (1 + fee_rate)
            cash_money -= max_purchase_amt
            coins_owned += max_purchase_amt / today_price 
            if verbose_output:
                print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))

        elif bought == True and short_sma < long_sma: 
            bought = False
            cash_money += (coins_owned * today_price) / (1 + fee_rate)
            if verbose_output: 
                print("sold " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
            coins_owned = 0

        # update moving average  
        prev_periods_short_sma.append(today_price)
        prev_periods_long_sma.append(today_price)
        prev_periods_short_sma.pop(0)
        prev_periods_long_sma.pop(0)
        short_sma = average(prev_periods_short_sma)
        long_sma = average(prev_periods_long_sma)
  
    # Report simulation results
    if bought: 
        cash_money += (coins_owned * today_price) / (1 + fee_rate)

    algo_returns = (cash_money - starting_capital) / starting_capital
    market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital
    
    if not silent:
        print("algo: " + format(algo_returns, ".2%"))
        print("market: " + format(market_returns, ".2%"))

    return algo_returns - market_returns

def update_best(a_list, current): 
    if len(a_list) < 6:
        a_list.append(current)
    else:
        mindx = 0 
        minimum = a_list[0][2]
        for i in range(1, len(a_list)):
            if a_list[i][2] < minimum: 
                mindx = i
                minimum = a_list[i][2]
            
        if current[2] > minimum: 
            a_list[mindx] = current


def usage(): 
    print("""USAGE: python sma.py data-file [options]
OPTIONS: 
    -d, --days-in-average <num> 
    \t\tSpecify how many days should be used to compute the moving average. 
    \t\tProgram uses 5 days if this option is not used.                          

    -h --has-header <t|true|f|false>
    \t\tSpecify whether or not data-file has a header with. 
    \t\tProgram assumes true if option is not used.""")


def average(lst): 
    the_sum = 0
    for i in lst:
        the_sum += i
    return the_sum / len(lst)


if __name__ == "__main__": 
    main()


