import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    sleep_time_in_seconds = 3599.850
    # TODO figure out Coinbase garbage to automatically fetch previous periods
    algo = Sma(bought=False, previous_periods=[44636.56, 44983.82, 45161.88], logfile_path="logs/btc_trade_driver.log")
    while True:                                
        algo.run()                             
        time.sleep(sleep_time_in_seconds)

if __name__ == "__main__":
    main()
                            
