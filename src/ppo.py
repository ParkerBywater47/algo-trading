import sys

def main(): 
    """
    """
    # deal with a data file...
    if len(sys.argv) < 2: 
        print("RRRRREEEEEEEEEEE!!!! You forgot to specify your data file")
        sys.exit(1)
    
        
    col_idx = 2  # which column of the csv the closing price is located in (0 base index of course)
    fluctuation_percentage = 0.01
    while fluctuation_percentage <= .21: 

        with open(sys.argv[1]) as f:
            # discard header
            f.readline()

            fee_rate = 0.015 
    #        col_idx = 0
            
            days_in_uptrend = 0
            days_in_downtrend = 0
            average_days_in_uptrend = 1.8958868894601542
            average_days_in_downtrend = 1.787917737789203

            bought = True
            money = 10000
            name = f.readline().split(",")
            yesterday_price = float(name[col_idx])
            initial_price = yesterday_price
            money -= yesterday_price
            today = name[0]
            trades = 1 
            volume = 0 
            for line in f: 
                today_price = float(line.split(",")[col_idx])
                # print(format(today_price, ".3f"),  "\tup:", format(average_days_in_uptrend, ".3f"), "\tdown:", format(average_days_in_downtrend, ".3f"))
                if today_price <= yesterday_price * (1 - fluctuation_percentage) and not bought: 
                    volume += today_price
                    money -= today_price * (1 + fee_rate)
                    bought = True
                    stop_loss_price = .90 * today_price
    #                print("bought @", today_price, "on " + today)
                elif today_price <= yesterday_price * (1 + fluctuation_percentage) and bought: 
                    volume += today_price
                    money += today_price * (1 - fee_rate)
                    bought = False
    #                print("sold @", today_price, "on " + today)


                if bought and today_price < stop_loss_price: 
                    bought = False
                    money += today_price
                    print("stop-loss @ " + str(today_price) +  " on " + today + "\ncontinue trading?")

                # update prices
                yesterday_price = today_price
                today = line.split(",")[0] 
                trades += 1
            
            # print simulation results 
            if bought: 
                money += today_price 
            print("\nfluctuation percentage: " + format(100 * fluctuation_percentage, "3.2f") + "%") 
            print("net:", money - 10000) 
            print("b&h:", (today_price - initial_price))

        fluctuation_percentage += 0.005


main()



