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
    securities = [
Security("CCL", 21.03, 14.61, True, 4, 25, 123,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("CCL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),
Security("KOS", 2.265, 1.65, True, 4, 36, 107,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("KOS", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),
Security("XOM", 65.774997, 42.1767901090535, False, 4, 23, 114,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("XOM", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("MRO", 8.97, 5.72, True, 4, 7, 121,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("MRO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),
Security("RCL", 74.29499849999999, 60.44477365432098, True, 4, 31, 113,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("RCL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]),
Security("SLB", 29.25, 19.71586419547325, True, 4, 17, 124,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("SLB", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("UCO", 49.4399985, 33.08309027405248, False, 4, 34, 126,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("UCO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("USO", 45.345, 30.3071036408508, False, 4, 26, 110,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("USO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("WFC", 36.599999999999994, 24.1677648, True, 4, 26, 115, [x["c"] for x in polygon_api.stocks_equities_aggregates ("WFC", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("CSCO", 70.995003, 41.9, False, 4, 19, 72,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("CSCO", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
Security("HAL", 6.3201, 16.5, True, 4, 32, 114,  [x["c"] for x in polygon_api.stocks_equities_aggregates ("HAL", 1, "day", start_date, end_date, sort="asc", unadjusted=True).results]), 
]


    algo = DynamicEma(securities, logfile_path="logs/alpaca_trade_driver.log") 
    while True:
        algo.run()  
        time.sleep(some_wait_time) 


if __name__ == "__main__": 
    main()
