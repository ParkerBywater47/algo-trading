import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    starting_capital = 450                                      # This will become a Coinbase API call eventually
    an_hour = 3600                                              # an hour in seconds for code readablility
    algo = Sma(bought=False, coin_balance=0, cash_balance=450, previous_periods=[8649.54, 8683.13, 8710.01, 8715.04, 8716.72], logfile_path="logs/btc_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(3600) 


if __name__ == "__main__": 
    main()
