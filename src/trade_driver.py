import websocket
import json
import _thread as thread
import time
import sma


last_trade_time = time.time() - 4000 # wow Parker.. A global and a magic number? 
previous_periods = [10025.35, 9997.99, 9915.86, 9943.57, 9929.65]


def on_message(ws, message):
    """ 
    This function seems to be called every time a message is sent or received" 
    """ 
    try: 
        resp = json.loads(message)
        if time.time() >= last_trade_time + 3600: 
            algos.sma(resp['price'], previous_periods)
                         

        print(resp['price'])
        
    except Exception as ex:
        print(ex)
        print(previous_periods)


def on_open(ws):
    def run(*args):
#        time.sleep(1)
        plz_subscrib = {
            "type": "subscribe",
            "channels": [{  "name": "ticker", 
                            "product_ids": ["BTC-USD"] }]
            }
        ws.send(json.dumps(plz_subscrib))
#        time.sleep(1)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com", on_message = on_message)
    ws.on_open = on_open
    ws.run_forever()


