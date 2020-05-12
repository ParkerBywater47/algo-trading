import json, hashlib, time, requests, base64, hmac, sys


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

def make_coinbase_call(method, path, req_body='', get_params=None): 
    """
    :method is HTTP method as str
    :path is the path to resource as str  
    :req_body is the body of the request if needed. Instance of dict
    """
    timestamp = str(time.time())
    if get_params is None:
        headers = {
                'CB-ACCESS-SIGN': sign(method, path, API_SECRET,  timestamp, req_body), 
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-KEY': API_KEY,
                'CB-ACCESS-PASSPHRASE': API_PASS,
                'Content-Type': 'application/json', 
                }
    else: 
        path_with_params = path_builder(path, get_params)  
        headers = {
                'CB-ACCESS-SIGN': sign(method, path_with_params, API_SECRET,  timestamp, req_body), 
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-KEY': API_KEY,
                'CB-ACCESS-PASSPHRASE': API_PASS,
                'Content-Type': 'application/json'
                }

    if method == "GET": 
        resp = requests.get(ENDPOINT + path, headers=headers)
    elif method == "POST":
        resp = requests.post(ENDPOINT + path, headers=headers, json=req_body)
    else: 
        print("HTTP method '" + method + "' not supported")
        sys.exit(1)

    return resp.json()
    
#    if isinstance(resp.json(), list) and len(resp.json()) > 0:
#        # use json.dumps because Python prints with fucking single quotes
#        print(str(json.dumps(resp.json()))[1:-1])
#    else: 
#        print(json.dumps(resp.json()))


def coinbase_GET(path, request_body=''): 
    timestamp = str(time.time())
    headers = {
            'CB-ACCESS-SIGN': sign('POST', path, API_SECRET,  timestamp, request_body), 
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': API_KEY,
            'CB-ACCESS-PASSPHRASE': API_PASS,
            'Content-Type': 'application/json', 
            }
    if request_body != "": 
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
    """ a test main """
    current_price = float(requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC").json()['data']['rates']['USD'])
    ask_price = int(current_price * 1.0025 * 100) / 100
    stop_loss_price = int(current_price * .925 * 100) / 100
    order = {
        'size': 0.001,
        'price': ask_price, 
        'side': 'buy',
        'product_id': 'BTC-USDC',
        'stop':'loss', 
        'stop_price': stop_loss_price, 
    }
    #print(json.dumps(make_coinbase_call('GET', "/orders"), sort_keys=True, indent=4))
    #print(json.dumps(coinbase_POST("/orders", order), sort_keys=True, indent=4))
    print(json.dumps(coinbase_DELETE("/orders/18ea5f96-9429-430e-99ef-8467ff351e0f"), sort_keys=True, indent=4))
    #print(json.dumps(make_coinbase_call('GET', "/currencies"), sort_keys=True, indent=4))


def sign(method, path,  secret, timestamp, req_body=""): 
    message = timestamp + method + path + (req_body if req_body == "" else str(json.dumps(req_body))) 
    hmac_key = base64.b64decode(secret) 
    signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
    signature_b64_encoded = base64.b64encode(signature.digest())
    return signature_b64_encoded


def get_price(): 
    """ return the price to a precision of two decimal points cuz coi boi api """ 
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

