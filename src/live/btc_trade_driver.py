import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma


def main():
    sleep_time_in_seconds = 3599.850
    algo = Sma(bought=False, previous_periods=[9642.59, 9652.89, 9618.67], logfile_path="logs/btc_trade_driver.log")
    while True:
        algo.run()
        time.sleep(sleep_time_in_seconds)

if __name__ == "__main__":
    main()
                            
