#!/bin/bash

# data from "elements of statistical learning"
# http://www-stat.stanford.edu/~tibs/ElemStatLearn/data.html

# recursive download with wget to get train.[0-9]
wget -Nr --level=1 --no-parent \
    http://www-stat.stanford.edu/~tibs/ElemStatLearn/datasets/zip.digits/ 

# move files to digits/ directory
mkdir digits
find www-stat.stanford.edu -name 'train.[0-9]' -exec mv {} digits/ \;
rm -rf www-stat.stanford.edu/

# create README for data
wget -O digits/README http://www-stat.stanford.edu/~tibs/ElemStatLearn/datasets/zip.info

