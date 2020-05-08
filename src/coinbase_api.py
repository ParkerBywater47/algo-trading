import json, hashlib, time, requests, base64, hmac, sys


ENDPOINT = 'https://api-public.sandbox.pro.coinbase.com'
key_file = open("keys/coinbase-sandbox.txt")
API_KEY = key_file.readline().strip()
API_SECRET = key_file.readline().strip()
API_PASS = key_file.readline().strip()
key_file.close()


def make_coinbase_request(method, path, req_body=''): 
    """
    :method is HTTP method as str
    :path is the path to resource as str  
    :req_body is the body of the request if needed. Instance of dict
    """
    timestamp = str(time.time())
    headers = {
            'CB-ACCESS-SIGN': sign(method, path, API_SECRET,  timestamp, req_body), 
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
    
    if isinstance(resp.json(), list):
        print(resp.json()[0])
    else: 
        print(resp.json())


def sign(method, path,  secret, timestamp, req_body=""): 
    #timestamp = "1588881000.89"
    message = timestamp + method + path + (req_body if req_body == "" else str(json.dumps(req_body))) 
#    print("prehash string: " + message)
    hmac_key = base64.b64decode(secret) 
    signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
    signature_b64_encoded = base64.b64encode(signature.digest())
#    print("b64 sig: ", signature_b64_encoded) 
    return signature_b64_encoded
    

def main(): 
    """ a test main """
    make_coinbase_request("GET", "/accounts")
    order = {
        'size': 0.5,
       'price': 9882,
        'side': 'buy',
       'product_id': 'BTC-USD',
    }
    make_coinbase_request("POST", "/orders", order) 
    #make_coinbase_request("GET", "/orders") 


if __name__ == "__main__": 
    main() 

