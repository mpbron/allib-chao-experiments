#!/bin/bash
# Our custom function
echo "Reading path $1 as TREC dataset"
echo "Selecting Topics specified $2"
echo "Writing results in $3"
echo "Running experiments specified in $4"
echo "Repeating each experiment $5 times"
echo "Running on $6 parallel cores"
podman run -ti \
  --rm \
  -v $1:/app/data:z \
  -v $2:/app/parameters/selection.txt:z \
  -v $3:/app/output/:z \
  -v $4:/app/parameters/experiments.txt:z \
  allib-chao ./benchmark_review.sh ./data ./parameters/selection.txt ./output ./parameters/experiments.txt $5 $6