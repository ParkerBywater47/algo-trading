import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    sleep_time_in_seconds = 3599                                
    algo = Sma(bought=False, previous_periods=[8778.11, 8810.0, 8783.19], logfile_path="logs/btc_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(sleep_time_in_seconds) 


if __name__ == "__main__": 
    main()
