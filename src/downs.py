import sys

def main(): 
    
    # deal with a data file ...
    if len(sys.argv)  > 1: 
        f = open(sys.argv[1])
    else: 
        print("RRRRREEEEEEEEEEE!!!! You forgot to specify your data file")
        sys.exit(1)
    
    # discard header
    f.readline()
    
    # the 4th column is closing price
    col_idx = 4

    down_days = []
    up_days = [] 
    
    days_in_downtrend = 0
    days_in_uptrend = 0
    in_downtrend = False
    yesterday_price = float(f.readline().split(",")[4])
    while len(up_days) < 4 or len(down_days) < 4: 
        line = f.readline()
        today_price = float(line.split(",")[4]) 
        # trend logic
        if today_price < yesterday_price and not in_downtrend:
            up_days.append(days_in_uptrend)
            in_downtrend = True
            days_in_downtrend += 1
            days_in_uptrend = 0
        elif today_price > yesterday_price and in_downtrend: 
            down_days.append(days_in_downtrend)
            in_downtrend = False
            days_in_uptrend += 1
            days_in_downtrend = 0
        elif today_price < yesterday_price: 
            days_in_downtrend += 1
        elif today_price > yesterday_price:
            days_in_uptrend += 1 
        yesterday_price = today_price

    average_days_in_downtrend = lwma(down_days) # 1.4285714285714286 
    average_days_in_uptrend = lwma(up_days) # 1.5714285714285714

    # reset these for the sake of proper simulation
    days_in_downtrend = 0
    days_in_uptrend = 0
    in_downtrend = False

    initial_price = yesterday_price
    print("init:", initial_price)
    bought = False
    money = 10000
    for line in f: 
        today_price = float(line.split(",")[4])
        print(format(today_price, ".3f"), "up:", format(average_days_in_uptrend, ".3f"), "down:", format(average_days_in_downtrend, ".3f"))

        # trend logic
        if today_price < yesterday_price and not in_downtrend:
            in_downtrend = True
            up_days.append(days_in_uptrend) 
            up_days.pop(0)
            print("up_days:", up_days)
            average_days_in_uptrend = lwma(up_days) 
            days_in_downtrend += 1    
            days_in_uptrend = 0
        elif today_price > yesterday_price and in_downtrend: 
            in_downtrend = False
            down_days.append(days_in_downtrend)
            down_days.pop(0)
            print("down_days:", down_days)
            average_days_in_downtrend = lwma(down_days) 
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
            print("bought @", today_price)
        elif bought and days_in_uptrend >= average_days_in_uptrend: 
            bought = False
            money += today_price
            print("sold @", today_price)

        # update price
        yesterday_price = today_price
    
    # print simulation results 
    if bought: 
        money += today_price 
    print("net:", money - 10000) 
    print("b&h:", (today_price - initial_price))
            

def lwma(days): 
    the_sum = 0
    n = len(days)
    for i in range(n): 
        the_sum += days[i] * (i + 1)
    return the_sum / (n*(n+1) * 0.5) #weight_sum  



main()
