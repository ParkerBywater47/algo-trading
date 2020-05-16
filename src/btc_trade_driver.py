import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    starting_capital = 445                                      # This will become a Coinbase API call eventually
    an_hour = 3600                                              # an hour in seconds forcode readablility
    algo = Sma(bought=False, coin_balance=0, cash_balance=starting_capital, previous_periods=[9395.69, 9375.22, 9277.36], logfile_path="logs/btc_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(3600) 


if __name__ == "__main__": 
    main()
