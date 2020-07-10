tickers="CCL KOS XOM MRO RCL SLB UCO USO WFC CSCO HAL"
hist_suffix="_h.csv"
sim_suffix="_s.csv"
out_dir="../data/dataset1/"
base_link="https://query1.finance.yahoo.com/v7/finance/download/" 

# These GET parameters correspond to data up to 6/19/20 (inclusive)
hists=("?period1=1529452800&period2=1560988800&interval=1d&events=history" "?period1=1497916800&period2=1529452800&interval=1d&events=history" "?period1=1466380800&period2=1497916800&interval=1d&events=history" "?period1=1434758400&period2=1466380800&interval=1d&events=history" "?period1=1403222400&period2=1434758400&interval=1d&events=history")
sims=("?period1=1560988800&period2=1592611200&interval=1d&events=history" "?period1=1529452800&period2=1592611200&interval=1d&events=history" "?period1=1497916800&period2=1592611200&interval=1d&events=history" "?period1=1466380800&period2=1592611200&interval=1d&events=history" "?period1=1434758400&period2=1592611200&interval=1d&events=history")

for ticker in $tickers; do
    for i in {0..4}; do 
        curl $base_link$ticker$(echo ${hists[i]}) > $out_dir$ticker$i$hist_suffix
        curl $base_link$ticker$(echo ${sims[i]}) > $out_dir$ticker$i$sim_suffix
    done; 
done; 
