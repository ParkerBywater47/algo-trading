import sys

def main(): 
    """
    <p>
    Simulates trading using a mean-reverting-esque strategy. 
    The strategy is basically this: <ol>
        <li> There is probably an average number of days that a stock trends down
        and a number of days that a stock trends up.
        <li> Theoretically, you could buy after a stock has trended down for its average number of days
            and sell after it's trended up for its average number of days.
        </ol>
    This is basically identical to dyamic_mean_rev.py, but differs in that it does not dynamically update 
    the value for average days in down/up-trends.
    </p> 
    """
    # deal with a data file ...
    if len(sys.argv) < 2: 
        print("RRRRREEEEEEEEEEE!!!! You forgot to specify your data file")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        # discard header
        f.readline()
        
        # the 4th column is closing price
        col_idx = 2 
#        col_idx = 0
        
        days_in_uptrend = 0
        days_in_downtrend = 0
        average_days_in_uptrend = 1.8958868894601542
        average_days_in_downtrend = 1.787917737789203

        bought = False
        money = 10000
        yesterday_price = float(f.readline().split(",")[col_idx])
        initial_price = yesterday_price
        print("init:", initial_price)
        name = f.readline().split(",")
        today_price =  float(name[col_idx])
        today = name[0]
        in_downtrend = today_price < yesterday_price
        for line in f: 
            # print(format(today_price, ".3f"),  "\tup:", format(average_days_in_uptrend, ".3f"), "\tdown:", format(average_days_in_downtrend, ".3f"))

            # trend logic
            if today_price < yesterday_price and not in_downtrend:
                in_downtrend = True
                days_in_downtrend += 1    
                days_in_uptrend = 0
            elif today_price > yesterday_price and in_downtrend: 
                in_downtrend = False
                days_in_uptrend += 1
                days_in_downtrend = 0
            elif today_price < yesterday_price: 
                days_in_downtrend += 1
            elif today_price > yesterday_price:
                days_in_uptrend += 1 
        
            if bought and today_price < stop_loss_price: 
                bought = False
                money += today_price
                print("stop-loss @ " + str(today_price) +  " on " + today + "\ncontinue trading?")

            # buy logic
            if days_in_downtrend >= average_days_in_downtrend and not bought: 
                bought = True
                money -= today_price * 1.002
                stop_loss_price = .90 * today_price
                print("bought @", today_price, "on " + today)
            elif bought and days_in_uptrend >= average_days_in_uptrend: 
                bought = False
                money += today_price * .998
                print("sold @", today_price, "on " + today)
            
            # update prices
            yesterday_price = today_price
            today_price = float(line.split(",")[col_idx])
            today = line.split(",")[0] 
        
        # print simulation results 
        if bought: 
            money += today_price 
        print("net:", money - 10000) 
        print("b&h:", (today_price - initial_price))


main()
