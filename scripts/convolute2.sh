data_dir="data/dataset2/"
hist_suffix="_h.csv"
sim_suffix="_s.csv"

ticker=$1
readjust=$2
lookback=$3
for i in {0..4}; do 
    ./dynema.out $data_dir$ticker$(echo $i)$hist_suffix $data_dir$ticker$(echo $i)$sim_suffix $readjust $lookback
done;
