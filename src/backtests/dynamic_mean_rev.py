mport sys

def main(): 
    """
    <p>
    Simulates trading using a mean-reverting-esque strategy. 
    The strategy is basically this: <ol>
        <li> There is probably an average number of days that a stock trends down
        and a number of days that a stock trends up.
        <li> Theoretically, you could buy after a stock has trended down for its average number of days
            and sell after it's trended up for its average number of days 
    </ol>
    This is basically identical to _mean_rev.py, but differs in that it does dynamically update 
    the value for average days in down/up-trends.
    </p> 
    """
    # deal with a data file ...
    if len(sys.argv) > 1: 
        f = open(sys.argv[1])
    else: 
        print("RRRRREEEEEEEEEEE!!!! You forgot to specify your data file")
        sys.exit(1)
    
    # discard header
    f.readline()
    
    # the 4th column is closing price
    col_idx = 4

    downtrend_lengths = []
    uptrend_lengths = [] 
    
    days_in_downtrend = 0
    days_in_uptrend = 0
    yesterday_price = float(f.readline().split(",")[4])
    today_price =  float(f.readline().split(",")[4])
    in_downtrend = today_price < yesterday_price
    while len(uptrend_lengths) < 4 or len(downtrend_lengths) < 4: 
        # trend logic
        if today_price < yesterday_price and not in_downtrend:
            uptrend_lengths.append(days_in_uptrend)
            in_downtrend = True
            days_in_downtrend += 1
            days_in_uptrend = 0
        elif today_price > yesterday_price and in_downtrend: 
            downtrend_lengths.append(days_in_downtrend)
            in_downtrend = False
            days_in_uptrend += 1
            days_in_downtrend = 0
        elif today_price < yesterday_price: 
            days_in_downtrend += 1
        elif today_price > yesterday_price:
            days_in_uptrend += 1 
        yesterday_price = today_price
        today_price = float(f.readline().split(",")[4])

    average_days_in_downtrend = lwma(downtrend_lengths) # 1.4285714285714286 
    average_days_in_uptrend = lwma(uptrend_lengths) # 1.5714285714285714

    # reset these for the sake of proper simulation
#    days_in_downtrend = 0
#    days_in_uptrend = 0
#    in_downtrend = False

    initial_price = yesterday_price
    print("init:", initial_price)
    bought = False
    money = 10000
    for line in f: 
        today_price = float(line.split(",")[4])
        print(format(today_price, ".3f"),  "\tup:", format(average_days_in_uptrend, ".3f"), "\tdown:", format(average_days_in_downtrend, ".3f"))

        # trend logic
        if today_price < yesterday_price and not in_downtrend:
            in_downtrend = True
            uptrend_lengths.append(days_in_uptrend) 
            uptrend_lengths.pop(0)
            #print("uptrend_lengths:", uptrend_lengths)
            average_days_in_uptrend = lwma(uptrend_lengths) 
            days_in_downtrend += 1    
            days_in_uptrend = 0
        elif today_price > yesterday_price and in_downtrend: 
            in_downtrend = False
            downtrend_lengths.append(days_in_downtrend)
            downtrend_lengths.pop(0)
            #print("downtrend_lengths:", downtrend_lengths)
            average_days_in_downtrend = lwma(downtrend_lengths) 
            days_in_uptrend += 1
            days_in_downtrend = 0
        elif today_price < yesterday_price: 
            days_in_downtrend += 1
        elif today_price > yesterday_price:
            days_in_uptrend += 1 
    
        # buy logic
        if days_in_downtrend >= average_days_in_downtrend and not bought: 
            bought = True
            money -= today_price
            stop_loss_price = .75 * today_price
            print("bought @", today_price)
        elif bought and days_in_uptrend >= average_days_in_uptrend: 
            bought = False
            money += today_price
            print("sold @", today_price)
        elif bought and today_price < stop_loss_price: 
            bought = False
            money += today_price
            print("stop-loss @", today_price)

        # update price
        yesterday_price = today_price
    
    # print simulation results 
    if bought: 
        money += today_price 
    print("net:", money - 10000) 
    print("b&h:", (today_price - initial_price))
            

def lwma(days): 
    """
    Compute linearly weighted moving average. 
    Weights are currently just 1,2,3,4,5,.. 
    """
    the_sum = 0
    n = len(days)
    for i in range(n): 
        the_sum += days[i] * (i + 1)
    return the_sum / (n*(n+1) * 0.5) #weight_sum  



main()
