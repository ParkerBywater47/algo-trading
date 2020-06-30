import requests
import json
import alpaca_trade_api 

key_file = open("keys/alpaca.txt")
key_id = key_file.readline().strip()
secret_key = key_file.readline().strip()
key_file.close()

ticker = "HAL"
some_balance = 40.123423509

alpaca_api = alpaca_trade_api.REST(key_id, secret_key, api_version='v2')

headers = { 
            "APCA-API-KEY-ID": key_id, 
            "APCA-API-SECRET-KEY": secret_key, 
        }

#print(json.dumps(alpaca_api.get_last_quote("CCL")._raw, sort_keys=True, indent=4))
#print(json.dumps(alpaca_api.get_orders()._raw, sort_keys=True, indent=4))
bid_price=15.43

order_resp = alpaca_api.submit_order(
    symbol="CCL",
    side='buy',
    type='market',
    qty="1", 
    time_in_force='day',
    order_class='bracket',
    take_profit={ 
        "limit_price": str(1.15 * bid_price),
    },  
    stop_loss={
        "stop_price": str((1 - .075) * bid_price),
    })
print(json.dumps(order_resp._raw, sort_keys=True, indent=4))


#alpaca_api.cancel_all_orders()

#resp = alpaca_api.list_positions()
#resp = alpaca_api.get_account() 
#bid_price = alpaca_api.get_last_quote(ticker)
#print(bid_price)
#last_trade = alpaca_api.get_last_trade(ticker)._raw
#print(bid_price, last_trade)
#resp = alpaca_api.submit_order(
#    symbol=ticker,
#    side='buy',
#    type='market',
#    qty='1',
#    time_in_force='day',
#    order_class='bracket',
#    take_profit= {
#        "limit_price": str(1.15 * bid_price),
#    },  
#    stop_loss = {
#        "stop_price": str((1 - .075) * bid_price),
#        "limit_price": str((1 - .075) * bid_price),
#    } 
#)

#resp = alpaca_api.get_order("f63db4a0-04f2-4520-93ee-213bf17ea45e")
#print(resp)


#print(resp)
#resp = requests.get(endpoint + "/v1/last_quote/stocks/COKE", headers=headers)
#print(resp)
#resp = requests.get(endpoint + "/v2/account", headers=headers)

#print(json.dumps(resp.json(), sort_keys=True, indent=4))
