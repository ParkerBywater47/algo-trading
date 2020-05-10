import json, hashlib, time, requests, base64, hmac, sys


ENDPOINT = 'https://api.pro.coinbase.com'
key_file = open("keys/coinbase.txt")
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
                'Content-Type': 'application/json'
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
        resp = requests.get(ENDPOINT + path, headers=headers, params=get_params)
    elif method == "POST":
        resp = requests.post(ENDPOINT + path, headers=headers, json=req_body)
    else: 
        print("HTTP method '" + method + "' not supported")
        sys.exit(1)
    
    if isinstance(resp.json(), list) and len(resp.json()) > 0:
        # use json.dumps because Python prints with fucking single quotes
        print(str(json.dumps(resp.json()))[1:-1])
    else: 
        print(json.dumps(resp.json()))


def sign(method, path,  secret, timestamp, req_body=""): 
    #timestamp = "1588881000.89"
    message = timestamp + method + path + (req_body if req_body == "" else str(json.dumps(req_body))) 
#    print("prehash string: " + message)
    hmac_key = base64.b64decode(secret) 
    signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
    signature_b64_encoded = base64.b64encode(signature.digest())
#    print("b64 sig: ", signature_b64_encoded) 
    return signature_b64_encoded


def path_builder(path, get_params):
    """
    :path is str 
    :get_params is dict
    """ 
    out = path
    for key in get_params.keys():
        out += "?" + key + "=" + get_params[key] + "&"
    return out


def main(): 
    """ a test main """
#    make_coinbase_call("GET", "/accounts")
#    make_coinbase_call("GET", "/products")
#    make_coinbase_call("GET", "/fills", get_params={"product_id":"BTC-USDC"})
#    make_coinbase_call("GET", "/coinbase-accounts")
#    make_coinbase_call("POST", "/orders", order) 
#    make_coinbase_call("GET", "/orders") 
 

    print( int((float(requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC").json()['data']['rates']['USD']) * 1.0025) * 100) / 100)
    order = {
        'size': 0.001,
        'price': int((float(requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC").json()['data']['rates']['USD']) * 1.0025) * 100) / 100, 
        'side': 'buy',
        'product_id': 'BTC-USDC',
    }
    make_coinbase_call("POST", "/orders", order)


if __name__ == "__main__": 
    main() 

