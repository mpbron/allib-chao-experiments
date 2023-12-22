#!/bin/bash
for dataset in $(cat $2); do 
    f="$1/$dataset.csv"
    for m in $(cat $4); do
        for ((i = 1; i <= $5; i++)); do
            echo "python3 -m allib benchmark -m Review -d $f -t $3 -e $m -r $i"
        done
    done
done
