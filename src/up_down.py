import sys

def main(): 
       
    with open(sys.argv[1]) as f: 
        # discard header
        f.readline()
        
        # the 4th column is closing price
        col_idx = 4

        # two counters
        days_in_downtrend = 0
        days_in_uptrend = 0
        total_downtrends = 0
        total_uptrends = 0
        in_downtrend = False
        yesterday_price = float(f.readline().split(",")[4])

        for line in f:
            today_price = float(line.split(",")[4])
            if today_price < yesterday_price and in_downtrend: 
                days_in_downtrend += 1
            elif today_price < yesterday_price: 
                in_downtrend = True
                total_downtrends += 1
                days_in_downtrend += 1
            elif today_price > yesterday_price and not in_downtrend:
                days_in_uptrend += 1 
            elif today_price > yesterday_price: 
                in_downtrend = False
                total_uptrends += 1
                days_in_uptrend += 1
            yesterday_price = today_price
                
               
        print("average # days in downtrend:", days_in_downtrend / total_downtrends) 
        print("average # days in uptrend:", days_in_uptrend / total_uptrends) 
        print(total_downtrends)
        print(total_uptrends)


main()
