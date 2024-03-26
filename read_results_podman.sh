#!/bin/bash

echo "Reading path $1 as dataset"
echo "Selecting path $2 as result target"
touch $2
filepath="$(pwd)/$2"
podman run -ti \
  --rm \
  -v $1:/app/data/:z \
  -v $filepath:/app/outputfile.pkl:z \
  allib-chao python3 readdata.py -s $datapath -t ./outputfile.pkl