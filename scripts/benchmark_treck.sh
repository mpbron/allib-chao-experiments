#!/bin/bash
# Our custom function
echo "Reading path $1 for TREC datasets"
echo "Using selection in $2"
echo "Running experiments specified in $3"
echo "Writing results in $4"
echo "Repeating each experiment $5 times"
echo "Excluding topics with ids specified in $6"
echo "Running on $7 parallel cores"
./create_trec_jobs.sh $1 $2 $3 $4 $5 $6| parallel -j $7