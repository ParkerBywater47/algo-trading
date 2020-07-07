# cd into first command line arg if given
if  [[ $# -ne 0 ]]; then cd $1; fi

data=*.txt
extension=".txt"
for item in $data; do 
    sort $item > sorted.txt;
    tac sorted.txt > $(echo $item | cut -d'_' -f 1)$extension;
done;
rm sorted.txt;
