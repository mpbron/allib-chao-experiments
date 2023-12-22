#!/bin/bash
# Our custom function
echo "Reading path $1 as dataset"
echo "Setting $2 as dataset name"
echo "Selecting path $3 as result target"
echo "Selecting path $4 as job target"
podman run -ti \
  --rm \
  -v $1:/app/data:z \
  -v $3:/app/output/:z \
  -v $4:/app/jobs/:z \
  allib-chao python3 divide.py -d ./data -n $2 -t ./output -j ./jobs
jobname="job_$2.sh"
jobpath="$4/$jobname"
podman run -ti \
  --rm \
  -v $1:/app/data:z \
  -v $3:/app/output/:z \
  -v $4:/app/jobs/:z \
  -v jobpath:/app/job.sh:z \
  allib-chao ./job.sh