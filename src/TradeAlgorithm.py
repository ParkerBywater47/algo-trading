class TradeAlgorithm:
    def __init__(self): 
        raise NotImplementedError("TradeAlgorithm is an abstract base class and should not be instantiated")

    def run(self, today_price, context):
        raise NotImplementedError("TradeAlgorithm is an abstract base class and should not be instantiated")

    def average(self, lst): 
        the_sum = 0
        for i in lst: 
            the_sum += i
        return the_sum / len(lst)
