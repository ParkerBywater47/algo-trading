tickers=["CCL", "KOS", "XOM", "MRO", "RCL", "SLB", "UCO", "USO", "WFC", "CSCO", "GILD", "COKE", "HAL"]

dataset1="testing-results/dataset1/"
dataset2="testing-results/dataset2/"

   
for ticker in tickers:
    with open(dataset1 + ticker + ".txt") as f: 
        for i in range(5):   
            line = f.readline()
            splits = line.split(",")
            print("./convolute2.sh " + ticker + " " + splits[1].strip() + " " +  splits[2].strip())

for ticker in tickers:
    with open(dataset2 + ticker + ".txt") as f: 
        for i in range(5):   
            line = f.readline()
            splits = line.split(",")
            print("./convolute1.sh " + ticker + " " + splits[1].strip() + " " +  splits[2].strip())
