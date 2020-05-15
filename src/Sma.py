import coinbase_api
from TradeAlgorithm import TradeAlgorithm
import json 
from time import strftime


class Sma(TradeAlgorithm):
    def __init__(self, bought, coin_balance, cash_balance, previous_periods, logfile_path=None):
        self.__bought = False
        self.__coin_balance = coin_balance
        self.__cash_balance = cash_balance
        self.__previous_periods = previous_periods
        self.__threshold = .03 # see doc/testing-results.md to understand this number
        self.__log = open(logfile_path, "a")
        self.__fee_rate = .005
        self.__smallest_trade_amt = .000001
        self.__stop_loss_id = None
        self.__runs = 0


    def run(self):
        if self.__check_stop_loss(): 
            self.__bought = False
            self.__coin_balance = 0

        # trade stuff 
        current_price = coinbase_api.get_price()
        ask_price = int(current_price * 1.0025 * 100) / 100
        stop_loss_price = int(ask_price * 100 * .9) / 100 
        moving_avg = self.average(self.__previous_periods) 
       
        # logging stuff 
        signal_price = moving_avg * ((1 - self.__threshold) if self.__bought else (1 + self.__threshold))
        self.__do_logging("current_price: " + format(current_price, ".2f") + "\t signal price: " + format(signal_price, ".2f") + " previous: " + str(self.__previous_periods))

        if self.__bought == False and current_price > moving_avg * (1 + self.__threshold): 
            self.__bought = True   
            max_purchase_amt = self.__cash_balance / (1 + self.__fee_rate)
            self.__cash_balance = 0
            self.__coin_balance += int((max_purchase_amt / ask_price) * (1 / self.__smallest_trade_amt)) * self.__smallest_trade_amt
            self.__do_logging("bought " + format(self.__coin_balance, ".5f") + " at " + format(ask_price, ".2f"))
            
            buy_order = {
                'size': self.__coin_balance,
                'price': ask_price, 
                'side': 'buy',
                'product_id': 'BTC-USDC',
            }
            stop_loss_order = {
                'size': self.__coin_balance,
                'price': int(stop_loss_price * .9975 * 100)/ 100, 
                'side': 'sell', 
                'product_id': 'BTC-USDC',
                'stop': 'loss', 
                'stop_price': stop_loss_price
            }
            #coinbase_api.coinbase_POST("/orders", buy_order),
            self.__do_logging(json.dumps(coinbase_api.coinbase_POST("/orders", buy_order), sort_keys=True, indent=4))
            stop_loss_order_resp = coinbase_api.coinbase_POST("/orders", stop_loss_order)
            self.__do_logging(json.dumps(stop_loss_order_resp, sort_keys=True, indent=4))

            if "id" in stop_loss_order_resp: 
                self.__stop_loss_id = stop_loss_order_resp['id'] 

        elif self.__bought == True and current_price < moving_avg * (1 - self.__threshold): 
            # trade stuff 
            current_price = coinbase_api.get_price()
            sell_price = int(current_price * .9975 * 100) / 100
            moving_avg = self.average(self.__previous_periods) 

            # logging stuff 
            log = open(self.__logfile_path, "a")
            self.__do_logging("current_price: " + format(current_price, ".2f") + "\t signal price: " + format(moving_avg * (1 + self.__threshold), ".2f"))

            self.__bought = False
            self.__cash_balance += (self.__coin_balance * sell_price) / (1 + self.__fee_rate)
            self.__do_logging("sold " + format(self.__coin_balance, ".5f") + " at " + format(sell_price, ".2f")) 
            sell_order = {
                'size': self.__coin_balance,
                'price': sell_price, 
                'side': 'sell',
                'product_id': 'BTC-USDC',
            }
            #coinbase_api.coinbase_POST("/orders", sell_order)
            self.__do_logging(json.dumps(coinbase_api.coinbase_POST("/orders", sell_order), sort_keys=True, indent=4))
            # delete the old stop loss order
            #coinbase_api.coinbase_DELETE("/orders/" + self.__stop_loss_id)
            self.__do_logging(json.dumps(coinbase_api.coinbase_DELETE("/orders/" + self.__stop_loss_id), sort_keys=True, indent=4))
            self.__coin_balance = 0
      
        # update previous periods
        self.__previous_periods.append(current_price)
        self.__previous_periods.pop(0)
        
        self.__runs += 1
        

    def __do_logging(self, message):
        print(message, strftime('%c'))
        print(message, strftime('%c'), file=self.__log)


    def __check_stop_loss(self): 
        if self.__stop_loss_id is not None:
            resp = coinbase_api.coinbase_GET("/orders/" + self.__stop_loss_id)
            if "filled_size" in resp and float(resp["filled_size"]) > 0:
                return True 
        return False 
