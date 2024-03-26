#!/bin/bash

echo "Reading path $1 as dataset"
echo "Selecting path $2 as result target"
touch $2
filepath="$(pwd)/$2"
docker run -ti \
  --rm \
  -v $1:/app/data/ \
  -v $filepath:/app/outputfile.pkl \
  allib-chao python3 readdata.py -s /app/data -t ./outputfile.pkl