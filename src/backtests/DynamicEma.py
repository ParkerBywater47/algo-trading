from TradeAlgorithm import TradeAlgorithm
import alpaca_trade_api
import find_optimal_ema

import json 
from time import strftime, sleep

class DynamicEma(TradeAlgorithm):
    """ 
    TradeAlgorithm subclass for algorithmically trading my alpaca account with dynamic ema strategy
    """
    def __init__(self, securities, logfile_path): 
        """
        :param securities: list of Security objects representing the securities to be traded by the algorithm
        :param api: A subclass of TradeApi
        """        
        self.__securities = securities
        self.__log = open(logfile_path, "a")
        self.__fee_rate = 0 

                
        key_file = open("keys/alpaca.txt")
        key_id = key_file.readline().strip()
        secret_key = key_file.readline().strip()
        key_file.close()

        self.__api = alpaca_trade_api.REST(key_id, secret_key, api_version='v2')
        self.__ema_smoothing_factor = 2

        self.__fill_time_allowed = 1
        self.__runs = 0

    def run(self): 
        # Iterate over traded securities 
        for s in self.__securities: 
            # check for stop loss or take_profit sells if the security was owned
             
            # do dynamic_ema 
            s.ema_length, s.price_movement_threshold, remove_later = find_optimal_ema.optimize(s.lookback_days, len(s.lookback_days) - s.optimal_lookback_length - 1, self.__fee_rate, False, True)[-1]

            # This will come out of the live version
            # Compute the ema if it's not already defined
            if s.ema is None: 
                sum_for_avg = 0
                for i in range(len(s.lookback_days) - s.ema_length - 1, len(s.lookback_days) - 1):
                    sum_for_avg += s.lookback_days[i]
                sma = sum_for_avg / s.ema_length
                s.ema_multiplier = self.__ema_smoothing_factor / (s.ema_length + 1)
                s.ema = s.lookback_days[len(s.lookback_days) - 1] * s.ema_multiplier + sma * (1 - s.ema_multiplier)
                
            signal_price = s.ema * ((1 + s.price_movement_threshold) if not s.currently_owned else (1 - s.price_movement_threshold))
           
            # I'll use one of these two numbers as the price for the day 
#            today_price = self.__api.get_last_quote(s.trade_symbol)._raw["bidprice"] 
            today_price = self.__api.get_last_trade(s.trade_symbol)._raw["price"]
            self.__do_logging(s.trade_symbol + "\ttoday price: " + format(today_price, ".2f") + "\tsignal price: " + format(signal_price, ".2f") + "\t" + str(s)) 
            if self.__runs == 10:
#            if not s.currently_owned and today_price > signal_price: 
                # some more api calls 
                bid_price = self.__api.get_last_quote(s.trade_symbol)._raw["bidprice"] 
                purchase_amt = int(s.tradable_balance / bid_price)
                order_resp = self.__api.submit_order(
                                symbol=s.trade_symbol,
                                side='buy',
                                type='market',
                                qty=purchase_amt, 
                                time_in_force='day',
                                order_class='bracket',
                                take_profit={ 
                                    "limit_price": str(1.15 * bid_price),
                                },  
                                stop_loss={
                                    "stop_price": str((1 - .075) * bid_price),
                                })
                self.__do_logging("sent order: " + json.dumps(dict( 
                                symbol=s.trade_symbol,
                                side='buy',
                                type='market',
                                qty=purchase_amt, 
                                time_in_force='day', 
                                order_class='bracket',
                                take_profit={ 
                                    "limit_price": str(1.15 * bid_price),
                                },  
                                stop_loss={
                                    "stop_price": str((1 - .075) * bid_price),
                                }), indent=4))
                self.__do_logging("received response: " + json.dumps(order_resp._raw, indent=4, sort_keys=True))
                s.order_id = order_resp._raw["id"]
                order = order_resp._raw

#                print(json.dumps(order_resp, indent=4, sort_keys=True))

                # check that order was not rejected
                if order["status"] != "rejected": 
                    # Give the order time to fill just in case it doesn't happen instantly
                    order = self.__api.get_order(s.order_id)._raw  
                    fill_time = 0
                    while int(order["filled_qty"]) != purchase_amt and fill_time <= self.__fill_time_allowed: 
                        sleep(1)
                        order = self.__api.get_order(s.order_id)._raw
                        fill_time += 1

                    # check that the order filled
                    if order["filled_avg_price"] is None: 
                        self.__api.cancel_order(s.order_id)
                        self.__do_logging("Order may not have filled. Sent cancel request. Order details: " + json.dumps(order, sort_keys=True, indent=4))
                    else:
                        s.currently_owned = True
                        s.tradable_balance -= float(order["qty"]) * float(order["filled_avg_price"])
                else:
                    # going to assume that this doesn't happen to start
                    pass

            elif self.__runs == 0:
