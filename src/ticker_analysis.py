import sys


def main(): 
    """
    just a script to do some analysis of coinbase websocket ticker channel 
    data 
    """
#    out = open("data/realtime_trimmed.csv", "w") 
    with open(sys.argv[1]) as f: 
        # discard header
        f.readline()
#        out.write(f.readline())
        
        # price data in column 0 with timestamp in column 1  
        price_col = 2 
        time_col = 0 

        # average price

        # average length of uptrend
        # average length of downtrend
        ticks_down = 0
        ticks_up = 0
        total_downtrends = 0
        total_uptrends = 0
        in_downtrend = False

        name = f.readline() # doesn't need a meaningful name
        prev_price = float(name.split(",")[price_col])
        prev_timestamp = name.split(",")[time_col]
#        out.write(name)

        max_price = prev_price
        min_price = prev_price
        
        # max number of ticks with identical timestamps 
        curr_at_same_timestamp = 1
        max_at_same_timestamp = 1

        # for max price difference of ticks with identical timestamps 
        max_in_same_timestamp = prev_price
        min_in_same_timestamp = prev_price
        max_same_timestamp_price_diff = 0
        
        for line in f:
            curr_price = float(line.split(",")[price_col])
            curr_timestamp = line.split(",")[time_col] 
    
            if curr_timestamp == prev_timestamp: 
                if curr_at_same_timestamp > 1:
                    max_in_same_timestamp = max(max_in_same_timestamp, curr_price)
                    min_in_same_timestamp = min(min_in_same_timestamp, curr_price)
                else: 
                    max_in_same_timestamp = curr_price 
                    min_in_same_timestamp = curr_price
                curr_at_same_timestamp += 1
            else: 
#                out.write(line)
                max_same_timestamp_price_diff = max(max_in_same_timestamp - min_in_same_timestamp, max_same_timestamp_price_diff)
                max_at_same_timestamp = max(max_at_same_timestamp, curr_at_same_timestamp) 
                
                # reset vars for the next timestamp
                max_in_same_timestamp = 0
                min_in_same_timestamp = 0
                curr_at_same_timestamp = 1
                
                if curr_price < prev_price and in_downtrend: 
                   ticks_down += 1
                elif curr_price < prev_price: 
                   in_downtrend = True
                   total_downtrends += 1
                   ticks_down += 1
                elif curr_price > prev_price and not in_downtrend:
                   ticks_up += 1 
                elif curr_price > prev_price: 
                   in_downtrend = False
                   total_uptrends += 1
                   ticks_up += 1

            max_price = max(max_price, curr_price)
            min_price = min(min_price, curr_price)
            prev_price = curr_price
            prev_timestamp = curr_timestamp
       
        print("max price:", max_price)         
        print("min price:", min_price)         
        print("max at same timestamp:", max_at_same_timestamp)
        print("max price difference at same timestamp:", max_same_timestamp_price_diff)
        
        print("average downtrend length:", ticks_down / total_downtrends) 
        print("average uptrend length:", ticks_up / total_uptrends) 
#    out.close()


main()
