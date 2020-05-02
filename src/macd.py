import sys 
import time


def main(): 
    """
    see usage function
    """
    has_header = True
    verbose_output = True
    data_file = None 
    short_ema_length = 12
    long_ema_length = 26
    smoothing_factor = 2
   
    # try to open the file 
    if len(sys.argv) < 2:
        print("Error: no data file given")
        usage()
        sys.exit(1)
    
    i = 1
    while i < len(sys.argv):  
        if i == len(sys.argv) - 1: 
            data_file = sys.argv[i] 
        elif sys.argv[i] == "-h":
            try: 
                arg = sys.argv[i + 1] 
                if arg == "f" or arg == "false": 
                    has_header = False 
                elif not (arg == "t" or arg == "true"): 
                    print("Error: invalid arg '" + arg + "' with -h option")
                    sys.exit(1)
                # extra increment because args were good if we got to this point
                i = i + 1
            except IndexError: 
                print("Error: expected arg with -h option")
                sys.exit(1)      
        elif sys.argv[i] == "-s": 
            try:
                short_ema_length = int(sys.argv[i + 1])
                # extra increment because args were good if we got to this point
                i = i + 1
            except IndexError:
                print("Error: Expected argument with '" + sys.argv[i] + "' option")
                sys.exit(1)
            except ValueError:
                print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                sys.exit(1)
        elif sys.argv[i] == "-l":             
            try:
                long_ema_length = int(sys.argv[i + 1])
                # extra increment because args were good if we got to this point
                i = i + 1
            except IndexError:
                print("Error: Expected argument with '" + sys.argv[i] + "' option")
                sys.exit(1)
            except ValueError:
                print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                sys.exit(1)
        elif sys.argv[i] == "-m": 
            try: 
                smoothing_factor = float(sys.argv[i + 1])
                # extra increment because args were good if we got to this point
                i = i + 1
            except IndexError:
                print("Error: Expected argument with '" + sys.argv[i] + "' option")
                sys.exit(1)
            except ValueError:
                print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                sys.exit(1)
        elif sys.argv[i] == "-v": 
            verbose_output = False
        else: 
            print("Error: Invalid arg '" + sys.argv[i] + "'")
            sys.exit(1)
        i = i + 1

        if data_file is None: 
            print("Error: No data file given")
            sys.exit(1)
        
        if long_ema_length <= short_ema_length: 
            print("Error: long EMA length must be greater than short EMA length")
            sys.exit(1) 

        with open(data_file) as f:  
            # discard the header if it has one
            if has_header: 
                f.readline()        
            macd(f, short_ema_length, long_ema_length, smoothing_factor, verbose_output, csv_col_idx=4)
    

def macd(prices, short_ema_length, long_ema_length, smoothing_factor, verbose_output, csv_col_idx):
    short_days = []
    long_days = []

    # compute the initial smas 
    for i in range(short_ema_length): 
        line = prices.readline()
        if i == 0: 
            initial_price = float(line.split(",")[csv_col_idx])
        if line != "": 
            short_days.append(float(line.split(",")[csv_col_idx]))
            long_days.append(float(line.split(",")[csv_col_idx]))
        else: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)

    for i in range(long_ema_length - short_ema_length): 
        line = prices.readline()
        if line != "": 
            long_days.append(float(line.split(",")[csv_col_idx]))
        else: 
            print("Error: Not enough data for number of days in moving average")
            sys.exit(1)

    short_sma = average(short_days) 
    long_sma = average(long_days) 
    short_multiplier = smoothing_factor / (short_ema_length + 1)
    long_multiplier = smoothing_factor / (long_ema_length + 1)
    signal_ema_length = 9  
    signal_line_multiplier = smoothing_factor / (signal_ema_length + 1)

    # set up the emas
    today = float(prices.readline().split(",")[csv_col_idx]) 
    short_ema = today * short_multiplier + short_sma * (1 - short_multiplier)  
    long_ema = today * long_multiplier + long_sma * (1 - long_multiplier)  
    macd = short_ema - long_ema
    macdees = [macd]
    
    for i in range(signal_ema_length - 1):
        today = float(prices.readline().split(",")[csv_col_idx]) 
        short_ema = today * short_multiplier + short_ema * (1 - short_multiplier)  
        long_ema = today * long_multiplier + long_ema * (1 - long_multiplier)  
        macdees.append(short_ema - long_ema) 

    macd_sma = average(macdees)
    today_price = float(prices.readline().split(",")[csv_col_idx]) 
    short_ema = today * short_multiplier + short_ema * (1 - short_multiplier)  
    long_ema = today * long_multiplier + long_ema * (1 - long_multiplier)  
    macd = short_ema - long_ema
    signal_line = macd * signal_line_multiplier + macd_sma * (1 - signal_line_multiplier)

    bank_acct = 1_000_000 
    bought = False
    for line in prices: 
        
        if verbose_output:
            print("macd: " + format(macd, "<10.2f")  + "signal line: "  + format(signal_line, ".2f"))

        if bought == False and macd > signal_line: 
            bought = True   
            bank_acct -= today_price
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("bought at " + format(today_price, ".2f"))
        elif bought == True and macd < signal_line: 
            bought = False
            bank_acct += today_price
            if verbose_output or line.startswith(time.strftime("%Y-%m-%d")):
                print("sold at " + format(today_price, ".2f"))

        today_price = float(line.split(",")[csv_col_idx]) 
        short_ema = today_price * short_multiplier + short_ema * (1 - short_multiplier)  
        long_ema = today_price * long_multiplier + long_ema * (1 - long_multiplier)  
        macd = short_ema - long_ema
        signal_line = macd * signal_line_multiplier + signal_line * (1 - signal_line_multiplier)

    # Report results
    if bought: 
        bank_acct += today_price
    print("bank_acct = " + format(bank_acct, ".2f"))
    print("if bought and held: " + format(today_price - initial_price, ".2f") + "\n")

 
def usage(msg=None): 
    if msg is None: 
        print("""USAGE: python macd.py data-file [options]
    OPTIONS: 
        -s, --short-ema-length <num> 
        \t\tSpecify how many days should be used to compute the short EMA. 
        \t\tProgram uses 12 days if this option is not used.                          
        
        -l, --long-ema-length <num> 
        \t\tSpecify how many days should be used to compute the long EMA. 
        \t\tProgram uses 26 days if this option is not used.                          

        -h --has-header <[t|true]|[f|false]>
        \t\tSpecify whether or not data-file has a header. 
        \t\tProgram assumes true if option is not used.""")
    else: 
        print(msg)


def average(lst): 
    the_sum = 0
    for i in lst:
        the_sum += i
    return the_sum / len(lst)


if __name__ == "__main__": 
    main()