#            elif s.currently_owned and today_price < signal_price: 
#                shares_owned = float(self.__api.get_order(s.order_id)._raw["qty"]) 
                shares_owned = float(self.__api.get_order("9ddf9f78-e548-419e-97c7-37620d3e2846")._raw["qty"]) 
                ask_price = self.__api.get_last_quote(s.trade_symbol)._raw["askprice"] 
                order_resp = self.__api.submit_order(
                                symbol=s.trade_symbol,
                                side='sell',
                                type='limit',
                                limit_price=str(ask_price),
                                qty=str(shares_owned), 
                                time_in_force='day',
                                order_class='simple')
                self.__do_logging("sent order: " + json.dumps(dict(
                                symbol=s.trade_symbol,
                                side='sell',
                                type='limit',
                                limit_price=ask_price,
                                qty=str(shares_owned), 
                                time_in_force='day',
                                order_class='simple'), indent=4))
                self.__do_logging("received response: " + json.dumps(order_resp._raw, indent=4, sort_keys=True))
                s.order_id = order_resp._raw["id"]
                order = order_resp._raw

                # check that order was not rejected
                if order["status"] != "rejected": 
                    # Give the order time to fill just in case it doesn't happen instantly
                    order = self.__api.get_order(s.order_id)._raw  
                    fill_time = 0
                    while int(order["filled_qty"]) != purchase_amt and fill_time <= 30: 
                        sleep(1)
                        order = self.__api.get_order(s.order_id)._raw
                        fill_time += 1

                    # check that the order filled
                    if order["filled_avg_price"] is None: 
                        self.__api.cancel_order(s.order_id)
                        self.__do_logging("Order may not have filled. Sent cancel request. Order details: " + json.dumps(order, indent=4, sort_keys=True))
                    else:
                        s.currently_owned = False
                        s.tradable_balance += float(order["qty"]) * float(order["filled_avg_price"])
                else:
                    # going to assume that this doesn't happen to start
                    pass

            self.__runs += 1            
            s.lookback_days.append(today_price)
            s.lookback_days.pop(0)

            s.days_since_readjustment += 1
            if s.days_since_readjustment % s.readjust_time == 0: 
                s.ema_length, s.price_movement_threshold, python_needs_this = find_optimal_ema.optimize(s.lookback_days, len(s.lookback_days) - s.optimal_lookback_length - 1, self.__fee_rate, False, True)[-1]
                s.ema_multiplier = self.__ema_smoothing_factor / (s.ema_length + 1)

            # update the ema
            s.ema = today_price * s.ema_multiplier + s.ema * (1 - s.ema_multiplier)            

    def __do_logging(self, message):
        print(message, strftime('%c'))
        print(message, strftime('%c'), file=self.__log)

class Security:     
    """ 
    A class to represent a security of the financial type. For example, a stock/ETF.
    """
    def __init__(self, trade_symbol, tradable_balance, ema, currently_owned, days_since_readjustment, readjust_time, optimal_lookback_length, lookback_days): 
        """
        :param trade_symbol: The ticker  
        :param tradable_balance: The amount (in USD) allotted to trading this security  
        :param currently_owned: Whether or not this security is currently owned 
        :param ema: The n-day ema for the security 
        """
        self.trade_symbol = trade_symbol
        self.tradable_balance = tradable_balance
        self.ema = ema
        self.ema_length = None
        self.price_movement_threshold = None 
        self.ema_multiplier = None
        self.currently_owned = currently_owned
        
        # Order id storage
        self.order_id = None
        self.stoploss_order_id = None
        self.take_profit_order_id = None

        self.days_since_readjustment = days_since_readjustment
        self.readjust_time = readjust_time
        self.optimal_lookback_length = optimal_lookback_length
        self.lookback_days = lookback_days 

        # This class member is made private becuase it should not change from its initial value
        self.__readjust_time = readjust_time  

    
    def get_readjust_time(): 
        return self.__readjust_time

    def __str__(self): 
        return self.trade_symbol + ", " + str(self.tradable_balance) + ", " + str(self.ema) + ", " + str(self.ema_length) + ", " + str(self.price_movement_threshold) + ", " + str(self.currently_owned) + ", " + str(self.days_since_readjustment) + ", " + str(self.lookback_days)
