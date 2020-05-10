import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    starting_capital = 450          # This will become a Coinbase API call eventually
    wait_time_between_updates = 275          
    an_hour = 3600                  # an hour in seconds for code readablility
    last_algo_update = time.time() - wait_time_between_updates # subtract an hour from the time so that the price is polled and the algo runs right when the script runs, not an hour later
    last_trade_time = time.time() - an_hour
    algo = Sma(bought=False, coin_balance=0, cash_balance=450, previous_periods=[9691.34, 9750.07, 9756.42, 9718.63, 9719.22], logfile_path="logs/btc_trade_driver.log") 
    while True:
        if time.time() >= last_algo_update + wait_time_between_updates:
            last_algo_update = time.time()
            temp = algo.run(last_trade_time)  
            if temp != last_trade_time:
                last_trade_time = temp
                time.sleep(an_hour)  
            else:
                print(algo.get_previous_periods())
                time.sleep(wait_time_between_updates)


if __name__ == "__main__": 
    main()
