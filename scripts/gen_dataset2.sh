tickers="CCL KOS XOM MRO RCL SLB UCO USO WFC CSCO HAL"
hist_suffix="_h.csv"
sim_suffix="_s.csv"
out_dir="../data/dataset1/"
base_link="https://query1.finance.yahoo.com/v7/finance/download/" 


# These GET parameters correspond to data up to the beginning of 2020 
hists=("?period1=1514764800&period2=1546300800&interval=1d&events=history" "?period1=1483228800&period2=1514764800&interval=1d&events=history" "?period1=1451692800&period2=1483228800&interval=1d&events=history" "?period1=1420156800&period2=1451692800&interval=1d&events=history" "?period1=1388620800&period2=1420156800&interval=1d&events=history")
sims=("?period1=1546300800&period2=1577836800&interval=1d&events=history" "?period1=1514764800&period2=1577836800&interval=1d&events=history" "?period1=1483228800&period2=1577836800&interval=1d&events=history" "?period1=1451692800&period2=1577836800&interval=1d&events=history" "?period1=1420156800&period2=1577836800&interval=1d&events=history")

for ticker in $tickers; do
    for i in {0..4}; do 
        curl $base_link$ticker$(echo ${hists[i]}) > $out_dir$ticker$i$hist_suffix
        curl $base_link$ticker$(echo ${sims[i]}) > $out_dir$ticker$i$sim_suffix
    done; 
done; 
