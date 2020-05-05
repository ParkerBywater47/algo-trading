import sys 
import time


def main(): 
    """
    see usage function
    """
    has_header = True
    prices_csv = None
    verbose_output = False
    simulation = False
    days_in_average = 5
   
    # try to open the file 
    if len(sys.argv) < 2:
        print("Error: no data file given")
        usage()
        sys.exit(1)
    
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
        
        sma(prices_csv, days_in_average, simulation,verbose_output, csv_col_idx=4)
    

def sma(prices, days_in_average, simulation_mode, verbose_output, csv_col_idx):
    # compute the moving average to start
    prev_days = []
    for i in range(days_in_average): 
        line = prices.readline()
        if i == 0: 
            initial_price = float(line.split(",")[csv_col_idx])
        if line != "": 
            prev_days.append(float(line.split(",")[csv_col_idx]))
        else: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)

    fee_rate = 0 
    moving_avg = average(prev_days) 
    bank_acct = 1_000_000 
    bought = False
    for line in prices: 
        today_price = float(line.split(",")[csv_col_idx]) 
        if verbose_output:
            print("today: " + format(today_price, "<10.2f")  + "avg: "  + format(moving_avg, ".2f"))

        if bought == False and today_price > moving_avg: 
            bought = True   
            bank_acct -= today_price * (1 + fee_rate) 
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("bought at " + format(today_price, ".2f"))

        elif bought == True and today_price < moving_avg: 
            bought = False
            bank_acct += today_price * (1 - fee_rate) 
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("sold at " + format(today_price, ".2f"))

        # update moving average  
        prev_days.append(today_price)
        prev_days.pop(0)
        moving_avg = average(prev_days)
  

    # Report stuff if this was ran in simulation mode
    if simulation_mode: 
        if bought: 
            bank_acct += today_price * (1 - fee_rate) 
        print("net:" + format(bank_acct -1_000_000 , ".2f"))
        print("b&h:" + format(today_price - initial_price, ".2f") + "\n")

 
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
