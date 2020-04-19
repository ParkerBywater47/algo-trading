import sys

def main(): 
    
    # deal with a data file ...

    f = open(sys.argv[1])
    
    # discard header
    f.readline()
    
    # the 4th column is closing price
    col_idx = 4

    # two counters
    average_days_in_downtrend = 1.4285714285714286 
    average_days_in_uptrend = 1.5714285714285714
     
    down_days = []
    up_days = [] 
    
    days_in_downtrend = 0
    days_in_uptrend = 0
    in_downtrend = False
    yesterday_price = float(f.readline().split(",")[4])
    while len(up_days) < 4 and len(down_days) < 4: 
        line = f.readline()
        today_price = float(line.split(",")[4]) 
        # trend logic
        if today_price < yesterday_price and not in_downtrend:
            print("do I get here")
            up_days.append(days_in_uptrend)
            in_downtrend = True
            days_in_downtrend += 1
            days_in_uptrend = 0
        elif today_price > yesterday_price and in_downtrend: 
            print("do I get here")
            down_days.append(days_in_downtrend)
            in_downtrend = False
            days_in_uptrend += 1
            days_in_downtrend = 0
        elif today_price < yesterday_price: 
            days_in_downtrend += 1
        elif today_price > yesterday_price:
            days_in_uptrend += 1 
        yesterday_price = today_price
        
    print(down_days) 
    print(up_days) 
    sys.exit(0)

    initial_price = yesterday_price
    print("init:", initial_price)
    bought = False
    money = 1000
    for line in f: 
        today_price = float(line.split(",")[4])
        print(today_price)

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
    
        # buy logic
        if days_in_downtrend > average_days_in_downtrend and not bought: 
            bought = True
            money -= today_price
            print("bought @", today_price)
        elif bought and days_in_uptrend > average_days_in_uptrend: 
            bought = False
            money += today_price
            print("sold @", today_price)

        # update price
        yesterday_price = today_price
    
    # print simulation results 
    if bought: 
        money += today_price 
    print("net:", money - 1000) 
    print("b&h:", (today_price - initial_price))
            

def lwma(days): 
    the_sum = 0
    n = len(days)
    for i in range(n): 
        the_sum += days[i] * (i + 1)
    return the_sum / (n*(n-1) * 0.5) 





main()
