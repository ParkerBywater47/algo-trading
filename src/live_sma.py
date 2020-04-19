import sys 
import time
import alpaca_trade_api


def main(): 
    """
    see usage function
    """
    has_header = True
    prices_csv = None
    verbose_output = False
    simulation = False
   
    # try to open the file 
    if len(sys.argv) == 1:
        print("Error: no data file given")
        sys.exit(1)
    
    print("Data file: " + sys.argv[1])
    i = 1  
    while i < len(sys.argv): 
        if i == 1: 
            prices_csv = open(sys.argv[1])
        else: 
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
                        days_in_average = int(sys.argv[i + 1])
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
    
    sma(prices=prices_csv, days_in_average=5, simulation_mode=simulation, verbose_output=verbose_output, csv_col_idx = 4)
    prices_csv.close()
    

def sma(prices, days_in_average, simulation_mode, verbose_output, csv_col_idx):
    initial_price = 0

    # compute the moving average 
    prev_days = []
    sum_for_avg = 0
    for i in range(days_in_average): 
        line = prices.readline()
        if i == 0: 
            initial_price = float(line.split(",")[csv_col_idx])
        if line != "": 
            sum_for_avg += float(line.split(",")[csv_col_idx])
            prev_days.append( float(line.split(",")[csv_col_idx]))
        else: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)

    moving_avg = sum_for_avg / days_in_average
   
    # buy the stock to start 
    bank_acct = 500 
    stock_acct = 0
    bought = False
    
    for line in prices: 
        today_price = float(line.split(",")[csv_col_idx]) 
        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "avg: "  + format(moving_avg, ".2f"))

        if bought == False and today_price > moving_avg: 
            bought = True   
            stock_acct += today_price
            bank_acct -= today_price
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("bought at " + format(today_price, ".2f"))

        elif bought == True and today_price < moving_avg: 
            bought = False
            stock_acct -= today_price
            bank_acct += today_price
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("sold at " + format(today_price, ".2f"))

        # update moving average  
        prev_days.append(today_price)
        prev_days.pop(0)
        
        sum_for_avg = 0
        for i in prev_days:
            sum_for_avg += i
        moving_avg = sum_for_avg / len(prev_days)

  

    # Report stuff if this was ran in simulation mode
    if simulation_mode: 
        print("stock value = " + format(today_price, ".2f"))
        print("bank_acct = " + format(bank_acct, ".2f"))
        print("total = " + format(today_price + bank_acct, ".2f"))
        print("if bought and held: " + format(today_price - initial_price, ".2f") + "\n")

 
def usage(): 
    print("""USAGE: python macd.py data-file [options]
OPTIONS: 
    -d, --days-in-average <num> 
    \t\tSpecify how many days should be used to compute the moving average. 
    \t\tProgram uses 5 days if this option is not used.                          

    -h --has-header <t|true|f|false>
    \t\tSpecify whether or not data-file has a header with. 
    \t\tProgram assumes true if option is not used.
"""
)












if __name__ == "__main__": 
    main()
