import cmc_api
import coinbase_api
from TradeAlgorithm import TradeAlgorithm


class Sma(TradeAlgorithm):
    def __init__(self, bought, coin_balance, cash_balance, previous_periods, logfile_path=None):
        self.__bought = False
        self.__coin_balance = coin_balance
        self.__cash_balance = cash_balance
        self.__previous_periods = previous_periods
        self.__threshold = .075 # see doc/testing-results.md to understand this number
        self.__logfile_path = logfile_path


    def run(self):
        print("ran algo")
        current_price = cmc_api.get_price()
        moving_avg = self.average(self.__previous_periods) 
        if self.__bought == False and current_price > moving_avg * (1 + self.__threshold) : 
            self.__bought = True   
            max_purchase_amt = self.__cash_balance / (1 + fee_rate)
            self.__cash_balance -= max_purchase_amt
            self.__coin_balance += max_purchase_amt / current_price 
            print("bought " + format(self.__coin_balance, ".5f") + " at " + format(current_price, ".2f") + " with sma = " + moving_avg)
            log = open(self.__logfile_path, "a")
            print("bought " + format(self.__coin_balance, ".5f") + " at " + format(current_price, ".2f") + " with sma = " + moving_avg, file=log)
            log.close() 

        elif self.__bought == True and current_price < moving_avg * (1 - self.__threshold): 
            self.__bought = False
            self.__cash_balance += (self.__coin_balance * current_price) / (1 + fee_rate)
            print("sold " + format(self.__coin_balance, ".5f") + " at " + format(current_price, ".2f") + " with sma = " + moving_avg)
            log = open(self.__logfile_path, "a")
            print("sold " + format(self.__coin_balance, ".5f") + " at " + format(current_price, ".2f") + " with sma = " + moving_avg, file=log)
            log.close() 
            self.__coin_balance = 0
      
        # update previous periods
        self.__previous_periods.append(current_price)
        self.__previous_periods.pop(0)

        

    def get_previous_periods(self): 
        return self.__previous_periods
