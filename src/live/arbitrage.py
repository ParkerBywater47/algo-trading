import coinbase_api
import time

fee_rate = .005


def arbitrage():
    # filter through to get only the currencies that are online 
    # filter only currencies that can traded to USDC
    # make sure that each currency can be traded to each other currency in the list
   
    all_currencies = coinbase_api.get_products() 
   
    # this will be a list of lists 
    filtered_currencies = []

    # a dictionary to hold the index of a currency in filtered_currencies for fast access
    currencies_indices = dict()
    for currency in all_currencies: 
        if currency["status"] == "online":
            if currency["base_currency"] not in currencies_indices: 
                filtered_currencies.append({
                                            "currency": currency["base_currency"], 
                                            "quote_currencies": [currency["quote_currency"]], 
                                            "ids": [currency["id"]]
                                            })
                currencies_indices[currency["base_currency"]] = len(filtered_currencies) - 1
            else: 
                filtered_currencies[currencies_indices[currency["base_currency"]]]["quote_currencies"].append(currency["quote_currency"])
                filtered_currencies[currencies_indices[currency["base_currency"]]]["ids"].append(currency["id"])
                

    to_remove = []   
    for i in range(len(filtered_currencies)):
        if 'USDC' not in filtered_currencies[i]['quote_currencies']: 
            to_remove.append(i)

    removed = 0
    for i in to_remove:
        filtered_currencies.pop(i - removed)
        removed += 1

#    for i in filtered_currencies: 
#        print(i) 

    # select a pair of currencies   
    for i in range(len(filtered_currencies) - 1):
        for j in range(i + 1, len(filtered_currencies)): 
            first_currency = filtered_currencies[i]
            second_currency = filtered_currencies[j]

            if not (first_currency["currency"] in second_currency["quote_currencies"] or second_currency["currency"] in first_currency["quote_currencies"]):
                continue
            # the currency that contains the other in its quote_currencies list is the one that has the id which 
            # should be used to get the exchange rate
            #if first_currency["currency"] in second_currency["quote_currencies"]):
                
            if second_currency["currency"] in first_currency["quote_currencies"]: 
                temp = first_currency
                first_currency = second_currency
                second_currency = temp
   
            USDC_to_first = 1 / coinbase_api.get_price(first_currency["currency"] + "-USDC")
            first_to_second = 1 / coinbase_api.get_price(second_currency["currency"] + "-" + first_currency["currency"])
            second_to_USDC = coinbase_api.get_price(second_currency["currency"] + "-USDC")
           
            discrepancy = abs(USDC_to_first * first_to_second * second_to_USDC - 1)
            if discrepancy > fee_rate:
                print(format(discrepancy * 100, ".3f") +  "% on " + first_currency["currency"] + " and " + second_currency["currency"])

    # Find exchange rate from USDC to first currency 
    # Find exchange rate from first currency to second currency
    # compute exchange from USDC to first
    # compute


def main():
    while True:
        arbitrage()
        time.sleep(60)


if __name__ == "__main__": 
    main()
