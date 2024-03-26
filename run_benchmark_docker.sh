#!/bin/bash

echo "Reading path $1 as dataset"
echo "Setting $2 as dataset name"
echo "Selecting path $3 as result target"
echo "Selecting path $4 as job target"
echo "Repeating each method with $5 different seed sets"
echo "Executing jobs with Low memory requirements with $6 CPU cores"
echo "Executing jobs with Medium memory requirements wth $7 CPU cores"
echo "Executing jobs with High memory requirements with $8 CPU cores"
datapath="/app/data/$2"
targetpathlocal="$3/$2"
mkdir -p $targetpathlocal
jobfile=$(docker run -ti \
  --rm \
  -v $1:$datapath \
  -v $targetpathlocal:/app/output/ \
  -v $4:/app/jobs/ \
  allib-chao python3 divide.py -d $datapath -n $2 -t ./output -j ./jobs --iterations $5 --lowmemcpu $6 --mediummemcpu $7 --highmemcpu $8)
jobname="job_$2.sh"
jobpath="/app/jobs/$jobname"
docker run -ti \
  --rm \
  -v $1:$datapath \
  -v $targetpathlocal:/app/output/ \
  -v $4:/app/jobs/ \
  allib-chao $jobpath