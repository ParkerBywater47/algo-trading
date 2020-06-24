cd $1

data=*.txt
extension=".txt"

for item in $data; do 
    tt.py sort $item > sorted.txt;
    tt.py tac sorted.txt > $(echo $item | cut -d'_' -f 1)$extension;
done;

rm sorted.txt;
