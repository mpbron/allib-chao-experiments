#!/bin/bash
# Our custom function
echo "Reading path $1 as dataset"
echo "Setting $2 as dataset name"
echo "Selecting path $3 as result target"
echo "Selecting path $4 as job target"
echo "Repeating each method with $5 different seed sets"
echo "Executing jobs with Low memory requirements with $6 CPU cores"
echo "Executing jobs with Medium memory requirements wth $7 CPU cores"
echo "Executing jobs with High memory requirements with $8 CPU cores"
python3 divide.py -d $1 -n $2 -t $3 -j $4 --iterations $5 --highcpu $6 --mediumcpu $7 --lowcpu $8
cd $4
jobname="job_$2.sh"
jobpath="./$jobname"
echo "Starting experiments"
sh $jobpath