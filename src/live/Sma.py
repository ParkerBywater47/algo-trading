import coinbase_api
from TradeAlgorithm import TradeAlgorithm
import json 
from time import strftime
from functools import reduce

MAX_ORDER_FILL_TRIES = 10


class Sma(TradeAlgorithm):
    def __init__(self, bought, previous_periods, logfile_path=None):
        self.__bought = bought
        self.__previous_periods = previous_periods
        self.__threshold = .03 # see doc/testing-results.md to understand this number
        self.__log = open(logfile_path, "a")
        self.__fee_rate = .005
        self.__order_precision = 10 ** 6
        self.__stop_loss_id = None


    def run(self):
        if self.__check_stop_loss(): 
            self.__stop_loss_id = None
            self.__bought = False

        # trade stuff 
        current_price = coinbase_api.get_price()
        moving_avg = reduce((lambda x,y: x + y), self.__previous_periods) / len(self.__previous_periods)
       
        # logging stuff 
        signal_price = moving_avg * ((1 - self.__threshold) if self.__bought else (1 + self.__threshold))
        self.__do_logging("current_price: " + format(current_price, ".2f") + "\t signal price: " + format(signal_price, ".2f") + " previous: " + str(self.__previous_periods))

        if not self.__bought and current_price > moving_avg * (1 + self.__threshold): 
            self.__bought = True   

            bid_price = coinbase_api.get_bid() 
            stop_loss_price = int(bid_price * 100 * .9) / 100 
            
            # determine how much money can actually go into buying BTC after fees
            max_purchase_amt = coinbase_api.get_USDC_balance() / (1 + self.__fee_rate)

            # determine quantity of BTC to purchase            
            coin_purchase = int((max_purchase_amt / bid_price) * self.__order_precision) / self.__order_precision

            # make the orders and log the responses in case of error
            buy_order = {
                'size': coin_purchase,
                'price': int(bid_price * 100) / 100, 
                'side': 'buy',
                'product_id': 'BTC-USDC',
            }
            stop_loss_order = {
                'size': coin_purchase,
                'price': int(stop_loss_price * .9995 * 100)/ 100, 
                'side': 'sell', 
                'product_id': 'BTC-USDC',
                'stop': 'loss', 
                'stop_price': stop_loss_price
            }
            self.__do_logging("bought " + format(coin_purchase, ".5f") + " at " + format(bid_price, ".2f"))
            self.__do_logging("sent: " + str(buy_order))
            self.__do_logging(json.dumps(coinbase_api.coinbase_POST("/orders", buy_order), sort_keys=True, indent=4))
           
            # keep track of stop loss order id in case algo sells as part of normal operation
            # inside of loop because, although unlikely, it could possibly take some time to fill 
            # the order just placed
            tries = 0
            stop_loss_order_resp = {}
            while "id" not in stop_loss_order_resp and tries < MAX_ORDER_FILL_TRIES: 
                time.sleep(0.5)
                stop_loss_order_resp = coinbase_api.coinbase_POST("/orders", stop_loss_order)
                self.__do_logging("sent: " + str(stop_loss_order)) 
                self.__do_logging(json.dumps(stop_loss_order_resp, sort_keys=True, indent=4))
            self.__stop_loss_id = stop_loss_order_resp['id'] 

        elif self.__bought and current_price < moving_avg * (1 - self.__threshold): 
            self.__bought = False
            ask_price = coinbase_api.get_ask()
            max_sell_amt = coinbase_api.get_BTC_balance() / (1 + self.__fee_rate) 
            coins_to_sell = int(coinbase_api.get_BTC_balance() * self.__order_precision) / self.__order_precision

            sell_order = {
                'size': coins_to_sell,
                'price': int(ask_price * 100) / 100, 
                'side': 'sell',
                'product_id': 'BTC-USDC',
            }
            self.__do_logging("sold " + format(coins_to_sell, ".5f") + " at " + format(ask_price, ".2f")) 
            # post the sell order
            self.__do_logging(json.dumps(coinbase_api.coinbase_POST("/orders", sell_order), sort_keys=True, indent=4))

            # delete the old stop loss order
            if self.__stop_loss_id is not None:
                self.__do_logging(json.dumps(coinbase_api.coinbase_DELETE("/orders/" + self.__stop_loss_id), sort_keys=True, indent=4))
            else:
                self.__do_logging("[INFO] Encountered stop_loss_id == None ==> stop loss order for most recent buy was never placed")
      

        # update previous periods
        self.__previous_periods.append(current_price)
        self.__previous_periods.pop(0)
        

    def __do_logging(self, message):
        print(message, strftime('%c'))
        print(message, strftime('%c'), file=self.__log)


    def __check_stop_loss(self): 
        if self.__stop_loss_id is not None:
            resp = coinbase_api.coinbase_GET("/orders/" + self.__stop_loss_id)
            if "filled_size" in resp and float(resp["filled_size"]) > 0:
                return True 
        return False 
