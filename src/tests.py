import coinbase_api
import json

smallest_trade_amt = .0000001
fee_rate = .005

current_price = 9460 #coinbase_api.get_price() 
sell_price = int(current_price * .9995 * 100) / 100
max_sell_amt = coinbase_api.get_BTC_balance() / (1 + fee_rate) 
coins_to_sell = int(coinbase_api.get_BTC_balance() * (1 / smallest_trade_amt)) * smallest_trade_amt
print(current_price, sell_price, coins_to_sell)

sell_order = {
    'size': coins_to_sell,
    'price': sell_price, 
    'side': 'sell',
    'product_id': 'BTC-USD',
}


print(json.dumps(coinbase_api.coinbase_POST("/orders", sell_order), sort_keys=True, indent=4))
