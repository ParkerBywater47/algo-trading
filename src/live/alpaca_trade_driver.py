import time, sys
from DynamicEma import DynamicEma, Security

def main():
    some_wait_time = 3599.850 * 24 
    securities = [
]

    algo = DynamicEma(securities, logfile_path="logs/alpaca_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(some_wait_time) 


if __name__ == "__main__": 
    main()
