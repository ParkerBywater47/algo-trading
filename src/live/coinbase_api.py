import json, hashlib, time, requests, base64, hmac, sys
from datetime import datetime, timedelta


SANDBOX_ENDPOINT = "https://api-public.sandbox.pro.coinbase.com"
LIVE_ENDPOINT = "https://api.pro.coinbase.com"

ENDPOINT = LIVE_ENDPOINT
if ENDPOINT == LIVE_ENDPOINT:
    key_file = open("keys/coinbase.txt")
    API_KEY = key_file.readline().strip()
    API_SECRET = key_file.readline().strip()
    API_PASS = key_file.readline().strip()
else:
    key_file = open("keys/coinbase-sandbox.txt")
    API_KEY = key_file.readline().strip()
    API_SECRET = key_file.readline().strip()
    API_PASS = key_file.readline().strip()
key_file.close()


def get_BTC_balance():
    accounts_get = coinbase_GET("/accounts")    
    
    # search for BTC in the list
    for i in accounts_get:
        if i["currency"] == "BTC": 
            return float(i["available"])    


def get_USDC_balance():
    accounts_get = coinbase_GET("/accounts")    
    
    # search for USDC in the list
    for i in accounts_get:
        if i["currency"] == "USDC": 
            return float(i["available"])    


def coinbase_GET(path, request_body=''): 
    timestamp = str(time.time())
    headers = {
            'CB-ACCESS-SIGN': sign('GET', path, API_SECRET,  timestamp, request_body), 
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': API_KEY,
            'CB-ACCESS-PASSPHRASE': API_PASS,
            'Content-Type': 'application/json', 
            }
    if request_body == "": 
        resp = requests.get(ENDPOINT + path, headers=headers)
    else: 
        resp = requests.get(ENDPOINT + path, headers=headers, json=request_body)
    return resp.json()


def coinbase_POST(path, request_body=''):
    timestamp = str(time.time()) 
    headers = {
            'CB-ACCESS-SIGN': sign('POST', path, API_SECRET,  timestamp, request_body), 
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': API_KEY,
            'CB-ACCESS-PASSPHRASE': API_PASS,
            'Content-Type': 'application/json', 
            }
    resp = requests.post(ENDPOINT + path, headers=headers, json=request_body)
    return resp.json()


def coinbase_DELETE(path, request_body=''):
    timestamp = str(time.time()) 
    headers = {
            'CB-ACCESS-SIGN': sign('DELETE', path, API_SECRET,  timestamp, request_body), 
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': API_KEY,
            'CB-ACCESS-PASSPHRASE': API_PASS,
            'Content-Type': 'application/json', 
            }
    if request_body == '': 
        resp = requests.delete(ENDPOINT + path, headers=headers)
    else:
        resp = requests.delete(ENDPOINT + path, headers=headers, json=request_body)
    return resp.json()


def main(): 
    #print(json.dumps(get_products(), sort_keys=True, indent=4)) 
    print(get_price()) 
    print(get_bid()) 
    print(get_ask()) 
   

def sign(method, path,  secret, timestamp, req_body=""): 
    message = timestamp + method + path + (req_body if req_body == "" else str(json.dumps(req_body))) 
    hmac_key = base64.b64decode(secret) 
    signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
    signature_b64_encoded = base64.b64encode(signature.digest())
    return signature_b64_encoded


def get_bid(ticker="BTC-USDC"): 
    return float(coinbase_GET("/products/" + ticker + "/ticker")["bid"])


def get_ask(ticker="BTC-USDC"): 
    return float(coinbase_GET("/products/" + ticker + "/ticker")["ask"])


def get_price(ticker="BTC-USDC"): 
    return float(coinbase_GET("/products/" + ticker + "/ticker")["price"])


def get_products(): 
    return coinbase_GET("/products")


def get_historic_rates(start=None, end=None, periods=3):  
    """ 
    format of data returned from Coinbase is 
        [[UNIX timestamp, low, high, open, close, volume]...]
    sorted in descending order by timestamp, that is, more recent data at front of list
    """
    close = 4 # see above docstring
    an_hour = 3600 # hour in seconds
    granularity=60 # granularity is size of time slice in seconds 

    end = datetime.now() - timedelta(hours=1)
    start = end - timedelta(hours=periods)
#    request_body = {
#        "granularity": granularity , 
#        "start": start.isoformat(), 
#        "end": end.isoformat(),
#    }

    endpoint = "/products/BTC-USDC/candles"
    # TODO find out how to get datetime module to handle timezones instead of hardcoding UTC offset
    params_str = "granularity=" + str(granularity) + "&" \
               + "end=" + str(end.isoformat()) + "-07:00" + "&" \
               + "start=" + str(start.isoformat()) + "-07:00" + "&" 
    url = endpoint + "?" + params_str
    candles = coinbase_GET(url)
    out = [candles[x * int(an_hour / granularity)][close] for x in range(0, periods)] 
    out.reverse() # reverse because other parts of app expect more recent data at higher indices
    return out

    
           
    

# This should not be used, but I left the code here because I don't want to go find it again if I need it
#def public_price():
#    return float(requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC").json()['data']['rates']['USD'])


def path_builder(path, get_params):
    """
    :path is str 
    :get_params is dict
    """ 
    out = path
    for key in get_params.keys():
        out += "?" + key + "=" + get_params[key] + "&"
    return out


if __name__ == "__main__": 
    main() 

