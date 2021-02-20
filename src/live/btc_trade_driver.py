import time, sys
from TradeAlgorithm import TradeAlgorithm
from Sma import Sma
from coinbase_api import get_historic_rates


def main():
    sleep_time_in_seconds = 3599.850

    # this automatically fetches recent price data, currently in testing only 
    prev = get_historic_rates()
    print("auto fetch of historic rates:", prev)

    algo = Sma(bought=False, previous_periods=[44636.56, 44983.82, 45161.88], logfile_path="logs/btc_trade_driver.log")
    while True:                                
        algo.run()                             
        time.sleep(sleep_time_in_seconds)

if __name__ == "__main__":
    main()
                            
