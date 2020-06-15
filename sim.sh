data_dir="long-backtest-data/"
$tickers="COKE HAL KOS MRO RCL SLB UCO USO WFC XOM CSCO CCL GILD"
tickers="HAL"
hist_suffix="_h.csv"
sim_suffix="_s.csv"
out_path="testing-results/"
fuck_bash="_para_raw.txt"

for ticker in $tickers; do 
    echo $ticker; 
    ./dynema $data_dir$ticker$hist_suffix $data_dir$ticker$sim_suffix; 
    backtest.py dynema $data_dir$ticker$(echo ".csv"); 
    echo
#    ./parallel_find_optimal_dynema.out $data_dir$ticker$hist_suffix $data_dir$ticker$sim_suffix > $out_path$ticker$fuck_bash;
done; 
