data_dir="../data/dataset1/"
tickers="CCL KOS XOM MRO RCL SLB UCO USO WFC CSCO HAL"
hist_suffix="_h.csv"
sim_suffix="_s.csv"
out_path="../testing-results/dataset1/"
out_file_suffix="_para_raw.txt"

for ticker in $tickers; do 
    echo $ticker; 
    ../bin/find_optimal_dynema.out $data_dir$ticker$(echo 4)$hist_suffix $data_dir$ticker$(echo 4)$sim_suffix > $out_path$ticker$out_file_suffix; 
    #backtest.py dynema $data_dir$ticker$(echo ".csv"); 
done; 
