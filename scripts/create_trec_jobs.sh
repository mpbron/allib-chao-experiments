#!/bin/bash
for topic in $(cat $2); do
    for m in $(cat $4); do
        for ((i = 1; i <= $5; i++)); do
            echo "python3 -m allib benchmark -m Trec -d $1 -i $topic -t $3 -e $m -r $i"
        done
    done
done