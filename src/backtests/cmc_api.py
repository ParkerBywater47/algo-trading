import json, hashlib, time, requests, base64, hmac, sys


ENDPOINT = 'https://pro-api.coinmarketcap.com/v1'
key_file = open("keys/coinmarketcap.txt")
API_KEY = key_file.readline().strip()
key_file.close()


def make_cmc_call(method, path, req_body=''): 
    """
    :method is HTTP method as str
    :path is the path to resource as str  
    :req_body is the body of the request if needed. Instance of dict
    """
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    parameters = { 
        'id':'1'    # id refers to the crpytocurrency
    }

    if method == "GET": 
        resp = requests.get(ENDPOINT + path, headers=headers, params=parameters)
    elif method == "POST":
        resp = requests.post(ENDPOINT + path, headers=headers, json=req_body)
    else: 
        print("HTTP method '" + method + "' not supported")
        sys.exit(1)
    
    try: 
        print("response:", resp.text) 
        resp_dict = resp.json()
        #print(json.dumps(resp.json()))
        return resp_dict
    except Exception as ex:
        print(ex)
        print("resp:", resp)


def get_price(): 
    return float(make_cmc_call("GET", "/cryptocurrency/quotes/latest")["data"]["1"]["quote"]["USD"]["price"]) 

def main(): 
    """ a test main """
    make_cmc_call("GET", "/cryptocurrency/quotes/latest")


if __name__ == "__main__": 
    main() 

