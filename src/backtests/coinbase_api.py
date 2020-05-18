import json, hashlib, time, requests, base64, hmac, sys


ENDPOINT = "https://api-public.sandbox.pro.coinbase.com"
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
    """for tests and such"""
    print(get_BTC_balance())
    print(get_USDC_balance())
    print(get_price())
    print(json.dumps(coinbase_GET("/products/BTC-USD/ticker"), sort_keys=True, indent=4))


def sign(method, path,  secret, timestamp, req_body=""): 
    message = timestamp + method + path + (req_body if req_body == "" else str(json.dumps(req_body))) 
    hmac_key = base64.b64decode(secret) 
    signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
    signature_b64_encoded = base64.b64encode(signature.digest())
    return signature_b64_encoded


def get_price(): 
    """ return the price to a precision of two decimal points because Coinbase requires this """ 
    return float(coinbase_GET("/products/BTC-USD/ticker")["bid"])
    return float(requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC").json()['data']['rates']['USD'])


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

