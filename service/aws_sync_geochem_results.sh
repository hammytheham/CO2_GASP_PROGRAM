#!/bin/bash
cd $1
zip -r geochem_result_$3.zip $2

rm -r $2

aws s3 sync . s3://co-2-gasp-bucket/temp/OUTPUT_DATA/geochemical_result --delete

rm geochem_result_$3.zip



