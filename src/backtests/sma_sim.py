import sys 
import time

# these wouldn't be globals if Python supported constants
starting_capital = 450
fee_rate = .005


def main(): 
    """
    see usage function
    """
    has_header = True
    prices_csv = None
    verbose_output = False
    simulation = True

    # best performer
#    periods_in_average = 5
#    volatility_buffer = .075   

    # second best performer
#    periods_in_average = 13
#    volatility_buffer = 0.09   

    # a good performer over the 2020 dataset
    periods_in_average = 3 
    volatility_buffer = .03

    # try to open the file 
    if len(sys.argv) < 2:
        print("Error: no data file given")
        usage()
        sys.exit(1)
    
    prices_csv = open(sys.argv[1])
    with open(sys.argv[1]) as prices_csv:
        i = 2  
        while i < len(sys.argv): # have to do a while loop here because dumbass python 
            if sys.argv[i] == "-h":
                if i != len(sys.argv) -1: 
                    if sys.argv[i + 1] == "f" or sys.argv[i + 1] == "false":
                        has_header = False 
                        i = i+1
                    else:
                        print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                        sys.exit(1)
                else: 
                    print("Error: Expected argument with '" + sys.argv[i] + "' option")
                    sys.exit(1)
            elif sys.argv[i] == "-n":             
                if i != len(sys.argv) -1: 
                    if sys.argv[i + 1].isdigit():
                        periods_in_average = int(sys.argv[i + 1])
                        i = i+1 
                    else:
                        print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                        sys.exit(1)
                else: 
                    print("Error: Expected argument with '" + sys.argv[i] + "' option")
                    sys.exit(1)
            elif sys.argv[i] == "-v": 
                verbose_output = True
            elif sys.argv[i] == "-s":             
                simulation = True 
            else: 
                print("Error: Invalid arg '" + sys.argv[i] + "'")
                sys.exit(1)
            i = i + 1

        # discard the header if it has one
        if has_header: 
            prices_csv.readline()        
        price_data = []
        price_data_idx = 2

        simulate(prices, periods_in_average, simulation, verbose_output, volatility_buffer, csv_col_idx=2)
    

def simulate(price_data, sma_length=3, price_movement_threshold=.03, starting_capital=450, fee_rate=.005, verbose_output=False, silent=False):
    # compute the moving average to start
    sum_for_avg = 0
    for i in range(sma_length): 
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
        today = line.split(",")[0]
        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "avg: "  + format(moving_avg, ".2f"))
            print("cash: " + str(cash_money) + "    " + "coins owned: " + str(coins_owned))

        if bought == False and today_price > moving_avg * (1 + threshold) : 
            bought = True   
            max_purchase_amt = cash_money / (1 + fee_rate)
            cash_money = 0
            coins_owned += max_purchase_amt / today_price 
            if verbose_output:
                print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f") + " at " + today )

        elif bought == True and today_price < moving_avg * (1 - threshold) : 
            bought = False
            cash_money += (coins_owned * today_price) / (1 + fee_rate)
            if verbose_output: 
                print("sold " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f") + " at " + today)
            coins_owned = 0

        # update moving average  
        prev_days.append(today_price)
        prev_days.pop(0)
        moving_avg = average(prev_days)
  

    # Report stuff if this was ran in simulation mode
    if bought: 
        cash_money += (coins_owned * today_price) / (1 + fee_rate)

#        print(str(periods_in_average) + ", " + format(threshold, "5.3f") + "," + format((bank_acct -1_000_000) / (today_price - initial_price), "3.2f"))
#        print(initial_coin_purchase) 
    print("algo: " + format(cash_money - starting_capital, ".2f"))
    print("market: " + format((initial_coin_purchase * today_price / (1 + fee_rate))- starting_capital, ".2f"))


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


