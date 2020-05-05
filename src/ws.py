import websocket
import json
import _thread as thread
import time



def on_message(ws, message):
    """ 
    This function seems to be called every time a message is sent or received" 
    """ 
    try: 
        resp = json.loads(message)
#        f = open("../data/BTC_realtime_data.csv", "a")
#        f.write(str(resp['price']) + "," + resp['time'][resp['time'].find("T") + 1:resp['time'].find(".")] + "\n")
#        f.close()
        print(resp['price'])
        
    except Exception: 
        pass


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

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
#    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
