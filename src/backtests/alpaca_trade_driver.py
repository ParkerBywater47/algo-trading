import time, sys


def main():
    an_hour = 3600                                              # an hour in seconds forcode readablility
    algo = Sma(bought=False, previous_periods=[9422.145, 9458.005, 9540.00], logfile_path="/dev/null") 
    while True:
        algo.run()  
        time.sleep(120) 


if __name__ == "__main__": 
    main()
