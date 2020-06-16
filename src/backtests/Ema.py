from TradeAlgorithm import TradeAlgorithm
import alpaca_trade_api
import find_optimal_ema


class DynamicEma(TradeAlgorithm):
    """ 
    TradeAlgorithm subclass for algorithmically trading my alpaca account with dynamic ema strategy
    """
    def __init__(self, securities, api): 
        """
        :param securities: list of Security objects representing the securities to be traded by the algorithm
        :param api: A subclass of TradeApi
        """        
        self.__securities = securities
        self.__log = open(logfile_path, "a")
        self.__fee_rate = 0 
        self.__api = api

    def run(self): 
        # Iterate over traded securities 
        for s in self.__securities: 
            # check for stop loss or take_profit sells if the security was owned
                  
            # do dynamic_ema 
                 
              

class Security:     
    """ 
    A class to represent a security of the financial type. For example, a stock/ETF.
    """
    def __init__(self, trade_symbol, tradable_balance, ema, ema_length, price_movement_threshold, currently_owned, days_since_readjustment, prev_price_data): 
        """
        :param trade_symbol: The ticker  
        :param tradable_balance: The amount (in USD) allotted to trading this security  
        :param currently_owned: Whether or not this security is currently owned 
        :param ema: The n-day ema for the security 
        """
        self.trade_symbol = trade_symbol
        self.tradable_balance = tradable_balance
        self.ema = ema
        self.__ema_length = 0
        self.__price_movement_threshold = 0
        self.currently_owned = currently_owned
        self.__days_since_parameter_readjustment = days_since_readjustment

    def __str__(self): 
        return trade_symbol + ", " + str(tradable_balance) + ", " + str(ema) + ", " + str(ema_length) + ", " + str(price_movement_threshold) + ", " + str(currently_owned) + ", " + str(days_since_readjustment) + ", " + str(prev_price_data)
