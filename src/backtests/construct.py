data_dir = "../../data/"
results_dir = "../../testing-results/dataset2/"

tickers=["CCL", "KOS", "XOM", "MRO", "RCL", "SLB", "UCO", "USO", "WFC", "CSCO", "GILD", "COKE", "HAL"]

for ticker in tickers: 
    pps=[]
    with open(data_dir+ticker, "r") as f: 
        f.readline()
        for line in f: 
            splits = line.split(",")
            pps.append(float(splits[4].strip()))
       
        best_file = open(results_dir + ticker + ".txt")
        best_split = best_file.readline().split(",")
        best_file.close() 
        print("Security(\"" + ticker + "\", 50, None, False, 0, " + best_split[1] + ", " + best_split[2] + ", "  + str(pps) + "),")
