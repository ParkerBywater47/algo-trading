import time, sys
from DynamicEma import DynamicEma, Security
import polygon


def main():
    some_wait_time = 3599.850 * 24 
    a_year = 31536000 # a year in seconds 
    a_day = 3600 * 24 # day in seconds 
    with open("keys/polygon.txt") as key_file: 
        polygon_api = polygon.RESTClient(key_file.readline().strip()) 
   
    now = time.time() 
    start_date = time.strftime("%Y-%m-%d", time.localtime(now - a_year))
    end_date = time.strftime("%Y-%m-%d", time.localtime(now + a_day))
    # TODO Read configuration values for securities from a config file instead
    securities = [

Security("CCL", 21.03, None, True, 8, 25, 123,  [x["c"] for x in polygon_api.stocks_equities_aggregates("CCL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),   
Security("KOS", 2.265, None, True, 8, 36, 107,  [x["c"] for x in polygon_api.stocks_equities_aggregates("KOS", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("XOM", 65.774997, None, False, 8, 23, 114,  [x["c"] for x in polygon_api.stocks_equities_aggregates("XOM", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("MRO", 8.97, None, True, 8, 7, 121,  [x["c"] for x in polygon_api.stocks_equities_aggregates("MRO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("RCL", 74.29499849999999, None, True, 8, 31, 113,  [x["c"] for x in polygon_api.stocks_equities_aggregates("RCL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("SLB", 29.25, None, True, 8, 17, 124,  [x["c"] for x in polygon_api.stocks_equities_aggregates("SLB", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("UCO", 49.4399985, None, False, 8, 34, 126,  [x["c"] for x in polygon_api.stocks_equities_aggregates("UCO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("USO", 45.345, None, False, 8, 26, 110,  [x["c"] for x in polygon_api.stocks_equities_aggregates("USO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("WFC", 36.599999999999994, None, True, 8, 26, 115,  [x["c"] for x in polygon_api.stocks_equities_aggregates("WFC", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("CSCO", 70.995003, None, False, 8, 19, 72,  [x["c"] for x in polygon_api.stocks_equities_aggregates("CSCO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  
Security("HAL", 6.3201, None, True, 8, 32, 114,  [x["c"] for x in polygon_api.stocks_equities_aggregates("HAL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),  

]

    algo = DynamicEma(securities, logfile_path="logs/alpaca_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(some_wait_time) 


def construct_securities(tickers: list): 
    for i in tickers:
        pass

if __name__ == "__main__": 
    main()
